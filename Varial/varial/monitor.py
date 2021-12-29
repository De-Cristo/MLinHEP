"""
Interface for system outputs.
"""

import settings
import time
import sys


current_error_level = 0
error_levels = {
    'DEBU': -1,
    'INFO': 0,
    'WARN': 1,
    'ERRO': 2,
    'FATA': 3
}
color_levels = {
    'INFO': '\x1B[33m',
    'WARN': '\x1B[31m',
    'ERRO': '\x1B[41m',
    'FATA': '\x1B[41m',
}
reset_col = '\x1B[0m'


class Messenger(object):
    #"""Message stub. Used to connect to monitor module."""
    def __init__(self, connected_obj):
        super(Messenger, self).__init__()
        self.connected_obj = connected_obj

    def __call__(self, message_obj):
        message(self.connected_obj, message_obj)

    def started(self):
        started(self.connected_obj, "INFO started")

    def finished(self):
        finished(self.connected_obj, "INFO finished")


class MonitorInfo(object):
    indent = 0
    n_procs = 0
    error_logs_opened = 0
    outstream = sys.stdout
_info = MonitorInfo()


class StdOutTee(object):
    def __init__(self, logfilename):
        self.logfile = open(logfilename, "w")

    def __del__(self):
        self.logfile.close()

    def __getattr__(self, item):
        return getattr(sys.__stdout__, item)

    def write(self, string):
        sys.__stdout__.write(string)
        self.logfile.write(string)

    def flush(self):
        sys.__stdout__.flush()
        self.logfile.flush()

    def close(self):
        sys.__stdout__.close()
        self.logfile.close()


def write_out(*args):
    message = ' '.join(str(a) for a in args)
    token = message.replace(' ', '')[:4]
    if error_levels.get(token, 0) >= current_error_level:
        col = color_levels.get(token, '')
        _info.outstream.write(col + message + reset_col)
        _info.outstream.write('\n')


def proc_enqueued(process):
    write_out(
        "INFO process enqueued:   cmsRun ",
        process.conf_filename
    )


def proc_started(process):
    write_out(
        "INFO process started  %s:   cmsRun " % time.ctime(),
        process.conf_filename,
        "PID: ",
        process.subprocess.pid
    )


def proc_finished(process):
    if settings.recieved_sigint:
        write_out(
            "INFO process aborted %s:   cmsRun " % time.ctime(),
            process.conf_filename
        )
    else:
        write_out(
            "INFO process finished %s:   cmsRun " % time.ctime(),
            process.conf_filename
        )


def proc_failed(process):
    write_out(
        "WARNING process FAILED %s  :   cmsRun " % time.ctime(),
        process.conf_filename
    )
    if not _info.error_logs_opened:
        write_out("_______________________________________begin_cmsRun_logfile")
        with open(process.log_filename, "r") as logfile:
            write_out(logfile.read())
        write_out("______________end of log for %s" % process.conf_filename)
        write_out("_________________________________________end_cmsRun_logfile")
        _info.error_logs_opened += 1


def started(obj, message_obj):
    message(obj, message_obj)
    _info.indent += 2


def message(sender, string):
    """
    Send a logmessage.

    :param sender:  str or Tool instance
    :param string:  str, message string
    """
    if hasattr(sender, "name"):
        sender = sender.name
    elif not type(sender) == str:
        sender = str(type(sender))
    write_out(_info.indent*"  " + '%s (%s)' % (str(string), sender))


def finished(obj, message_obj):
    _info.indent -= 2
    message(obj, message_obj)


def connect_object_with_messenger(obj):
    obj.messenger = Messenger(obj)
    return obj.messenger


def reset():
    _info.indent = 0


class ErrorLevelContext(object):
    def __init__(self, new_error_level):
        super(ErrorLevelContext, self).__init__()
        self.old_error_level = current_error_level
        self.new_error_level = new_error_level

    def __enter__(self):
        global current_error_level
        current_error_level = self.new_error_level

    def __exit__(self, exc_type, exc_val, exc_tb):
        global current_error_level
        current_error_level = self.old_error_level
        return exc_type, exc_val, exc_tb
