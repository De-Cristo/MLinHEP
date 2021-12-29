"""
Store wrappers into a pkl object for every directory.

Please checkout the :ref:`diskio-module` documentation for more information.
"""

import cPickle
import os

import analysis
import monitor


_current_path = ''
_current_pack = {}
_changed = False
use_analysis_cwd = True


def _write_out():
    global _current_path, _current_pack, _changed

    if not _changed:
        return

    with open(os.path.join(_current_path, 'data.pkl'), 'w') as f:
        cPickle.dump(_current_pack, f)

    _changed = False


def _sync(path):
    global _current_path, _current_pack, _changed

    if use_analysis_cwd:
        path = os.path.join(analysis.cwd, path)

    if path == _current_path:
        return

    # write out and load if possible
    _write_out()
    _current_path = path
    data_path = os.path.join(_current_path, 'data.pkl')
    if not os.path.exists(data_path):
        _current_pack = {}
    else:
        with open(data_path) as f:
            try:
                _current_pack = cPickle.load(f)
            except Exception as e:
                msg = 'ERROR with file: %s' % data_path
                e.message += msg
                monitor.message('pklio', msg)
                raise
            assert isinstance(_current_pack, dict), 'path: %s' % data_path


class _BlockMaker(dict):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        _write_out()


block_of_files = _BlockMaker()


##################################################### read / write wrappers ###
def exists(name):
    """Check if data exists."""
    _sync(os.path.dirname(name))
    return name in _current_pack


def write(wrp, name=None):
    """Write a wrapper."""
    global _current_pack, _changed
    _sync(os.path.dirname(name or '_'))
    _changed = True
    _current_pack[name or wrp.name] = wrp


def read(name):
    """Read a wrapper."""
    _sync(os.path.dirname(name))
    wrp = _current_pack.get(os.path.basename(name))
    if wrp:
        return wrp
    else:
        raise RuntimeError('Data not found in: %s' % _current_path)


def get(name, default=None):
    """Reads wrapper if availible, else returns default."""
    try:
        return read(name)
    except RuntimeError:
        return default


################################################### write and close on exit ###
import atexit
atexit.register(_write_out)
