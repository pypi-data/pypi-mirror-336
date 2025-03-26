from typing import List
from concurrent.futures import Future
from .pool import get_active_pool


__all__ = [
    "get_future",
    "cancel",
    "get_result",
    "get_not_finished_task_ids",
    "get_not_finished_futures",
]


def get_future(task_id) -> Future:
    pool = get_active_pool()
    return pool.get_future(task_id)


def cancel(task_id):
    """The current implementation does not allow cancelling running tasks"""
    future = get_future(task_id)
    future.cancel()


def get_result(task_id, **kwargs):
    future = get_future(task_id)
    return future.result(**kwargs)


def get_not_finished_task_ids() -> list:
    """Get all task ID's that are not finished"""
    pool = get_active_pool()
    return pool.get_not_finished_task_ids()


def get_not_finished_futures() -> List[Future]:
    """Get all futures that are not finished"""
    return [get_future(task_id) for task_id in get_not_finished_task_ids()]
