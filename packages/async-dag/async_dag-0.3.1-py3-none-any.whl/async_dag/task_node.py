from collections.abc import Awaitable, Callable, Sequence
from typing import TYPE_CHECKING, cast

from .execution_result import ExecutionResult
from .state import State

if TYPE_CHECKING:
    from .task_manager import TaskManager


class TaskNode[_ParameterType, _ReturnType]:
    """
    `TaskNode` represents a task in the DAG.
    The only API you should use in this class is the `extract_result` method.
    **You should never initialize this class by yourself!**
    """

    def __init__(
        self,
        callback: Callable[..., Awaitable[_ReturnType]],
        task_manager: "TaskManager[_ParameterType]",
        dependencies_ids: Sequence[int],
        node_id: int,
    ) -> None:
        self._task_manager = task_manager
        self._dependencies_ids = dependencies_ids
        self._callback = callback
        self._state = State.UNDISCOVERED
        self._depth = 0
        self._id = node_id
        self._dependents_ids: set[int] = set()

    def extract_result(
        self, execution_result: ExecutionResult[_ParameterType]
    ) -> _ReturnType:
        """
        Returns the value that the `callback` of the task returned for a specific `TaskManager.invoke` call represented by the `execution_result` parameter.

        This function raises a `ValueError` if:
        1. It was called before `TaskManager.sort()` was called.
        2. the `execution_result` passed to it was from a different `TaskManager` then the one that created this node.
        """
        self._assert_state(State.PERMANENT)
        self._assert_task_manager(execution_result._task_manager)

        return cast(_ReturnType, execution_result._results[self._id])

    async def _invoke(
        self,
        execution_result: ExecutionResult[_ParameterType],
    ) -> _ReturnType:
        self._assert_state(State.PERMANENT)
        self._assert_task_manager(execution_result._task_manager)

        return await self._callback(
            *[execution_result._results[dep_id] for dep_id in self._dependencies_ids],
        )

    def _assert_state(self, expected_state: State) -> None:
        if self._state != expected_state:
            raise ValueError(
                f"TaskNode in invalid state, current state: {self._state}, expected state: {expected_state}"
            )

    def _assert_task_manager(self, task_manager: "TaskManager[_ParameterType]") -> None:
        if self._task_manager is not task_manager:
            raise ValueError(
                f"Task manager mismatch, expected: {self._task_manager} but got: {task_manager}"
            )
