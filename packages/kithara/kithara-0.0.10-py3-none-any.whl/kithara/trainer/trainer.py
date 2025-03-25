"""
 Copyright 2025 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

import os

os.environ["KERAS_BACKEND"] = "jax"
import keras
import time
import sys
import jax
from kithara.distributed.sharding.utils import (
    entire_tree_is_sharded,
    is_not_sharded_and_is_large,
    get_size_in_mb,
    get_size_in_gb,
)
from kithara.model import Model
from kithara.dataset import Dataloader
from kithara.callbacks import Profiler, Checkpointer
from kithara.distributed.sharding._data_sharding import DataSharding
from keras.src.backend.common import global_state
from typing import Any, Union, List, Tuple
import jax.tree_util as jtu
import numpy as np


class Trainer:
    """
    A Trainer class for training and evaluating Kithara models. This base class is designed to be
    subclassed for implementing custom training objectives.

    Attributes:
        model (kithara.Model): The model to be trained or evaluated.
        optimizer (keras.Optimizer): The optimizer used for training.
        train_dataloader (kithara.Dataloader): A dataloader that provides training batches.
        eval_dataloader (kithara.Dataloader, optional): A dataloader that provides evaluation batches.
            Defaults to None.
        steps (int, optional): The total number of training steps to execute, where each step processes
            one batch of data. Defaults to None and trains 1 epoch.
        epochs (int, optional): The total number of training epochs to execute. Defaults to None. If
            steps is also set to None, falls back to training for 1 epoch.
        log_steps_interval (int, optional): The interval between logging steps. Each log includes the
            current loss value and performance metrics. Defaults to 1.
        eval_steps_interval (int, optional): The interval between evaluation steps. Only one of
            eval_steps_interval or eval_epochs_interval can be set.
        eval_epochs_interval (int, optional): The interval between evaluation epochs. Only one of
            eval_steps_interval or eval_epochs_interval can be set.
        max_eval_samples (int, optional): The maximum number of samples to use during evaluation.
            Uses the entire evaluation dataset if not provided.
        tensorboard_dir (str, optional): The directory path for TensorBoard logs. Can be either a
            local directory or a Google Cloud Storage (GCS) path. Defaults to None.
        profiler (kithara.Profiler, optional): A profiler instance for monitoring performance metrics. Defaults to None.

    Methods:
        loss_fn: Returns a JAX-compatible callable that computes the loss value from logits and labels.
            Defaults to SparseCategoricalCrossentropy.
        train(): Executes the main training loop.
        evaluate(state=None): Performs evaluation using batches from eval_dataloader.
        generate(prompt, stop_token_ids="auto"): Generates text responses in inference mode.
        save_model(filepath): Saves model weights in HDF5 (.h5) format.
    """

    def __init__(
        self,
        model: Model,
        optimizer: keras.Optimizer,
        train_dataloader: Dataloader,
        eval_dataloader: Dataloader = None,
        steps=None,
        epochs=None,
        log_steps_interval=1,
        eval_steps_interval=None,
        eval_epochs_interval=None,
        max_eval_samples=sys.maxsize,
        tensorboard_dir=None,
        profiler: Profiler = None,
        checkpointer: Checkpointer = None,
    ):
        if steps is None and epochs is None:
            epochs = 1
        if (
            (eval_dataloader is not None)
            and (eval_steps_interval is None)
            and (eval_epochs_interval is None)
        ):
            eval_epochs_interval = 1

        # Core components
        self.model = model
        self.optimizer = optimizer
        self.train_dataloader = train_dataloader
        self.eval_dataloader = eval_dataloader

        # Training parameters
        self.steps = steps
        self.epochs = epochs
        self.tensorboard_dir = tensorboard_dir
        self.step_count = 0
        self.epoch_count = 0
        self.eval_steps_interval = eval_steps_interval
        self.eval_epochs_interval = eval_epochs_interval
        self.max_eval_samples = max_eval_samples
        self.log_steps_interval = log_steps_interval
        self.global_batch_size = train_dataloader.global_batch_size
        self.profiler = profiler
        self.checkpointer = checkpointer
        self._validate_setup()

        # Initialize optimizer and callbacks
        self.optimizer.build(self.model.trainable_variables)
        self.callbacks = self._create_callbacks()
        if self.tensorboard_dir:
            # Tensorboard requires reading "iteration" from model.optimizer
            self.model.optimizer = optimizer

        # JIT compile training and evaluation steps for better performance
        self.train_step = self._make_train_step()
        self.eval_step = self._make_eval_step()

        # Configure data sharding strategy
        self.data_sharding = global_state.get_global_attribute(
            "DATA_SHARDING", DataSharding["fully_replicated"]
        )
        self.device_count = jax.device_count()

        # Validate setup and print summary
        self._print_run_summary()
        self._validate_memory_usage()

    @property
    def loss_fn(self):
        """Define the loss function for training and evaluation. This property
        is intended to be overriden with custom loss functions.

        Returns:
            A JAX callable that takes y_true and logits as input and returns the loss value.
        """
        return keras.losses.SparseCategoricalCrossentropy(
            from_logits=True,
            reduction="mean",  # per token loss
            ignore_class=self.train_dataloader.dataset.tokenizer.pad_token_id,
        )

    def compute_loss(self, trainable_variables, non_trainable_variables, x, y):
        """Compute model loss in a stateless manner. This function is intended
        to use together with jax.grad, i.e. grad_fn =
        jax.value_and_grad(compute_loss, has_aux=True)

        Args:
            trainable_variables: Model's trainable parameters, obtained with `model.trainable_variables`
            non_trainable_variables: Model's non-trainable parameters, obtained with `model.non_trainable_variables`
            x: Input data
            y: Target data

        Returns:
            tuple: (loss value, updated non-trainable variables)
        """
        logits, non_trainable_variables = self.model.stateless_call(
            trainable_variables, non_trainable_variables, x
        )
        loss = self.loss_fn(y, logits)

        return loss, non_trainable_variables

    @property
    def grad_fn(self):
        """Stateless function that returns the value and gradients from the
        `compute_loss` function."""

        return jax.value_and_grad(self.compute_loss, has_aux=True)

    def _train_step(self, state: Tuple[List[jax.Array]], data: dict):
        """Execute a single training step.

        Args:
            state: Current model state (trainable variables, non-trainable variables, optimizer variables)
            data: Batch of training data, a dictionary containing "x" (input) and "y" (target) entries.
            Input value is directly fed into the model, so it should be exact format expected by the model.
            Target value is used to compute the loss, and should be in the exact format expected by the loss function.

        Returns:
            tuple: (loss value, updated state)
        """
        (
            trainable_variables,
            non_trainable_variables,
            optimizer_variables,
        ) = state
        x, y = data["x"], data["y"]
        (loss, non_trainable_variables), grads = self.grad_fn(
            trainable_variables, non_trainable_variables, x, y
        )
        trainable_variables, optimizer_variables = self.optimizer.stateless_apply(
            optimizer_variables, grads, trainable_variables
        )
        return (
            loss,
            (
                trainable_variables,
                non_trainable_variables,
                optimizer_variables,
            ),
        )

    def train(self):
        """Execute the main training loop.

        This method handles:
        - Epoch iteration
        - Batch processing
        - Loss computation
        - Model updates
        - Progress logging
        - Periodic evaluation
        """

        print("-> Start training...")
        print("The first training step will be slow due to JAX compilation.")

        state = self._get_jax_state(
            trainable_variables=True,
            non_trainable_variables=True,
            optimizer_variables=True,
        )

        self.callbacks.on_train_begin()

        # Training loop
        while True:
            self.epoch_count += 1
            self.callbacks.on_epoch_begin(self.epoch_count)

            epoch_loss = 0
            batches_seen_in_epoch = 0

            # Process each batch in the epoch
            for batch_input in self.train_dataloader:
                if self.steps and self.step_count >= self.steps:
                    break
                self.step_count += 1

                start_time = time.time()
                self.callbacks.on_train_batch_begin(self.step_count)

                # Prepare and validate input
                batch_input = self._prepare_batch_input_for_training(batch_input)
                self._validate_sharding_correctness(batch_input, state)

                # Execute training step
                loss, state = self.train_step(state, batch_input)
                epoch_loss += loss
                batches_seen_in_epoch += 1

                self._update_model_with_state(state)

                # Wait for computation to complete for accurate step time
                jax.block_until_ready(loss)

                # Calculate training step statistics
                step_time = time.time() - start_time

                tokens_per_second_per_device = (
                    self.global_batch_size
                    * self.train_dataloader.dataset.max_seq_len
                    / (step_time * self.device_count)
                )

                samples_per_second = self.global_batch_size / step_time

                step_stats = {
                    "step": self.step_count,
                    "loss": round(float(loss), 3),
                    "step_time": round(step_time, 2),
                    "epoch": self.epoch_count,
                    "tokens_per_second_per_device": round(
                        tokens_per_second_per_device, 1
                    ),
                    "tokens_per_second": round(
                        tokens_per_second_per_device * self.device_count, 1
                    ),
                    "samples_per_second": round(samples_per_second, 2),
                    "train_steps_per_second": round(1 / step_time, 2),
                    "samples_seen": self.global_batch_size * self.step_count,
                    "learning_rate": round(float(self.optimizer.learning_rate.value),7),
                }

                # Log progress
                if (
                    self.step_count == 1
                    or self.step_count % self.log_steps_interval == 0
                ):
                    print(step_stats)

                self.callbacks.on_train_batch_end(self.step_count, step_stats)

                # Step based evaluation
                if (
                    (self.eval_dataloader is not None)
                    and (self.eval_steps_interval is not None)
                    and (self.step_count % self.eval_steps_interval == 0)
                ):
                    self.evaluate(state)

            # Compute epoch statistics
            # If no custom loss_fn is supplied, the default *step loss* calculates
            # the per-token loss (i.e. average of the loss from #non-padding tokens in batch).
            # The *epoch loss* is simply the average of the step losses. It is not the exact
            # per-token loss across the epoch, but rather a proxy.
            epoch_loss = epoch_loss / batches_seen_in_epoch
            self.callbacks.on_epoch_end(self.epoch_count, {"epoch_loss": epoch_loss})
            print(
                f"Train epoch {self.epoch_count} (epoch may be incompete) loss : {epoch_loss}"
            )

            # Epoch based evaluation
            if (
                (self.eval_dataloader is not None)
                and (self.eval_epochs_interval is not None)
                and (self.epoch_count % self.eval_epochs_interval == 0)
            ):
                self.evaluate(state)

            # Check termination conditions
            if self.steps and self.step_count >= self.steps:
                break
            if self.epochs and self.epoch_count >= self.epochs:
                break

        self.callbacks.on_train_end()

    def save_model(self, filepath):
        """Save model weights in .h5 format.

        Args:
            filepath (str): Path where model weights will be saved
        """
        self.model.save_weights(filepath)

    def _eval_step(self, state: Tuple[List[jax.Array]], data: dict):
        """Execute a single evaluation step.

        This method performs forward propagation without gradient computation
        to evaluate model performance on provided data.

        Args:
            state: Tuple containing (trainable_variables, non_trainable_variables, optimizer_state)
            data: Dictionary containing input data 'x' and target data 'y'.
            Data should be in the same format as expected by _train_step function.

        Returns:
            tuple: (logits, loss value)
        """
        (trainable_variables, non_trainable_variables, _) = state
        x, y = data["x"], data["y"]
        logits, non_trainable_variables = self.model.stateless_call(
            trainable_variables, non_trainable_variables, x, training=False
        )
        loss = self.loss_fn(y, logits)
        return logits, loss

    def evaluate(self, state=None):
        """Execute the evaluation loop on batches of data provided by the
        `eval_dataloader`.

        This method:
        1. Processes the evaluation dataset
        2. Computes model predictions and loss
        3. Tracks and reports evaluation metrics
        4. Handles callbacks for monitoring

        Args:
            state: Optional tuple of model state. If None, current model state is used.
            Contains (trainable_variables, non_trainable_variables, optimizer_variables)
        """

        if state is None:
            state = self._get_jax_state(
                trainable_variables=True,
                non_trainable_variables=True,
                optimizer_variables=True,
            )

        # Initialize evaluation
        self.callbacks.on_test_begin()
        eval_loss = 0
        eval_batches_seen = 0
        eval_start_time = time.time()
        # Process each batch in evaluation dataset
        for step_i, batch_input in enumerate(self.eval_dataloader):
            if (eval_batches_seen + 1) * self.global_batch_size > self.max_eval_samples:
                break

            start_time = time.time()
            # Prepare and shard input
            batch_input = self._prepare_batch_input_for_training(batch_input)
            self._validate_sharding_correctness(batch_input, state)

            # Eval step
            logits, loss = self.eval_step(state, batch_input)

            # Accumulate metrics
            eval_loss += loss
            eval_batches_seen += 1

            # Logging
            if (step_i + 1) % self.log_steps_interval == 0:

                jax.block_until_ready(loss)

                step_time = time.time() - start_time
                samples_per_second = self.global_batch_size / step_time

                tokens_per_second_per_device = (
                    self.global_batch_size
                    * self.train_dataloader.dataset.max_seq_len
                    / (step_time * self.device_count)
                )

                step_stats = {
                    "eval_loss": round(float(loss), 3),
                    "eval_step": step_i,
                    "step_time": round(step_time, 2),
                    "tokens_per_second_per_device": round(
                        tokens_per_second_per_device, 1
                    ),
                    "tokens_per_second": round(
                        tokens_per_second_per_device * self.device_count, 1
                    ),
                    "eval_samples_per_second": round(samples_per_second, 2),
                    "eval_steps_per_second": round(1 / step_time, 2),
                }

                print(step_stats)

        # Compute final metrics and report results
        eval_loss = eval_loss / eval_batches_seen
        eval_time = time.time() - eval_start_time

        tokens_per_second_per_device = (
            eval_batches_seen
            * self.global_batch_size
            * self.train_dataloader.dataset.max_seq_len
        ) / (eval_time * self.device_count)

        samples_per_second = eval_batches_seen * self.global_batch_size / eval_time

        self.callbacks.on_test_end(
            {
                "eval_loss": eval_loss,
                "eval_samples_seen": eval_batches_seen * self.global_batch_size,
                "eval_time": eval_time,
                "tokens_per_second_per_device": tokens_per_second_per_device,
                "tokens_per_second": tokens_per_second_per_device * self.device_count,
                "samples_per_second": samples_per_second,
                "eval_steps_per_second": eval_batches_seen / eval_time,
            }
        )

        print(f"Eval loss after {self.step_count} training steps: ", eval_loss)

        return eval_loss

    def _make_train_step(self):
        return jax.jit(self._train_step, donate_argnums=(0,))

    def _make_eval_step(self):
        return jax.jit(self._eval_step, donate_argnums=(0,))

    def _get_jax_state(
        self,
        trainable_variables=False,
        non_trainable_variables=False,
        optimizer_variables=False,
    ):
        state = []
        if trainable_variables:
            state.append([v.value for v in self.model.trainable_variables])
        if non_trainable_variables:
            state.append([v.value for v in self.model.non_trainable_variables])
        if optimizer_variables:
            state.append([v.value for v in self.optimizer.variables])
        return tuple(state)

    def _form_global_array(self, path, array: np.ndarray) -> jax.Array:
        """Convert local array to globally sharded array for distributed
        computing. Each accelerator host should call `_form_global_array` with
        their local batch shard, this function will from a logical global batch
        that is sharded across all devices, abiding by the `self.data_sharding`
        partitioning.

        Args:
            path: Tree path for the array (used in error reporting)
            array (np.ndarray): Input array to be distributed

        Returns:
            jax.Array: Distributed global batch
        """

        seq_len = array.shape[1]
        global_shape = (self.global_batch_size, seq_len)

        try:
            local_device_arrays = np.split(
                array, len(self.data_sharding.mesh.local_devices), axis=0
            )
        except ValueError as array_split_error:
            raise ValueError(
                f"Unable to put to devices shape {array.shape} with "
                f"local device count {len(self.data_sharding.mesh.local_devices)} "
                f"at {jtu.keystr(path)}"
            ) from array_split_error

        local_device_buffers = jax.device_put(
            local_device_arrays, self.data_sharding.mesh.local_devices
        )
        return jax.make_array_from_single_device_arrays(
            global_shape, self.data_sharding, local_device_buffers
        )

    def _update_model_with_state(self, state):
        """Update model internal parameters with the provided state."""
        trainable_variables, non_trainable_variables, optimizer_variables, *_ = state
        for variable, value in zip(self.model.trainable_variables, trainable_variables):
            value = jax.lax.with_sharding_constraint(value, variable._layout)
            variable.assign(value)
        for variable, value in zip(
            self.model.non_trainable_variables, non_trainable_variables
        ):
            value = jax.lax.with_sharding_constraint(value, variable._layout)
            variable.assign(value)

        for variable, value in zip(self.optimizer.variables, optimizer_variables):
            value = jax.lax.with_sharding_constraint(value, variable._layout)
            variable.assign(value)

    def _prepare_batch_input_for_training(self, batch: List[str]):
        return jtu.tree_map_with_path(self._form_global_array, batch)

    def _print_run_summary(self):

        training_duration = (
            f"Steps = {self.steps:,}" if self.steps else f"Epochs = {self.epochs}"
        )
        trainable_params = sum(
            get_size_in_gb(v.value) for v in self.model.trainable_variables
        )
        total_params = trainable_params + sum(
            get_size_in_gb(v.value) for v in self.model.non_trainable_variables
        )
        trainable_params_percent = round((trainable_params / total_params) * 100, 2)
        logo_with_key_stats = (
            f"       '==='\n"
            f"        |||\n"
            f"     '- ||| -'\n"
            f"    /  |||||  \\   Kithara | Device Count = {self.device_count}\n"
            f"   |   (|||)   |  {training_duration} | Batch size per device = {self.global_batch_size // self.device_count}\n"
            f"   |   |◕‿◕|   |  Total batch size = {self.global_batch_size} | Total parameters = {total_params:.3f}(GB)\n"
            f"    \\  |||||  /   Trainable parameters = {trainable_params:.3f}(GB) ({trainable_params_percent}%) | Non-trainable = {total_params - trainable_params:.3f}(GB)\n"
            f"     --|===|--   "
        )
        print(logo_with_key_stats)

        # TODO: Implement more structured logging
        for attr_name, attr_value in vars(self).items():
            print(attr_name, attr_value)

    def _create_callbacks(self):
        callbacks = []
        if self.tensorboard_dir:
            callbacks.append(
                keras.callbacks.TensorBoard(
                    log_dir=self.tensorboard_dir,
                    update_freq="batch",
                    write_steps_per_second=True,
                )
            )
        if self.profiler:
            callbacks.append(self.profiler)
        if self.checkpointer:
            callbacks.append(self.checkpointer)

        return keras.callbacks.CallbackList(callbacks, model=self.model)

    def _validate_sharding_correctness(self, data, state):
        """This method performs several sharding correctness checks and prints
        warnings for any sharding issues detected.

        1. Checks if data is properly sharded
        2. Validates sharding of trainable variables
        3. Validates sharding of non-trainable variables
        4. Validates sharding of optimizer variables

        Args:
            data: Input batch to validate
            state: Current model state tuple

        """
        try:
            if not entire_tree_is_sharded(data):
                print(
                    "Warning: data is not sharded",
                    data["y"].shape,
                    data["y"].sharding,
                )
            for variable, value in zip(self.model.trainable_variables, state[0]):
                if is_not_sharded_and_is_large(value):
                    print(
                        f"Step {self.step_count}: trainable variable is not sharded",
                        f"{get_size_in_mb(value)}mb",
                        variable.path,
                        value.shape,
                        value.sharding,
                    )
            for variable, value in zip(self.model.non_trainable_variables, state[1]):
                if is_not_sharded_and_is_large(value):
                    print(
                        f"Step {self.step_count}: nontrainable variable is not sharded",
                        f"{get_size_in_mb(value)}mb",
                        variable.path,
                        value.shape,
                        value.sharding,
                    )
            for variable, value in zip(self.optimizer.variables, state[2]):
                if is_not_sharded_and_is_large(value):
                    print(
                        f"Step {self.step_count}: optimizer variable is not sharded",
                        f"{get_size_in_mb(value)}mb",
                        variable.path,
                        value.shape,
                        value.sharding,
                    )
        except Exception as e:
            print(f"Error during sharding correctness validation: {e}")

    def _validate_memory_usage(self):
        """This method checks the current HBM usage matches the expected HBM
        usage.

        Current HBM usage is calculated by summing the size of all live arrays,
        expected HBM usage is calculated by summing the size of all model and
        optimizer variables.
        """

        total_size = 0
        for v in self.model.variables:
            total_size += get_size_in_mb(v.value)

        for v in self.optimizer.variables:
            total_size += get_size_in_mb(v.value)

        live_arrays = jax.live_arrays()
        live_arrays_size = 0
        for v in live_arrays:
            live_arrays_size += get_size_in_mb(v)

        if not np.isclose(total_size, live_arrays_size, atol=1.0):
            print(
                f"WARNING: Potential memory leakage. HBM usage is {live_arrays_size:.3f} MB "
                f"but model and optimizer are only {total_size:.3f} MB in size."
            )
        else:
            print(
                f"✅ No memory leakage detected. HBM usage ({live_arrays_size:.3f} MB) "
                f"matches model and optimizer size ({total_size:.3f} MB)."
            )

        try: 
            memory_info = jax.local_devices()[0].memory_stats()
            memory_per_device_mb = memory_info["bytes_limit"] / (1024**2)
            total_memory = memory_per_device_mb * jax.device_count()
            print(f"Total memory available is {total_memory:.3f} MB, if you run into "
                "errors, check if your memory usage is close to the limit, and either "
                "reduce your per-device batch size or sequence length.")
        except Exception as e:
            # memory_info is not available on some TPUs
            pass 
    
    def _validate_setup(self):
        assert (
            self.max_eval_samples >= self.global_batch_size
        ), "Number of eval examples must be greater or equal to global batch size"

        assert not (
            (
                self.eval_steps_interval is not None
                or self.eval_epochs_interval is not None
            )
            and self.eval_dataloader is None
        ), "Evaluation interval is set but no evaluation dataloader is provided"

        assert (
            self.steps is None or self.epochs is None
        ), "Specify either steps or epochs, not both"

        assert (self.eval_steps_interval is None) or (
            self.eval_epochs_interval is None
        ), "Specify either eval_steps_interval or eval_epochs_interval, not both"
