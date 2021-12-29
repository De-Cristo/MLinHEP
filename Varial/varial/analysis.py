"""
All analysis specific information is kept here.

This module has data members that can be accessed from the outside:

=============== ===============================================================
all_samples     dict(str => sample instance)
active_samples  list of str.
                These samples are *active*, which means that certain functions,
                e.g. for stacking histograms, will only select histograms from
                these samples. Thus, sets of systematic samples can be treated
                consistently.
cwd             str
                current working directory (set by the tool that's currently
                active)
=============== ===============================================================
"""
import os


################################################################### samples ###
import settings
import wrappers
active_samples = []  # list of samplenames
all_samples = {}
data_lumi_sum_value = None

def samples():
    """Returns a dict of all MC samples."""
    return dict(
        (k, v)
        for k, v in all_samples.iteritems()
        if k in active_samples
    )


def mc_samples():
    """Returns a dict of all MC samples."""
    return dict(
        (k, v)
        for k, v in all_samples.iteritems()
        if k in active_samples and not v.is_data
    )


def data_samples():
    """Returns a dict of all real data samples."""
    return dict(
        (k, v)
        for k, v in all_samples.iteritems()
        if k in active_samples and v.is_data
    )


def data_lumi_sum():
    """Returns the sum of luminosity in data samples."""
    global data_lumi_sum_value
    if data_lumi_sum_value == None:
        data_lumi_sum_value = float(sum(
            v.lumi
            for k, v in data_samples().iteritems()
            if k in active_samples
        ))
    return data_lumi_sum_value or settings.default_data_lumi


def data_lumi_sum_wrp():
    """Returns the sum of data luminosity in as a FloatWrapper."""
    lumi = data_lumi_sum()
    return wrappers.FloatWrapper(lumi, history='DataLumiSum(%g)' % lumi)


def get_pretty_name(key):
    """Utility function for re-labeling stuff."""
    return settings.pretty_names.get(key, key)


def get_color(sample_or_legend_name, samplename=None, default=0):
    """Returns a ROOT color value for sample or legend name."""
    name = sample_or_legend_name
    if name in all_samples:
        name = all_samples[name].legend
    if name in settings.colors:
        return settings.colors[name]
    if samplename in settings.colors:
        return settings.colors[samplename]
    if default:
        return default
    new_color = None
    used_colors = settings.colors.values()
    for col in settings.default_colors:
        if col not in used_colors:
            new_color = col
            break
    if not new_color:
        new_color = settings.default_colors[
            len(settings.colors) % len(settings.default_colors)
        ]
    settings.colors[name] = new_color
    return new_color


def get_stack_position(wrp):
    """Returns the stacking position (sortable str)"""

    def comparable_str(s):
        # reverse...
        pos = len(settings.stacking_order) - settings.stacking_order.index(s)
        # need comparable string that sorts before alpha chars
        return str(pos * 0.001)

    if wrp.legend in settings.stacking_order:
        res = comparable_str(wrp.legend)

    elif wrp.sample in settings.stacking_order:
        res = comparable_str(wrp.sample)

    elif (wrp.sample in all_samples and
          all_samples[wrp.sample].legend in settings.stacking_order):
        res = comparable_str(all_samples[wrp.sample].legend)

    else:
        res = wrp.legend

    return res + ('__' + wrp.sys_info if wrp.sys_info else '')


################################################ result / folder management ###
import util

cwd = settings.varial_working_dir
_tool_stack = []
results_base = None
current_result = None


def _mktooldir():
    global cwd
    cwd = (settings.varial_working_dir
           + "/".join(t.name for t in _tool_stack)
           + "/")
    if not os.path.exists(cwd):
        os.mkdir(cwd)


class ResultProxy(object):
    def __init__(self, tool, parent, path):
        self.name = tool.name
        self.io = tool.io
        self.parent = parent
        self.path = path
        self.children = {}
        self.result = None  # 0 means no result is available
        if parent:
            parent.children[self.name] = self

    def get_result(self):
        if self.result is None:
            with util.Switch(self.io, 'use_analysis_cwd', False):
                with self.io.block_of_files:
                    self.result = self.io.get(self.path + 'result') or 0
        return self.result or None

    def lookup(self, keys):
        if not keys:
            return self
        k = keys.pop(0)
        if k == '.':
            return self.lookup(keys)
        if k == '..' and self.parent:
            return self.parent.lookup(keys)
        if k in self.children:
            return self.children[k].lookup(keys)


def push_tool(tool):
    global current_result
    global results_base
    _tool_stack.append(tool)
    _mktooldir()
    current_result = ResultProxy(tool, current_result, cwd)
    if not results_base:
        results_base = current_result


def pop_tool():
    global current_result
    t = _tool_stack.pop()
    _mktooldir()
    current_result.result = getattr(t, 'result', 0)
    current_result = current_result.parent


def get_current_tool_path():
    return "/".join(t.name for t in _tool_stack)


def _lookup(key):
    keys = key.split('/')
    if keys[0] in ('', '.'):
        keys.pop(0)
    if keys[0] == '..':
        return current_result.lookup(keys)
    else:
        if keys == [results_base.name]:
            return results_base
        if keys[0] == results_base.name:
            keys.pop(0)
        return results_base.lookup(keys)


def lookup_result(key, default=None):
    """
    Lookup the result of tool.

    :param key:     str, e.g. ``/MyToolChain/MyFirstTool`` (absolute path)
                    or ``../MyFirstTool`` (relative path)
    :returns:       Wrapper
                    or list of Wrappers
                    or None
    """
    res = _lookup(key)
    if res and res.get_result():
        return res.result
    else:
        return default


def lookup_path(key):
    """
    Lookup the absolute path of a tool.

    :param key:     str, e.g. ``../MyFirstTool`` (relative path)
    :returns:       str
    """
    res = _lookup(key)
    return res.path if res else ""


def lookup_parent_name(key):
    """
    Lookup the name of the parent of a tool.

    :param key:     str, e.g. ``/MyToolChain/MyFirstTool`` (absolute path)
                    or ``../MyFirstTool`` (relative path)
    :returns:       str
    """
    res = _lookup(key)
    if res and res.parent:
        return res.parent.name


def lookup_children_names(key):
    """
    Lookup the names of the childrens of a tool.

    :param key:     str, e.g. ``/MyToolChain/MyFirstTool`` (absolute path)
                    or ``../MyFirstTool`` (relative path)
    :returns:       list of str
    """
    res = _lookup(key)
    if res:
        return res.children.keys()


def lookup_tool(abs_path):
    """
    Lookup a tool by its absolute path. Will return ``None`` if unsuccessful.
    """
    tokens = abs_path.split('/')
    if tokens and not tokens[0]:
        tokens.pop(0)
    if not tokens:
        raise RuntimeError('lookup_tool: abs_path empty, %s' % abs_path)
    if not _tool_stack:
        raise RuntimeError('lookup_tool: _tool_stack empty.')
    if tokens.pop(0) != _tool_stack[0].name:
        raise RuntimeError(
            'lookup_tool: tokens.pop(0) != _tool_stack[0].name, %s, %s' % (
                tokens.pop(0), _tool_stack[0].name))
    tmp = _tool_stack[0]
    for tok in tokens:
        try:
            tmp = tmp.tool_names[tok]
        except KeyError:
            raise RuntimeError(
                'lookup_tool: %s has no tool called %s' % (
                    tmp.name, tok))
    return tmp


def print_tool_tree():
    """Print all tools the ran or were reused."""
    print '='*80
    print 'Tools available through analysis.lookup:'
    print '+', results_base.name
    for rname in sorted(results_base.children):
        _print_tool_tree(results_base.children[rname], 0)
    print '='*80


def _print_tool_tree(res, indent):
    print '    ' + '|   '*indent + '+', res.name
    for rname in sorted(res.children):
        _print_tool_tree(res.children[rname], indent + 1)


############################################################### fileservice ###
fs_aliases = []
fs_wrappers = {}


def fileservice(section_name, autosave=True):
    """
    Return FileService Wrapper for automatic storage.

    This function returns a wrapper to collect and automatically store
    histograms. When called with ``autosave=True`` (default option), the
    wrappers will be store when python exits and all wrappers will be stored
    into one file, where the ``section_name`` argument is the directory in
    which all histograms are stored in the rootfile.

    :param section_name:    str, name of the directory in the fileservice
                            output, where all histograms on the wrapper are
                            stored.
    :param autosave:        bool, default: ``True``
    :returns:               FileServiceWrapper
    """
    if autosave:
        if section_name not in fs_wrappers:
            fs_wrappers[section_name] = wrappers.FileServiceWrapper(name=section_name)
        return fs_wrappers[section_name]
    else:
        return wrappers.FileServiceWrapper(name=section_name)


############################################################### fileservice ###
def reset():
    global active_samples, all_samples, cwd, _tool_stack, results_base, \
        current_result, fs_aliases, fs_wrappers
    active_samples = []
    all_samples = {}
    cwd = settings.varial_working_dir
    _tool_stack = []
    results_base = None
    current_result = None
    fs_aliases = []
    fs_wrappers = {}


#TODO cwd as a property => function to register cwd_changed callbacks
