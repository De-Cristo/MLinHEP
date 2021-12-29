"""
Management for multiprocessing in varial.

WorkerPool creates child processes that do not daemonize. Therefore they can
spawn further children, which is handy to parallelize at many levels (e.g. run
parallel tools at every level of a complex directory structure). Nevertheless,
only a given number of workers runs at the same time, thus keeping the processes
from dead-locking resources.
Exceptions from the worker processes are passed to the host process.

When using this module it is important to watch memory consumption! Every
spawned process is copied in memory. It is best to load data within a worker,
not in the host process.

Example usage:

>>> import varial.multiproc
>>>
>>> my_input_list = [1,2,3,4]
>>> n_workers = min(varial.settings.max_num_processes, len(my_input_list))
>>>
>>> def my_square(num):
>>>     return num*num
>>>
>>> with varial.multiproc.WorkerPool(n_workers) as pool:
>>>     for res in pool.imap_unordered(my_square, my_input_list):
>>>         print res

Note that in the example, the input and output data of the worker is just an
int. If large amounts of data need to be transferred, it is better to let the
worker store the data on disk and read it back in the host.
"""

import multiprocessing.pool
import settings
import sys

_cpu_semaphore = None
_traceback_printlock = None  # this is never released (only print once)
pre_fork_cbs = []
pre_join_cbs = []


############################## errors handling: catch and raise on hostside ###
def _catch_exception_in_worker(func, *args, **kws):
    try:
        res = func(*args, **kws)

    # TODO: write SIGINT handler and kill again
    except KeyboardInterrupt as e:
        res = 'Exception', e

    except Exception as e:
        res = 'Exception', e
        if _traceback_printlock.acquire(block=False):
            import traceback
            tb = ''.join(traceback.format_exception(*sys.exc_info()))
            print '='*80
            print 'EXCEPTION IN PARALLEL EXECUTION START'
            print '='*80
            print tb
            print '='*80
            print 'EXCEPTION IN PARALLEL EXECUTION END'
            print '='*80

    return res


def _gen_raise_exception_in_host(iterator):
    for i in iterator:
        if isinstance(i, tuple) and i and i[0] == 'Exception':
            raise i[1]
        else:
            yield i


def _exec_in_worker(func_and_item):
    """parallel execution with cpu control and exception catching."""

    with _cpu_semaphore:
        return _catch_exception_in_worker(*func_and_item)


################################ special worker-pool to allow for recursion ###
class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

    def run(self):
        try:
            super(NoDaemonProcess, self).run()
        except (KeyboardInterrupt, IOError):
            exit(-1)


class WorkerPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

    def __init__(self, *args, **kws):
        global _cpu_semaphore, _traceback_printlock

        # prepare parallelism (only once for the all processes)
        self.me_created_semaphore = False
        if _cpu_semaphore:
            # process with pool is supposed to be waiting a lot
            _cpu_semaphore.release()
        else:
            self.me_created_semaphore = True
            n_procs = settings.max_num_processes
            _cpu_semaphore = multiprocessing.BoundedSemaphore(n_procs)
            _traceback_printlock = multiprocessing.RLock()

        for func in pre_fork_cbs:
            func()

        # go parallel
        super(WorkerPool, self).__init__(*args, **kws)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.join()

    def imap_unordered(self, func, iterable, chunksize=1):
        iterable = ((func, i) for i in iterable)
        res = super(WorkerPool, self).imap_unordered(
            _exec_in_worker, iterable, chunksize
        )
        res = _gen_raise_exception_in_host(res)
        return res

    def close(self):
        global _cpu_semaphore, _traceback_printlock

        for func in pre_join_cbs:
            func()

        if self.me_created_semaphore:
            _cpu_semaphore = None
            _traceback_printlock = None
        else:
            # must re-acquire before leaving
            _cpu_semaphore.acquire()

        super(WorkerPool, self).close()
