"""
Call ``make`` in an analysis.
"""

import subprocess
import random
import os

from varial.toolinterface import Tool


class Make(Tool):
    """
    Calls make in the directories given in paths.

    If compilation was needed (i.e. the output of make was different from
    "make: Nothing to be done for `all'") wanna_reuse will return False and
    by that cause all following modules to run.

    :param paths:   list of str: paths where make should be invoked
    """
    nothing_done = 'make: Nothing to be done for `all\'.\n'

    def __init__(self, paths):
        super(Make, self).__init__()
        self.paths = paths

    def wanna_reuse(self, all_reused_before_me):
        nothing_compiled_yet = True
        for path in self.paths:
            self.message('INFO Compiling in: ' + path)
            # here comes a workaround: we need to examine the output of make,
            # but want to stream it directly to the console as well. Hence use
            # tee and look at the output after make finished.
            tmp_out = '/tmp/varial_compile_%06i' % random.randint(0, 999999)
            res = subprocess.call(
                # PIPESTATUS is needed to get the returncode from make
                ['make -j 9 | tee %s; test ${PIPESTATUS[0]} -eq 0' % tmp_out],
                cwd=path,
                shell=True,
            )
            if res:
                os.remove(tmp_out)
                raise RuntimeError('Compilation failed in: ' + path)
            if nothing_compiled_yet:
                with open(tmp_out) as f:
                    if not f.readline() == self.nothing_done:
                        nothing_compiled_yet = False
            os.remove(tmp_out)

        return nothing_compiled_yet and all_reused_before_me

    def run(self):
        pass


# TODO: use 'make -n' in wanna_reuse and run compilation in 'run' method.