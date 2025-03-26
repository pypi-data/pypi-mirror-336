import asyncio
import logging
import os
import uuid
from collections.abc import Sequence
from typing import Any, Optional, Union

import mlflow
from mlflow.entities import Metric, Param, Run, RunTag

from ..configs import MlflowConfig
from ..utils.decorators import lock_decorator

__all__ = [
    "init_mlflow_connection",
    "MlflowClient",
]

logger = logging.getLogger("mlflow")


def init_mlflow_connection(
    config: MlflowConfig,
    experiment_uuid: str,
    mlflow_run_name: Optional[str] = None,
    experiment_name: Optional[str] = None,
    experiment_description: Optional[str] = None,
    experiment_tags: Optional[dict[str, Any]] = None,
) -> tuple[str, tuple[str, mlflow.MlflowClient, Run, str]]:
    """
    Initialize an MLflow connection with a new or existing experiment and run.

    - **Args**:
        config (MlflowConfig): Configuration containing MLflow credentials and URI.
        experiment_uuid (str): A unique identifier for the experiment.
        mlflow_run_name (str, optional): Name of the MLflow run. Defaults to a generated name.
        experiment_name (str, optional): Name of the experiment. Defaults to a generated name.
        experiment_description (str, optional): Description for the experiment. Defaults to None.
        experiment_tags (dict, optional): Tags to associate with the experiment. Defaults to None.

    - **Returns**:
        tuple: A tuple containing the run_id and another tuple with the MLflow URI, client, run object, and run UUID.
    """
    if config.username is not None:
        os.environ["MLFLOW_TRACKING_USERNAME"] = config.username
    if config.password is not None:
        os.environ["MLFLOW_TRACKING_PASSWORD"] = config.password

    run_uuid = str(uuid.uuid4())
    # run name
    if mlflow_run_name is None:
        mlflow_run_name = f"exp_{run_uuid}"

    # exp name
    if experiment_name is None:
        experiment_name = f"run_{run_uuid}"

    # tags
    if experiment_tags is None:
        experiment_tags = {}
    ## exp uuid
    experiment_tags["experiment_id"] = experiment_uuid
    ## description
    if experiment_description is not None:
        experiment_tags["mlflow.note.content"] = experiment_description

    uri = config.mlflow_uri
    client = mlflow.MlflowClient(tracking_uri=uri)

    # experiment
    try:
        experiment_id = client.create_experiment(
            name=experiment_name,
            tags=experiment_tags,
        )
    except Exception as e:
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment is None:
            raise e
        experiment_id = experiment.experiment_id

    # run
    run = client.create_run(experiment_id=experiment_id, run_name=mlflow_run_name)

    run_id = run.info.run_id

    return run_id, (uri, client, run, run_uuid)


class MlflowClient:
    """A wrapper around MLflow's MlflowClient for managing experiments and runs."""

    def __init__(
        self,
        config: MlflowConfig,
        experiment_uuid: str,
        mlflow_run_name: Optional[str] = None,
        experiment_name: Optional[str] = None,
        experiment_description: Optional[str] = None,
        experiment_tags: Optional[dict[str, Any]] = None,
        run_id: Optional[str] = None,
    ) -> None:
        """
        Initialize the MlflowClient.

        - **Args**:
            config (dict): Configuration containing MLflow credentials and URI.
            experiment_uuid (str): A unique identifier for the experiment.
            mlflow_run_name (str, optional): Name of the MLflow run. Defaults to a generated name.
            experiment_name (str, optional): Name of the experiment. Defaults to a generated name.
            experiment_description (str, optional): Description for the experiment. Defaults to None.
            experiment_tags (dict, optional): Tags to associate with the experiment. Defaults to None.
            run_id (str, optional): Existing MLflow run ID to attach to. Defaults to None.
        """
        if run_id is None:
            self._run_id, (
                self._mlflow_uri,
                self._client,
                self._run,
                self._run_uuid,
            ) = init_mlflow_connection(
                config=config,
                experiment_uuid=experiment_uuid,
                mlflow_run_name=mlflow_run_name,
                experiment_name=experiment_name,
                experiment_description=experiment_description,
                experiment_tags=experiment_tags,
            )
        else:
            self._mlflow_uri = uri = config.mlflow_uri
            if config.username is not None:
                os.environ["MLFLOW_TRACKING_USERNAME"] = config.username
            if config.password is not None:
                os.environ["MLFLOW_TRACKING_PASSWORD"] = config.password
            self._client = client = mlflow.MlflowClient(tracking_uri=uri)
            self._run = client.get_run(run_id=run_id)
            self._run_id = run_id
            self._run_uuid = run_uuid = str(uuid.uuid4())
        self._lock = asyncio.Lock()

    @property
    def client(
        self,
    ) -> mlflow.MlflowClient:
        """Return the underlying MLflow client."""
        return self._client

    @property
    def run_id(
        self,
    ) -> str:
        """Return the current run ID."""
        assert self._run_id is not None
        return self._run_id

    @lock_decorator
    async def log_batch(
        self,
        metrics: Sequence[Metric] = (),
        params: Sequence[Param] = (),
        tags: Sequence[RunTag] = (),
    ):
        """
        Log a batch of metrics, parameters, and tags to the MLflow run.

        This method is thread-safe due to the `@lock_decorator`.
        """
        self.client.log_batch(
            run_id=self.run_id, metrics=metrics, params=params, tags=tags
        )

    @lock_decorator
    async def log_metric(
        self,
        key: str,
        value: float,
        step: Optional[int] = None,
        timestamp: Optional[int] = None,
    ):
        """
        Log a single metric to the MLflow run.

        This method is thread-safe due to the `@lock_decorator`.

        - **Args**:
            key (str): The name of the metric.
            value (float): The value of the metric.
            step (int, optional): The step at which the metric was recorded. Defaults to None.
            timestamp (int, optional): The timestamp when the metric was recorded. Defaults to None.
        """
        if timestamp is not None:
            timestamp = int(timestamp)
        self.client.log_metric(
            run_id=self.run_id,
            key=key,
            value=value,
            timestamp=timestamp,
            step=step,
        )
