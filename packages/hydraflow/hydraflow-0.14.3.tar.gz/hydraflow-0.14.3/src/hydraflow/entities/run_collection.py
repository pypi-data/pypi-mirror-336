"""Provide a collection of MLflow runs.

This module includes the `RunCollection` class, which serves as a container
for multiple MLflow `Run` instances, and various methods to filter and
retrieve these runs.

Key Features:
- **Run Management**: The `RunCollection` class allows for easy management of
  multiple MLflow runs, providing methods to filter and retrieve runs based
  on various criteria.
- **Filtering**: Support filtering runs based on specific configurations
  and parameters, enabling users to easily find runs that match certain conditions.
- **Retrieval**: Users can retrieve specific runs, including the first, last, or any
  run that matches a given configuration.
- **Artifact Handling**: Provide methods to access and manipulate the
  artifacts associated with each run, including retrieving artifact URIs and
  directories.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from typing import TYPE_CHECKING, Any, overload

import hydraflow.core.param
from hydraflow.core.config import iter_params, select_config, select_overrides
from hydraflow.core.io import load_config
from hydraflow.core.param import get_params, get_values

from .run_data import RunCollectionData
from .run_info import RunCollectionInfo

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from typing import Any

    from mlflow.entities.run import Run


@dataclass
class RunCollection:
    """Represent a collection of MLflow runs.

    Provide methods to interact with the runs, such as filtering,
    retrieving specific runs, and accessing run information.

    Key Features:
    - Filtering: Easily filter runs based on various criteria.
    - Retrieval: Access specific runs by index or through methods.
    - Metadata: Access run metadata and associated information.
    """

    _runs: list[Run]
    """A list of MLflow `Run` instances."""

    _info: RunCollectionInfo = field(init=False)
    """An instance of `RunCollectionInfo`."""

    _data: RunCollectionData = field(init=False)
    """An instance of `RunCollectionData`."""

    def __post_init__(self) -> None:
        self._info = RunCollectionInfo(self)
        self._data = RunCollectionData(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self)})"

    def __len__(self) -> int:
        return len(self._runs)

    def __iter__(self) -> Iterator[Run]:
        return iter(self._runs)

    @overload
    def __getitem__(self, index: int) -> Run: ...

    @overload
    def __getitem__(self, index: slice) -> RunCollection: ...

    def __getitem__(self, index: int | slice) -> Run | RunCollection:
        if isinstance(index, slice):
            return self.__class__(self._runs[index])

        return self._runs[index]

    def __contains__(self, run: Run) -> bool:
        return run in self._runs

    def __bool__(self) -> bool:
        return bool(self._runs)

    def __add__(self, other: RunCollection) -> RunCollection:
        """Add another `RunCollection` to this one.

        Args:
            other (RunCollection): The `RunCollection` to add.

        Returns:
            A new `RunCollection` instance with the runs from both collections.

        """
        return self.__class__(self._runs + other._runs)

    def __sub__(self, other: RunCollection) -> RunCollection:
        """Subtract another `RunCollection` from this one.

        Args:
            other (RunCollection): The `RunCollection` to subtract.

        Returns:
            A new `RunCollection` instance with the runs that are in this collection
            but not in the other.

        """
        runs = [run for run in self._runs if run not in other._runs]
        return self.__class__(runs)

    @property
    def info(self) -> RunCollectionInfo:
        """An instance of `RunCollectionInfo`."""
        return self._info

    @property
    def data(self) -> RunCollectionData:
        """An instance of `RunCollectionData`."""
        return self._data

    def one(self) -> Run:
        """Get the only `Run` instance in the collection.

        Returns:
            The only `Run` instance in the collection.

        Raises:
            ValueError: If the collection does not contain exactly one run.

        """
        if len(self._runs) != 1:
            raise ValueError("The collection does not contain exactly one run.")

        return self._runs[0]

    def try_one(self) -> Run | None:
        """Try to get the only `Run` instance in the collection.

        Returns:
            The only `Run` instance in the collection, or None if the collection
            does not contain exactly one run.

        """
        return self._runs[0] if len(self._runs) == 1 else None

    def first(self) -> Run:
        """Get the first `Run` instance in the collection.

        Returns:
            The first `Run` instance in the collection.

        Raises:
            ValueError: If the collection is empty.

        """
        if not self._runs:
            raise ValueError("The collection is empty.")

        return self._runs[0]

    def try_first(self) -> Run | None:
        """Try to get the first `Run` instance in the collection.

        Returns:
            The first `Run` instance in the collection, or None if the collection
            is empty.

        """
        return self._runs[0] if self._runs else None

    def last(self) -> Run:
        """Get the last `Run` instance in the collection.

        Returns:
            The last `Run` instance in the collection.

        Raises:
            ValueError: If the collection is empty.

        """
        if not self._runs:
            raise ValueError("The collection is empty.")

        return self._runs[-1]

    def try_last(self) -> Run | None:
        """Try to get the last `Run` instance in the collection.

        Returns:
            The last `Run` instance in the collection, or None if the collection
            is empty.

        """
        return self._runs[-1] if self._runs else None

    def filter(
        self,
        config: object | Callable[[Run], bool] | None = None,
        *,
        select: list[str] | None = None,
        overrides: list[str] | None = None,
        status: str | list[str] | int | list[int] | None = None,
        **kwargs,
    ) -> RunCollection:
        """Filter the `Run` instances based on the provided configuration.

        This method filters the runs in the collection according to the
        specified configuration object and additional key-value pairs. The
        configuration object and key-value pairs should contain key-value pairs
        that correspond to the parameters of the runs. Only the runs that match
        all the specified parameters will be included in the returned
        `RunCollection` object.

        The filtering supports:
        - Exact matches for single values.
        - Membership checks for lists of values.
        - Range checks for tuples of two values (inclusive of both the lower
          and upper bound).
        - Callable that takes a `Run` object and returns a boolean value.

        Args:
            config (object | Callable[[Run], bool] | None): The configuration object
                to filter the runs. This can be any object that provides key-value
                pairs through the `iter_params` function, or a callable that
                takes a `Run` object and returns a boolean value.
            select (list[str] | None): The list of parameters to select.
            overrides (list[str] | None): The list of overrides to filter the
                runs.
            status (str | list[str] | int | list[int] | None): The status of the
                runs to filter.
            **kwargs: Additional key-value pairs to filter the runs.

        Returns:
            A new `RunCollection` object containing the filtered runs.

        """
        return RunCollection(
            filter_runs(
                self._runs,
                config,
                select=select,
                overrides=overrides,
                status=status,
                **kwargs,
            ),
        )

    def get(
        self,
        config: object | Callable[[Run], bool] | None = None,
        **kwargs,
    ) -> Run:
        """Retrieve a specific `Run` instance based on the provided configuration.

        This method filters the runs in the collection according to the
        specified configuration object and returns the run that matches the
        provided parameters. If no run matches the criteria, or if more than
        one run matches the criteria, a `ValueError` is raised.

        Args:
            config (object | Callable[[Run], bool] | None): The configuration object
                to identify the run. This can be any object that provides key-value
                pairs through the `iter_params` function, or a callable that
                takes a `Run` object and returns a boolean value.
            **kwargs: Additional key-value pairs to filter the runs.

        Returns:
            The `Run` instance that matches the provided configuration.

        Raises:
            ValueError: If no run matches the criteria or if more than one run
            matches the criteria.

        See Also:
            `filter`: Perform the actual filtering logic.

        """
        try:
            return self.filter(config, **kwargs).one()
        except ValueError:
            msg = "The filtered collection does not contain exactly one run."
            raise ValueError(msg)

    def try_get(
        self,
        config: object | Callable[[Run], bool] | None = None,
        **kwargs,
    ) -> Run | None:
        """Try to get a specific `Run` instance based on the provided configuration.

        This method filters the runs in the collection according to the
        specified configuration object and returns the run that matches the
        provided parameters. If no run matches the criteria, None is returned.
        If more than one run matches the criteria, a `ValueError` is raised.

        Args:
            config (object | Callable[[Run], bool] | None): The configuration object
                to identify the run. This can be any object that provides key-value
                pairs through the `iter_params` function, or a callable that
                takes a `Run` object and returns a boolean value.
            **kwargs: Additional key-value pairs to filter the runs.

        Returns:
            The `Run` instance that matches the provided configuration, or None
            if no runs match the criteria.

        Raises:
            ValueError: If more than one run matches the criteria.

        See Also:
            `filter`: Perform the actual filtering logic.

        """
        return self.filter(config, **kwargs).try_one()

    def get_param_names(self) -> list[str]:
        """Get the parameter names from the runs.

        This method extracts the unique parameter names from the provided list
        of runs. It iterates through each run and collects the parameter names
        into a set to ensure uniqueness.

        Returns:
            A list of unique parameter names.

        """
        param_names = set()

        for run in self:
            for param in run.data.params:
                param_names.add(param)

        return list(param_names)

    def get_param_dict(self, *, drop_const: bool = False) -> dict[str, list[str]]:
        """Get the parameter dictionary from the list of runs.

        This method extracts the parameter names and their corresponding values
        from the provided list of runs. It iterates through each run and
        collects the parameter values into a dictionary where the keys are
        parameter names and the values are lists of parameter values.

        Args:
            drop_const (bool): If True, drop the parameter values that are constant
                across all runs.

        Returns:
            A dictionary where the keys are parameter names and the values are
            lists of parameter values.

        """
        params = {}

        for name in self.get_param_names():
            it = (run.data.params[name] for run in self if name in run.data.params)
            unique_values = sorted(set(it))
            if not drop_const or len(unique_values) > 1:
                params[name] = unique_values

        return params

    def groupby(
        self,
        names: str | list[str],
    ) -> dict[str | None | tuple[str | None, ...], RunCollection]:
        """Group runs by specified parameter names.

        Group the runs in the collection based on the values of the
        specified parameters. Each unique combination of parameter values will
        form a key in the returned dictionary.

        Args:
            names (str | list[str]): The names of the parameters to group by.
                This can be a single parameter name or multiple names provided
                as separate arguments or as a list.

        Returns:
            dict[str | None | tuple[str | None, ...], RunCollection]: A
            dictionary where the keys are tuples of parameter values and the
            values are `RunCollection` objects containing the runs that match
            those parameter values.

        """
        grouped_runs: dict[str | None | tuple[str | None, ...], list[Run]] = {}
        is_list = isinstance(names, list)
        for run in self._runs:
            key = get_params(run, names)
            if not is_list:
                key = key[0]
            grouped_runs.setdefault(key, []).append(run)

        return {key: RunCollection(runs) for key, runs in grouped_runs.items()}

    def sort(
        self,
        *,
        key: Callable[[Run], Any] | None = None,
        reverse: bool = False,
    ) -> None:
        """Sort the runs in the collection.

        Sort the runs in the collection according to the provided key function
        and optional reverse flag.

        Args:
            key (Callable[[Run], Any] | None): A function that takes a run and returns
                a value to sort by.
            reverse (bool): If True, sort in descending order.

        """
        self._runs.sort(key=key or (lambda x: x.info.start_time), reverse=reverse)

    def values(self, names: str | list[str]) -> list[Any]:
        """Get the values of specified parameters from the runs.

        Args:
            names (str | list[str]): The names of the parameters to get the values.
                This can be a single parameter name or multiple names provided
                as separate arguments or as a list.

        Returns:
            A list of values for the specified parameters.

        """
        is_list = isinstance(names, list)

        if isinstance(names, str):
            names = [names]

        config = load_config(self.first())
        types = [type(v) for v in select_config(config, names).values()]
        values = [get_values(run, names, types) for run in self]

        if is_list:
            return values

        return [v[0] for v in values]

    def sorted(
        self,
        names: str | list[str],
        *,
        reverse: bool = False,
    ) -> RunCollection:
        """Sort the runs in the collection by specified parameter names.

        Sort the runs in the collection based on the values of the specified
        parameters.

        Args:
            names (str | list[str]): The names of the parameters to sort by.
                This can be a single parameter name or multiple names provided
                as separate arguments or as a list.
            reverse (bool): If True, sort in descending order.

        """
        values = self.values(names)
        index = sorted(range(len(self)), key=lambda i: values[i], reverse=reverse)
        return RunCollection([self[i] for i in index])


def _param_matches(run: Run, key: str, value: Any) -> bool:
    params = run.data.params
    if key not in params:
        return False

    param = params[key]
    if param == "None":
        return value is None or value == "None"

    return hydraflow.core.param.match(param, value)


def filter_runs(
    runs: list[Run],
    config: object | Callable[[Run], bool] | None = None,
    *,
    select: list[str] | None = None,
    overrides: list[str] | None = None,
    status: str | list[str] | int | list[int] | None = None,
    **kwargs,
) -> list[Run]:
    """Filter the runs based on the provided configuration.

    Filter the runs in the collection according to the
    specified configuration object and additional key-value pairs.
    The configuration object and key-value pairs should contain
    key-value pairs that correspond to the parameters of the runs.
    Only the runs that match all the specified parameters will
    be included in the returned list of runs.

    The filtering supports:
    - Exact matches for single values.
    - Membership checks for lists of values.
    - Range checks for tuples of two values (inclusive of both the lower and
      upper bound).

    Args:
        runs (list[Run]): The list of runs to filter.
        config (object | Callable[[Run], bool] | None, optional): The
            configuration object to filter the runs. This can be any object
            that provides key-value pairs through the `iter_params` function.
            This can also be a callable that takes a `Run` object and returns
            a boolean value. Defaults to None.
        select (list[str] | None, optional): The list of parameters to select.
            Defaults to None.
        overrides (list[str] | None, optional): The list of overrides to filter the
            runs. Defaults to None.
        status (str | list[str] | RunStatus | list[RunStatus] | None, optional): The
            status of the runs to filter. Defaults to None.
        **kwargs: Additional key-value pairs to filter the runs.

    Returns:
        A list of runs that match the specified configuration and key-value pairs.

    """
    if callable(config):
        runs = [run for run in runs if config(run)]

    else:
        if overrides:
            config = select_overrides(config, overrides)
        elif select:
            config = select_config(config, select)

        for key, value in chain(iter_params(config), kwargs.items()):
            runs = [run for run in runs if _param_matches(run, key, value)]
            if not runs:
                return []

    if status is None:
        return runs

    return filter_runs_by_status(runs, status)


def filter_runs_by_status(
    runs: list[Run],
    status: str | list[str] | int | list[int],
) -> list[Run]:
    """Filter the runs based on the provided status.

    Args:
        runs (list[Run]): The list of runs to filter.
        status (str | list[str] | int | list[int]): The status of the runs
            to filter.

    Returns:
        A list of runs that match the specified status.

    """
    from mlflow.entities import RunStatus

    if isinstance(status, str):
        if status.startswith("!"):
            status = status[1:].lower()
            return [run for run in runs if run.info.status.lower() != status]

        status = [status]

    elif isinstance(status, int):
        status = [RunStatus.to_string(status)]

    status = [_to_lower(s) for s in status]
    return [run for run in runs if run.info.status.lower() in status]


def _to_lower(status: str | int) -> str:
    from mlflow.entities import RunStatus

    if isinstance(status, str):
        return status.lower()

    return RunStatus.to_string(status).lower()
