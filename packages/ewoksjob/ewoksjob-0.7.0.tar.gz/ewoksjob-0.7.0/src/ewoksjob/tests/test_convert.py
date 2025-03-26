from ..client import celery
from ..client import local
from .utils import get_result


def test_convert(ewoks_worker, tmpdir):
    assert_convert(celery, tmpdir)


def test_convert_local(local_ewoks_worker, tmpdir):
    assert_convert(local, tmpdir)


def assert_convert(mod, tmpdir):
    filename = tmpdir / "test.json"
    args = {"graph": {"id": "testgraph", "schema_version": "1.0"}}, str(filename)
    kwargs = {"save_options": {"indent": 2}}
    future = mod.convert_graph(args=args, kwargs=kwargs)
    results = get_result(future, timeout=60)
    assert results == str(filename) or results is None  # TODO: None is deprecated
    assert filename.exists()
