"""
Support framework for fwlite processing. **EXPERIMENTAL!**
"""

import ROOT
import itertools
import subprocess
import time
import multiprocessing
import sys
import traceback
import os

from varial import diskio
from varial import wrappers


############################################ executed in parallel processes ###
class FwliteWorker(object):
    """Baseclass for fwlite jobs."""
    def __init__(self, name):
        self.name = name
        self.result = wrappers.FileServiceWrapper(name=name)

    def node_setup(self, event_handle_wrp):
        """Setup"""
        pass

    def node_process_event(self, event):
        """Process event"""
        pass

    def node_finalize(self, event_handle_wrp):
        """Finalize"""
        pass


def run_workers(event_handle_wrp):
    from DataFormats.FWLite import Events
    event_handle_wrp.event_handle = Events(event_handle_wrp.filenames)
    workers = event_handle_wrp.workers
    if not event_handle_wrp.event_handle.size():
        del event_handle_wrp.event_handle
        print "Skipping (no events): ", event_handle_wrp.filenames
        event_handle_wrp.results = []
        event_handle_wrp.workers = None
        return event_handle_wrp

    # setup workers
    for w in workers:
        try:
            w.node_setup(event_handle_wrp)
        except Exception as e:
            if not isinstance(e, KeyboardInterrupt):
                print '\nin node_setup:'
                traceback.print_exc(file=sys.stdout)
                print event_handle_wrp
                print '\n'
            raise e
        for v in w.result.__dict__.values():
            if isinstance(v, ROOT.TH1):
                v.SetDirectory(0)

    # run the eventloop
    def do_the_eventloop():
        for event in event_handle_wrp.event_handle:
            for w in workers:
                try:
                    w.node_process_event(event)
                except Exception as e:
                    if not isinstance(e, KeyboardInterrupt):
                        print '\nin node_process_event:'
                        traceback.print_exc(file=sys.stdout)
                        print event_handle_wrp
                        print '\n'
                    raise e
    if event_handle_wrp.event_handle.size():
        if _proxy and _proxy.do_profiling:
            print 'Running with cProfile: ', event_handle_wrp.filenames
            import cProfile
            cProfile.runctx(
                'do_the_eventloop()',
                globals(),
                locals(),
                "cProfile_%s_%s_.txt" % (
                    event_handle_wrp.sample,
                    "".join(event_handle_wrp.filenames[0].split('/'))
                )
            )
        else:
            do_the_eventloop()

    # finalize workers
    workers_with_result = []
    for w in workers[:]:
        try:
            w.node_finalize(event_handle_wrp)
        except Exception as e:
            if not isinstance(e, KeyboardInterrupt):
                print '\nin node_finalize:'
                traceback.print_exc(file=sys.stdout)
                print event_handle_wrp
                print '\n'
            raise e
        if not w.result.is_empty():
            workers_with_result.append(w)
            if hasattr(event_handle_wrp, 'sample'):
                w.result.sample = event_handle_wrp.sample
                w.result.id = '%s!%s' % (event_handle_wrp.sample, w.result.name)
            else:
                w.result.id = w.result.name

    event_handle_wrp.results = list(w.result for w in workers_with_result)
    del event_handle_wrp.workers
    del event_handle_wrp.event_handle
    return event_handle_wrp


############################################### executed in control process ###
_proxy = None
runner_py = """
import BTagDeltaR.Analysis.worker_vertexDR as wrkr
from varial import wrappers, diskio, fwliteworker
fwliteworker._proxy = wrappers.Wrapper(do_profiling = %s)
event_handle = diskio.read('in')
event_handle.workers = wrkr.workers
out = fwliteworker.run_workers(event_handle)
res = out.results
out.results = list(r.name for r in res)
for r in res:
    diskio.write(r)
diskio.write(out, 'out')
"""


def my_imap(func, event_handles):
    if os.path.exists('.py_confs'):
        os.system('rm -rf .py_confs')
    os.mkdir('.py_confs')

    waiting = list(event_handles)
    running = []

    def add_proc():
        hndl = waiting.pop(0)
        path = '.py_confs/%s_%s/' % (
            hndl.sample,
            hndl.filenames[0].replace("/", "_")[:-5]
        )
        os.mkdir(path)
        hndl.workers = None
        diskio.write(hndl, path + 'in')
        rnnr_py = runner_py
        rnnr_py %= 'True' if _proxy.do_profiling else 'False'
        with open(path + 'runner.py', 'w') as f:
            f.write(rnnr_py)
        running.append(
            (path, subprocess.Popen(
                ['python', 'runner.py'],
                cwd=os.getcwd()+'/'+path
            ))
        )

    def finish_proc(path):
        res = diskio.read(path + 'out')
        results = []
        for r in res.results:
            results.append(diskio.read(path + r))
            diskio.close_root_file(path + r)
        res.results = results
        time.sleep(0.01)
        if not _proxy.do_profiling:
            os.system('rm -rf %s' % path)
        return res

    while waiting or running:
        time.sleep(0.02)

        if waiting and len(running) < _proxy.max_num_processes:
            add_proc()

        for path, proc in running[:]:
            proc.poll()
            if None == proc.returncode:
                continue
            elif 0 == proc.returncode:
                running.remove((path, proc))
                yield finish_proc(path)
                break
            else:
                raise 'FAILED PROC, RETURNCODE: ' + str(proc.returncode)


def _add_results(event_handle_wrps):
    res_sums = {}
    for evt_hndl_wrp in event_handle_wrps:
        for new_res in evt_hndl_wrp.results:
            if new_res.id in res_sums:
                res_sum = res_sums[new_res.id]
                for k, v in new_res.__dict__.iteritems():
                    if isinstance(v, ROOT.TH1):
                        getattr(res_sum, k).Add(v)
            else:
                res_sums[new_res.id] = diskio.get(new_res.id, new_res)
        if _proxy:
            _proxy.results.update((r, True) for r in res_sums)
            if evt_hndl_wrp.sample in _proxy.files_done:
                f_done_dict = _proxy.files_done[evt_hndl_wrp.sample]
                f_done_dict[evt_hndl_wrp.filenames[0]] = True
            else:
                _proxy.files_done[evt_hndl_wrp.sample] = {
                    evt_hndl_wrp.filenames[0]: True
                }
            for res_sum in res_sums.values():
                diskio.write(res_sum, '.cache/' + res_sum.id)
            diskio.write(_proxy, '.cache/' + _proxy.name)
            os.system('mv .cache/* .')

    return res_sums


def work(workers, event_handles=None):
    global _proxy
    if not event_handles:
        _proxy = diskio.get('fwlite_proxy')
        if not _proxy:
            raise RuntimeError('You must either provide the event_handles '
                               'argument or fwlite_proxy.info in my cwd!')
        if os.path.exists('.cache'):
            os.system('rm -rf .cache')
        os.mkdir('.cache')

        def event_handle_gen():
            for sample, files in _proxy.event_files.iteritems():
                for f in files:
                    if sample in _proxy.files_done:
                        if f in _proxy.files_done[sample]:
                            continue
                    yield wrappers.Wrapper(
                        sample=sample,
                        filenames=[f],
                        workers=workers,
                    )

        event_handles = list(event_handle_gen())
    else:
        event_handles = (wrappers.Wrapper(
            event_handle=h_evt,
            filenames=h_evt._filenames,
        ) for h_evt in event_handles)

    if _proxy.max_num_processes > 1:
        results_iter = multiprocessing.Pool(
            _proxy.max_num_processes
        ).imap_unordered(run_workers, event_handles)
    else:
        results_iter = itertools.imap(run_workers, event_handles)

    results_iter = my_imap(None, event_handles)

    return _add_results(results_iter)
