"""
``zip`` analysis contents.
"""

import os

from varial.toolinterface import Tool
from varial import settings


class ZipTool(Tool):
    """
    Zip-compress a target folder.

    :param abs_path:    str, absolute path of tool to be zipped
    """
    def __init__(self, abs_path):
        super(ZipTool, self).__init__(None)
        self.abs_path = abs_path

    def run(self):
        p = os.path.join(settings.varial_working_dir, self.abs_path)
        os.system(
            'zip -r %s %s' % (p, p)
        )





