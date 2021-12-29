"""
Read/Write wrappers to disk.

On disk, a wrapper is represented by a .info file. If it contains root objects,
there's a .root file with the same name in the same directory.
"""

import settings  #  init ROOT first

from ROOT import TFile, TDirectory, TH1, TObject, TTree
from os.path import basename, dirname, join
from itertools import takewhile
from ast import literal_eval
import resource
import glob
import os

import wrappers
import history
import monitor


_n_file_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
try:
    resource.setrlimit(resource.RLIMIT_NOFILE, (_n_file_limit, _n_file_limit))
except ValueError:
    pass


class NoDictInFileError(RuntimeError): pass
class NoObjectError(RuntimeError): pass
class NoHistogramError(RuntimeError): pass


################################################################# file refs ###
class _BlockMaker(object):
    def __enter__(self):
        global _in_a_block
        _in_a_block += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _in_a_block
        _in_a_block -= 1
        if not _in_a_block:
            for filename in _block_of_open_files:
                file_handle = _open_root_files.pop(filename, 0)
                if file_handle:
                    file_handle.Close()


_open_root_files = {}
_block_of_open_files = []
_in_a_block = 0  # number of opened blocks
block_of_files = _BlockMaker()


def get_open_root_file(filename):
    if filename in _open_root_files:
        file_handle = _open_root_files[filename]
    else:
        if len(_open_root_files) > settings.max_open_root_files:
            monitor.message(
                'diskio',
                'WARNING to many open root files. Closing all. '
                'Please check for lost histograms. '
                '(Use hist.SetDirectory(0) to keep them)'
            )
            close_open_root_files()
        file_handle = TFile.Open(filename, 'READ')
        if (not file_handle) or file_handle.IsZombie():
            raise RuntimeError('Cannot open file with root: "%s"' % filename)
        _open_root_files[filename] = file_handle
        if _in_a_block:
            _block_of_open_files.append(filename)
    return file_handle


def close_open_root_files():
    for name, file_handle in _open_root_files.iteritems():
        file_handle.Close()
    _open_root_files.clear()


def close_root_file(filename):
    if not filename[-5:] == '.root':
        filename += '.root'
    if filename in _open_root_files:
        _open_root_files[filename].Close()
        del _open_root_files[filename]


##################################################### read / write wrappers ###
def exists(filename):
    """Checks for existance."""
    filename = prepare_basename(filename)
    return os.path.exists('%s.info' % filename)


def read(filename):
    """Reads wrapper from disk, including root objects."""
    filename = prepare_basename(filename) + '.info'
    with open(filename) as f:
        try:
            info = _read_wrapper_info(f)
        except ValueError as e:
            monitor.message(
                'diskio.read',
                'ERROR can not read info: ' + filename
            )
            raise e

    if 'root_filename' in info:
        _read_wrapper_objs(info, dirname(filename))
    klass = getattr(wrappers, info.get('klass'))
    if klass == wrappers.WrapperWrapper:
        p = dirname(filename)
        info['wrps'] = _read_wrapperwrapper(
            join(p, f)
            for f in info['wrpwrp_names']
        )
    wrp = klass(**info)
    _clean_wrapper(wrp)
    return wrp


def write(wrp, filename=None, suffices=(), mode='RECREATE'):
    """Writes wrapper to disk, including root objects."""
    filename = prepare_basename(filename or wrp.name)
    if mode is not 'UPDATE':
        record_in_save_log(filename)

    if settings.diskio_check_readability:
        _check_readability(wrp)
    # save with suffices
    for suffix in suffices:
        wrp.obj.SaveAs(filename + suffix)
    # WrapperWrapper: store others first
    if isinstance(wrp, wrappers.WrapperWrapper):
        _write_wrapperwrapper(wrp, filename)
    # write root objects (if any)
    if any(isinstance(o, TObject) for o in wrp.__dict__.itervalues()):
        wrp.root_filename = basename(filename+'.root')
        f = TFile.Open(filename+'.root', mode)
        f.cd()
        _write_wrapper_objs(wrp, f)
        f.Close()
    # write wrapper infos
    with open(filename+'.info', 'w') as f:
        _write_wrapper_info(wrp, f)
    _clean_wrapper(wrp)


def small_write(wrp, filename, suffices=()):
    """Writes only according to the given suffices and the wrp info."""
    filename = prepare_basename(filename)
    record_in_save_log(filename)
    with open(filename+'.info', 'w') as f:
        _write_wrapper_info(wrp, f)
    for suffix in suffices:
        wrp.obj.SaveAs(filename + suffix)


def get(filename, default=None):
    """Reads wrapper from disk if availible, else returns default."""
    try:
        return read(filename)
    except (RuntimeError, IOError):
        return default


########################################################## i/o with aliases ###
def generate_aliases(glob_path='./*.root'):
    """Looks for root files based on a pattern string and produces aliases."""
    file_paths = glob.glob(glob_path)
    return generate_aliases_list(file_paths)


def generate_aliases_list(list_of_files=('',)):
    """Looks for root files based on a list and produces aliases."""
    for file_path in list_of_files:
        if type(file_path) is not str:
            raise RuntimeError(
                'diskio.generate_aliases_list needs a list of strings')
        root_file = get_open_root_file(file_path)
        for ifp, typ in _recursive_path_and_type(root_file, ''):
            yield wrappers.Alias(file_path, ifp, typ)


def load_bare_object(alias):
    return _get_obj_from_file(
        alias.file_path,
        alias.in_file_path
    )


def load_histogram(alias):
    """Returns a wrapper with a fileservice histogram."""
    histo = load_bare_object(alias)
    return _wrapperize(histo, alias)


def bulk_load_histograms(aliases):
    """Returns a list of wrappers with fileservice histograms."""
    # todo with(SyncReadIo(timeout)): for the next statement
    histos = list((load_bare_object(a), a) for a in aliases)
    histos = list(_wrapperize(h, a) for h, a in histos)
    return histos


########################################################## helper functions ###
use_analysis_cwd = True
_save_log = set()


def prepare_basename(filename):
    if use_analysis_cwd:
        filename = join(analysis.cwd, filename)
    if filename[-5:] == '.info':
        filename = filename[:-5]
    return filename


def record_in_save_log(filename):
    if filename in _save_log:
        monitor.message(
            'diskio',
            'WARNING Overwriting file from this session: %s' % filename
        )
    else:
        _save_log.add(filename)


def _write_wrapper_info(wrp, file_handle):
    #"""Serializes Wrapper to python code dict."""
    if hasattr(wrp, 'history'):
        history, wrp.history = wrp.history, str(wrp.history)
        file_handle.write(wrp.pretty_writeable_lines() + ' \n\n')
        file_handle.write(wrp.history + '\n')
        wrp.history = history
    else:
        file_handle.write(wrp.pretty_writeable_lines() + ' \n\n')


def _write_wrapper_objs(wrp, file_handle):
    #"""Writes root objects on wrapper to disk."""
    wrp.root_file_obj_names = {}
    if isinstance(wrp, wrappers.FileServiceWrapper):
        dirfile = file_handle.Get(wrp.name) or file_handle.mkdir(wrp.name, wrp.name)
        dirfile.cd()
        for key, value in wrp.__dict__.iteritems():
            if not isinstance(value, TObject):
                continue
            value.Write()
            wrp.root_file_obj_names[key] = value.GetName()
        dirfile.Close()
    else:
        for key, value in wrp.__dict__.iteritems():
            if not isinstance(value, TObject):
                continue
            dirfile = file_handle.mkdir(key, key)
            dirfile.cd()
            value.Write()
            dirfile.Close()
            wrp.root_file_obj_names[key] = value.GetName()


def _write_wrapperwrapper(wrp, filename=None):
    global use_analysis_cwd
    if not filename:
        filename = wrp.name
    wrp_names = []
    for i, w in enumerate(wrp.wrps):
        name = filename + '_WRPWRP_%03d' % i
        wrp_names.append(basename(name))
        with_ana_cwd = use_analysis_cwd
        try:
            use_analysis_cwd = False  # write should not prepend cwd again
            write(w, name)
        finally:
            use_analysis_cwd = with_ana_cwd  # reset
    wrp.wrpwrp_names = wrp_names
    wrp._wrpwrp_wrps = wrp.wrps
    del wrp.wrps


def _read_wrapper_info(file_handle):
    #"""Instaciates Wrapper from info file, without root objects."""
    lines = takewhile(lambda l: l!='\n', file_handle)
    lines = (l.strip() for l in lines)
    lines = ''.join(lines)
    info = literal_eval(lines)
    if not type(info) == dict:
        raise NoDictInFileError('Could not read file: '+file_handle.name)
    return info


def _read_wrapper_objs(info, path):
    #"""Reads root objects from disk."""
    root_file = join(path, info['root_filename'])
    obj_paths = info['root_file_obj_names']
    is_fs_wrp = info['klass'] == 'FileServiceWrapper'
    for key, value in obj_paths.iteritems():
        if is_fs_wrp:
            obj = _get_obj_from_file(root_file, info['name'] + '/' + value)
        else:
            obj = _get_obj_from_file(root_file, key + '/' + value)
        if hasattr(obj, 'SetDirectory'):
            obj.SetDirectory(0)
        info[key] = obj


def _read_wrapperwrapper(wrp_list):
    wrps = []
    for fname in wrp_list:
        wrps.append(read(fname))
    return wrps


def _clean_wrapper(wrp):
    del_attrs = ['root_filename',
                 'root_file_obj_names',
                 'wrapped_object_key'
                 'wrpwrp_names']
    for attr in del_attrs:
        if hasattr(wrp, attr):
            delattr(wrp, attr)

    if hasattr(wrp, '_wrpwrp_wrps'):
        wrp.wrps = wrp._wrpwrp_wrps
        del wrp._wrpwrp_wrps


def _check_readability(wrp):
    try:
        literal_eval(wrp.pretty_writeable_lines().replace('\n', ''))
    except (ValueError, SyntaxError):
        monitor.message(
            'diskio.write',
            'WARNING Wrapper will not be readable:\n%s' % str(wrp)
        )


def _get_obj_from_file(filename, in_file_path):
    obj = get_open_root_file(filename)
    # browse through file
    for name in in_file_path.split('/'):
        obj_key = obj.GetKey(name)
        if not obj_key:
            raise NoObjectError(
                'I cannot find "%s" in root file "%s"!' % (in_file_path,
                                                           filename))
        obj = obj_key.ReadObj()
    return obj


def _recursive_path_and_type(root_dir, in_file_path):
    for key in root_dir.GetListOfKeys():
        if in_file_path:
            key_path = in_file_path + '/' + key.GetName()
        else:
            key_path = key.GetName()
        if key.IsFolder():
            obj = key.ReadObj()
            if isinstance(obj, TTree):
                continue
            for info in _recursive_path_and_type(
                obj,
                key_path
            ):
                yield info
        else:
            yield key_path, key.GetClassName()


def _wrapperize(bare_histo, alias):
    """Returns a wrapper with a fileservice histogram."""
    if not isinstance(bare_histo, TH1):
        raise NoHistogramError(
            'Loaded object is not of type TH1.\n'
            'Alias: %s\nObject: %s\n' % (alias, bare_histo)
        )
    if not bare_histo.GetSumw2().GetSize():
        bare_histo.Sumw2()
    wrp = wrappers.HistoWrapper(bare_histo, **alias.all_info())
    if isinstance(alias, wrappers.FileServiceAlias):
        bare_histo.SetTitle(alias.legend)
        wrp.history = history.History(
            'FileService(%s, %s)' % (
                alias.in_file_path, alias.sample))
    else:
        info = alias.all_writeable_info()
        del info['klass']
        wrp.history = history.History(
            'RootFile(%s)' % info
        )
    return wrp


################################################### write and close on exit ###
import multiproc
import analysis
import atexit


multiproc.pre_fork_cbs.append(close_open_root_files)
multiproc.pre_join_cbs.append(close_open_root_files)


def write_fileservice(filename='', initial_mode='RECREATE'):
    if not analysis.fs_wrappers:
        return

    filename = filename or settings.fileservice_filename
    fs_wrappers = analysis.fs_wrappers.values()
    write(fs_wrappers[0], filename=filename, mode=initial_mode)
    for wrp in fs_wrappers[1:]:
        write(wrp, filename=filename, mode='UPDATE')

    analysis.fs_wrappers = {}


atexit.register(write_fileservice)
atexit.register(close_open_root_files)


# TODO read and write should only call utility methods (see ugly wrpwrp writing)
# TODO synchronized/buffered write with multiprocessing.Manager object
# TODO bulk_read(aliases) function => all reading en block, with possible lock
# TODO context manager for use_analysis_cwd (maybe general util)
# TODO get rid of use_analysis_cwd. It's bad design.
