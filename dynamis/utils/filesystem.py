import shutil
import tempfile
import contextlib


@contextlib.contextmanager
def tempdir():
    _dir = tempfile.mkdtemp()
    try:
        yield _dir
    except:
        shutil.rmtree(_dir, ignore_errors=True)
        raise
    else:
        shutil.rmtree(_dir, ignore_errors=True)
