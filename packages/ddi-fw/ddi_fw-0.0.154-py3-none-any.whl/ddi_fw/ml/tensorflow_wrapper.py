from typing import Any, Callable
from ddi_fw.ml.model_wrapper import ModelWrapper
import tensorflow as tf
from tensorflow import keras
# from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, Callback
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
import numpy as np
from tensorflow.keras import Model
import mlflow
from mlflow.utils.autologging_utils import batch_metrics_logger

from mlflow.models import infer_signature
from ddi_fw.ml.evaluation_helper import Metrics, evaluate

# import tf2onnx
# import onnx

import ddi_fw.utils as utils
import os


class TFModelWrapper(ModelWrapper):

    def __init__(self, date, descriptor, model_func, use_mlflow=True, **kwargs):
        super().__init__(date, descriptor, model_func, **kwargs)
        self.batch_size = kwargs.get('batch_size', 128)
        self.epochs = kwargs.get('epochs', 100)
        self.use_mlflow = use_mlflow

    def fit_model(self, X_train, y_train, X_valid, y_valid):
        self.kwargs['input_shape'] = self.train_data.shape
        model = self.model_func(**self.kwargs)
        checkpoint = ModelCheckpoint(
            filepath=f'{self.descriptor}_validation.weights.h5',
            monitor='val_loss',
            save_best_only=True,
            save_weights_only=True,
            verbose=1,
            mode='min'
        )
        early_stopping = EarlyStopping(
            monitor='val_loss', patience=10, mode='auto')
        custom_callback = CustomCallback(self.use_mlflow)
        train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        train_dataset = train_dataset.batch(batch_size=self.batch_size)

        if X_valid is not None and y_valid is not None:
            val_dataset = tf.data.Dataset.from_tensor_slices(
                (X_valid, y_valid))
            val_dataset = val_dataset.batch(batch_size=self.batch_size)
        else:
            val_dataset = None

        history = model.fit(
            train_dataset,
            epochs=self.epochs,
            # validation_data=val_dataset,
            callbacks=[early_stopping, checkpoint, custom_callback]
        )
        # ex
        # history = model.fit(
        #     X_train, y_train,
        #     batch_size=self.batch_size,
        #     epochs=self.epochs,
        #     validation_data=(X_valid, y_valid),
        #     callbacks=[early_stopping, checkpoint, custom_callback]
        # )

        if os.path.exists(f'{self.descriptor}_validation.weights.h5'):
            os.remove(f'{self.descriptor}_validation.weights.h5')

        return checkpoint.model, checkpoint

    def fit(self):
        print(self.train_data.shape)
        models = {}
        models_val_acc = {}
        if self.train_idx_arr is not None and self.val_idx_arr is not None:
            for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
                print(f"Validation {i}")

                if self.use_mlflow:
                    with mlflow.start_run(run_name=f'Validation {i}', description='CV models', nested=True) as cv_fit:
                        X_train_cv = self.train_data[train_idx]
                        y_train_cv = self.train_label[train_idx]
                        X_valid_cv = self.train_data[val_idx]
                        y_valid_cv = self.train_label[val_idx]
                        model, checkpoint = self.fit_model(
                            X_train_cv, y_train_cv, X_valid_cv, y_valid_cv)
                        models[f'{self.descriptor}_validation_{i}'] = model
                        models_val_acc[f'{self.descriptor}_validation_{i}'] = checkpoint.best
                else:
                    X_train_cv = self.train_data[train_idx]
                    y_train_cv = self.train_label[train_idx]
                    X_valid_cv = self.train_data[val_idx]
                    y_valid_cv = self.train_label[val_idx]
                    model, checkpoint = self.fit_model(
                        X_train_cv, y_train_cv, X_valid_cv, y_valid_cv)
                    models[f'{self.descriptor}_validation_{i}'] = model
                    models_val_acc[f'{self.descriptor}_validation_{i}'] = checkpoint.best
        else:
            if self.use_mlflow:
                with mlflow.start_run(run_name=f'Training', description='Training', nested=True) as cv_fit:
                    model, checkpoint = self.fit_model(
                        self.train_data, self.train_label, None, None)
                    models[self.descriptor] = model
                    models_val_acc[self.descriptor] = checkpoint.best
            else:
                model, checkpoint = self.fit_model(
                    self.train_data, self.train_label, None, None)
                models[self.descriptor] = model
                models_val_acc[self.descriptor] = checkpoint.best

        best_model_key = max(models_val_acc, key=lambda k: models_val_acc[k])
        # best_model_key = max(models_val_acc, key=models_val_acc.get)
        best_model = models[best_model_key]
        return best_model, best_model_key

    # https://github.com/mlflow/mlflow/blob/master/examples/tensorflow/train.py

    def predict(self):
        test_dataset = tf.data.Dataset.from_tensor_slices(
            (self.test_data, self.test_label))
        test_dataset = test_dataset.batch(batch_size=1)
        # pred = self.best_model.predict(self.test_data)
        pred = self.best_model.predict(test_dataset)
        return pred

    def fit_and_evaluate(self, print_detail=False) -> tuple[dict[str, Any], Metrics, Any]:
        if self.use_mlflow:
            with mlflow.start_run(run_name=self.descriptor, description="***", nested=True) as run:
                print(run.info.artifact_uri)
                best_model, best_model_key = self.fit()
                print(best_model_key)
                self.best_model: Model = best_model
                pred = self.predict()
                logs, metrics = evaluate(
                    actual=self.test_label, pred=pred, info=self.descriptor, print_detail=print_detail)
                metrics.format_float()
                mlflow.log_metrics(logs)
                mlflow.log_param('best_cv', best_model_key)
                utils.compress_and_save_data(
                    metrics.__dict__, run.info.artifact_uri, f'{self.date}_metrics.gzip')
                mlflow.log_artifact(
                    f'{run.info.artifact_uri}/{self.date}_metrics.gzip')

                return logs, metrics, pred
        else:
            best_model, best_model_key = self.fit()
            print(best_model_key)
            self.best_model = best_model
            pred = self.predict()
            logs, metrics = evaluate(
                actual=self.test_label, pred=pred, info=self.descriptor)
            metrics.format_float()
            return logs, metrics, pred


"""
    Custom Keras callback for logging training metrics and model summary to MLflow.
"""


class CustomCallback(Callback):
    def __init__(self, use_mlflow: bool = True):
        super().__init__()
        self.use_mlflow = use_mlflow

    def _mlflow_log(self, func: Callable):
        if self.use_mlflow:
            func()

    def on_train_begin(self, logs=None):
        if logs is None:
            logs = {}
        if not isinstance(self.model, Model):
            raise TypeError("self.model must be an instance of Model")

        keys = list(logs.keys())
        self._mlflow_log(lambda: mlflow.log_param("train_begin_keys", keys))
        # config = self.model.optimizer.get_config()
        config = self.model.get_config()
        for attribute in config:
            self._mlflow_log(lambda: mlflow.log_param(
                "opt_" + attribute, config[attribute]))

        sum_list = []
        self.model.summary(print_fn=sum_list.append)
        summary = "\n".join(sum_list)
        self._mlflow_log(lambda: mlflow.log_text(
            summary, artifact_file="model_summary.txt"))

    def on_train_end(self, logs=None):
        if logs is None:
            logs = {}
        print(logs)
        self._mlflow_log(lambda: mlflow.log_metrics(logs))

    def on_epoch_begin(self, epoch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_epoch_end(self, epoch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_test_begin(self, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_test_end(self, logs=None):
        if logs is None:
            logs = {}
        self._mlflow_log(lambda: mlflow.log_metrics(logs))
        print(logs)

    def on_predict_begin(self, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_predict_end(self, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())
        self._mlflow_log(lambda: mlflow.log_metrics(logs))

    def on_train_batch_begin(self, batch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_train_batch_end(self, batch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_test_batch_begin(self, batch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_test_batch_end(self, batch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_predict_batch_begin(self, batch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())

    def on_predict_batch_end(self, batch, logs=None):
        if logs is None:
            logs = {}
        keys = list(logs.keys())
