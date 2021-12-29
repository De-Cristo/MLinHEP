#!/usr/bin/env python

##################################### definition of UserConfig item changes ###

cfg_filename = '/path/to/the/sframe/config.xml'

sys_uncerts = {
    # 'name' : {'item name': 'item value', ...},
    'jec_up'        : {'jecsmear_direction':'up'},
    'jec_down'      : {'jecsmear_direction':'down'},
    'jer_up'        : {'jersmear_direction':'up'},
    'jer_down'      : {'jersmear_direction':'down'},
    # 'jer_jec_up'    : {'jersmear_direction':'up','jecsmear_direction':'up'},
    # 'jer_jec_down'  : {'jersmear_direction':'down','jecsmear_direction':'down'},
}

start_all_parallel = True

use_sframe_batch = True

sframe_batch_conf = """
<!--
   <ConfigParse NEventsBreak="100000" FileSplit="0" AutoResubmit="0" />
   <ConfigSGE RAM="2" DISK="2" Mail="my_mail@desy.de" Notification="as" Workdir="workdir"/>
-->
"""


############################################################### script code ###
from varial.extensions.sframe import SFrame
from varial import tools
import os


def set_uncert_func(uncert_name):
    """Change parameters in the sframe config"""
    uncert = sys_uncerts[uncert_name]
    def do_set_uncert(element_tree):
        cycle = element_tree.getroot().find('Cycle')
        user_config = cycle.find('UserConfig')
        output_dir = cycle.get('OutputDirectory')
        cycle.set('OutputDirectory', os.path.join(output_dir, uncert_name))

        for name, value in uncert.iteritems():
            uc_item = list(i for i in user_config if i.get('Name') == name)
            assert uc_item, 'could not find item with name: %s' % name
            uc_item[0].set('Value', value)

    return do_set_uncert


class SFrameBatch(SFrame):
    """Run sframe_batch.py instead of sframe_main"""
    def configure(self):
        self.xml_doctype = self.xml_doctype + sframe_batch_conf
        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt


if start_all_parallel:
    n_workers = None  # auto-adjust number of workers
else:
    n_workers = 1

if use_sframe_batch:
    SFrame = SFrameBatch


sframe_tools = tools.ToolChainParallel(
    'SFrameUncerts',
    list(
        SFrame(
            cfg_filename=cfg_filename,
            xml_tree_callback=set_uncert_func(uncert),
            name='SFrame_' + uncert,
            halt_on_exception=False,
        )
        for uncert in sys_uncerts
    ),
    n_workers=n_workers,
)


if __name__ == '__main__':
    tools.Runner(sframe_tools)
