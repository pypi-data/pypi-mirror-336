from ewokscore.tests.examples.graphs import get_graph
from ..client import celery
from ..client import local
from .utils import get_result


def test_submit(ewoks_worker):
    assert_submit(celery)
    assert_submit_test(celery)


def test_submit_local(local_ewoks_worker):
    assert_submit(local)
    assert_submit_test(local)


def assert_submit(mod):
    graph, expected = get_graph("acyclic1")
    expected = expected["task6"]
    future1 = mod.submit(args=(graph,))
    future2 = mod.get_future(future1.task_id)
    results = get_result(future1, timeout=60)
    assert results == expected
    results = get_result(future2, timeout=0)
    assert results == expected


def assert_submit_test(mod):
    future1 = mod.submit_test()
    future2 = mod.get_future(future1.task_id)
    results = get_result(future1, timeout=60)
    assert results == {"return_value": True}
    results = get_result(future2, timeout=0)
    assert results == {"return_value": True}
