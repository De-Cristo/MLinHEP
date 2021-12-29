"""
Wrappers for root histograms, graphs and canvases.

A HistoWrapper holds a 'histo' member, a FloatWrapper holds 'float' member
variable and so on.. The StackWrapper has a histo variable as well, which hold
the sum of its component histograms.

Aliases describe histograms, that are not loaded yet. They are
created from the directory structure of a rootfile. After possibly filtering
and sorting these, the histogram objects can be loaded with the ``diskio``
module.
"""

import settings  # init ROOT first
from ROOT import TH1, TH1D, TH2D, TH3D, THStack, TGraph, TCanvas, TObject
from ast import literal_eval


class WrapperBase(object):
    """
    Overwrites __str__ to print classname and __dict__
    """
    def __str__(self):
        """Writes all __dict__ entries into a string."""
        name = self.__dict__.get('name', self.__class__.__name__)
        txt = '_____________' + name + '____________\n'
        txt += self.pretty_info_lines()
        txt += '\n'
        return txt

    def __repr__(self):
        return str(self)

    def all_info(self):
        """Returns copy of self.__dict__."""
        return dict(self.__dict__)

    def all_writeable_info(self):
        """Like all_info, but removes root objects."""
        return dict(
            (k, v)
            for k, v in self.__dict__.iteritems()
            if k[0] != '_' and not isinstance(v, TObject)
        )

    def pretty_info_lines(self):
        return self._pretty_lines(sorted(self.__dict__.keys()))

    def pretty_writeable_lines(self):
        return self._pretty_lines(sorted(self.all_writeable_info().keys()))

    def _pretty_lines(self, keys):
        size = max(len(k) for k in keys) + 2
        return '{\n' + ',\n'.join(
                    ('%'+str(size)+'s: ')%('"'+k+'"')
                    + repr(getattr(self, k))
                    for k in keys
                ) + ',\n}'

    def __setattr__(self, name, value):
        if not (name[0] == '_'
                or name == 'history'
                or isinstance(value, TObject)):
            try:
                literal_eval(repr(value))
            except (ValueError, SyntaxError):
                raise RuntimeError(
                    'ERROR Wrapper members of non-literal values or '
                    'non-TObject-instances must start with an underscore.'
                    '\nName and value: ("%s", %s)' % (name, value)
                )
        return super(WrapperBase, self).__setattr__(name, value)


class Alias(WrapperBase):
    """
    Alias of a non-loaded histogram on disk.

    :param file_path:       str, path to root file
    :param in_file_path:    str, path to ROOT-object within the root file.
    :param typ:             str, classname of the root object
    """
    def __init__(self, file_path, in_file_path, typ):
        self.klass          = self.__class__.__name__
        self.file_path      = file_path
        self.in_file_path   = in_file_path
        self.name           = in_file_path.split('/')[-1]
        self.type           = typ


class FileServiceAlias(Alias):
    """
    Alias of a histogram in the fileservice output.

    :param file_path:       str, path to root file
    :param in_file_path:    str, path to ROOT-object within the root file.
    :param typ:             str, classname of the root object
    :param sample_inst:     sample instance which should be associated
    """
    def __init__(self, file_path, in_file_path, typ, sample_inst):
        super(FileServiceAlias, self).__init__(
            file_path,
            in_file_path,
            typ
        )
        self.sample         = sample_inst.name
        self.legend         = sample_inst.legend
        self.lumi           = sample_inst.lumi
        self.is_data        = sample_inst.is_data
        self.is_signal      = sample_inst.is_signal
        assert not(self.is_data and self.is_signal)  # both is forbidden!


class Wrapper(WrapperBase):
    """
    Wrapper base class.

    All constructor keywords are added as attributes.

    **Example:**

    >>> w = Wrapper(name='n', title='t', history='h', blabla=True)
    >>> info = w.all_info()
    >>> info['blabla']
    True
    """
    def __init__(self, **kws):
        self.name           = ''
        self.title          = self.name
        self.history        = ''
        kws.pop('type', None)  # do not overwrite type
        self.__dict__.update(kws)
        self.klass          = self.__class__.__name__

    def _check_object_type(self, obj, typ):
        if not isinstance(obj, typ):
            raise TypeError(
                '%s needs a %s instance as first argument! She got a %s.' %
                (self.__class__.__name__, str(typ), str(type(obj)))
            )
        if isinstance(obj, TObject):
            self.type = obj.ClassName()
        else:
            self.type = str(typ)

    def primary_object(self):
        """Deprecated."""
        return self.obj

    @property
    def obj(self):
        """Getter property for primary object."""
        pass


class WrapperWrapper(Wrapper):
    """
    Wrapper to wrap many wrappers.

    **Keywords:** See superclass.

    :raises: TypeError
    """
    _list_type = list
    def __init__(self, wrps, **kws):
        self._check_object_type(wrps, self._list_type)
        if not all(isinstance(w, WrapperBase) for w in wrps):
            raise TypeError(
                ('%s needs a list of wrappers as first argument! She got '
                 'something else in the list: \n' % self.__class__.__name__)
                + str(wrps)
            )
        super(WrapperWrapper, self).__init__(**kws)
        self.wrps = wrps
        if not self.name:
            if 'name_func' in kws:
                self.name = kws['name_func'](self)
            else:
                self.name = 'WrpWrp'

    def __iter__(self):
        return iter(self.wrps)

    def __len__(self):
        return len(self.wrps)

    def __getitem__(self, ind):
        return self.wrps[ind]

    @property
    def obj(self):
        """Getter property for primary object."""
        return self.wrps

    def __setattr__(self, name, value):
        if (value
            and isinstance(value, list)
            and any(isinstance(w, WrapperBase)for w in value)
        ):
            if not all(isinstance(w, WrapperBase) for w in value):
                raise TypeError(
                    ('List of wrappers must only contain wrappers! Something'
                     'else is in the list: \n')
                    + str(value)
                )
            # note: object.__setattr__ is called since we checked validity here
            return super(WrapperBase, self).__setattr__(name, value)
        else:
            return super(WrapperWrapper, self).__setattr__(name, value)


class FloatWrapper(Wrapper):
    """
    Wrapper for float values.

    **Keywords:** See superclass.

    :raises: TypeError

    >>> w = FloatWrapper(2.0, name='n', history='h')
    >>> w.float
    2.0
    >>> w.obj  # using Wrapper property
    2.0
    """
    _float_type = float
    def __init__(self, float_val, **kws):
        self._check_object_type(float_val, self._float_type)
        super(FloatWrapper, self).__init__(**kws)
        self.float = float_val

    @property
    def obj(self):
        return self.float


class HistoWrapper(Wrapper):
    """
    Wrapper class for a ROOT histogram TH1.

    :raises: TypeError
    """
    def __init__(self, histo, **kws):
        self._check_object_type(histo, TH1)
        super(HistoWrapper, self).__init__(**kws)
        self.histo          = histo
        self.name           = kws.get('name', histo.GetName())
        self.title          = kws.get('title', histo.GetTitle())
        self.is_data        = kws.get('is_data', False)
        self.is_pseudo_data = kws.get('is_pseudo_data', False)
        self.is_signal      = kws.get('is_signal', False)
        self.lumi           = kws.get('lumi', 1.)
        self.sample         = kws.get('sample', '')
        self.legend         = kws.get('legend', '')
        self.file_path      = kws.get('file_path', '')
        self.in_file_path   = kws.get('in_file_path', '')
        self.histo_sys_err  = kws.get('histo_sys_err', None)
        self.sys_info       = kws.get('sys_info', '')  # e.g. 'JER__minus'

        assert sum(
            1 for boool in
            (self.is_data, self.is_pseudo_data, self.is_signal)
            if boool
        ) <= 1, 'only one of is_data, is_pseudo_data, is_signal is allowed'

    def all_info(self):
        info = super(HistoWrapper, self).all_info()
        del info['histo']
        return info

    @property
    def obj(self):
        """Getter property for primary object."""
        return self.histo

    @property
    def is_background(self):
        return not any((self.is_data, self.is_pseudo_data, self.is_signal))


class StackWrapper(HistoWrapper):
    """
    Wrapper class for a ROOT histogram stack THStack.

    :raises: TypeError
    """
    def __init__(self, stack, **kws):
        self._check_object_type(stack, THStack)
        if 'histo' not in kws:
            kws['histo'] = self._add_stack_up(stack)
        super(StackWrapper, self).__init__(**kws)
        self.stack          = stack
        self.name           = kws.get('name', stack.GetName())
        self.title          = kws.get('title', stack.GetTitle())

    def _add_stack_up(self, stack):
        sum_hist = None
        for histo in stack.GetHists():
            if sum_hist:
                sum_hist.Add(histo)
            else:
                sum_hist = histo.Clone()
        return sum_hist

    def all_info(self):
        """
        :returns: dict with all members, but not the stack.
        """
        info = super(StackWrapper, self).all_info()
        del info['stack']
        return info

    @property
    def obj(self):
        """Getter property for primary object."""
        return self.stack


class GraphWrapper(Wrapper):
    """
    Wrapper class for a ROOT TGraph instance.

    **Keywords:**
    ``lumi``,
    ``is_data``
    ``is_signal``
    and also see superclass.

    :raises: TypeError
    """
    def __init__(self, graph, **kws):
        self._check_object_type(graph, TGraph)
        super(GraphWrapper, self).__init__(**kws)
        self.graph          = graph
        self.name           = kws.get('name', graph.GetName())
        self.title          = kws.get('title', graph.GetTitle())
        self.is_data        = kws.get('is_data', False)
        self.is_pseudo_data = kws.get('is_pseudo_data', False)
        self.is_signal      = kws.get('is_signal', False)
        self.lumi           = kws.get('lumi', 1.)
        self.sample         = kws.get('sample', '')
        self.legend         = kws.get('legend', '')
        self.file_path      = kws.get('file_path', '')
        self.in_file_path   = kws.get('in_file_path', '')

        assert sum(
            1 for bo in
            (self.is_data, self.is_pseudo_data, self.is_signal)
            if bo
        ) <= 1, 'only one of is_data, is_pseudo_data, is_signal is allowed'


    def all_info(self):
        """
        :returns: dict with all members, but not the histo.
        """
        info = super(GraphWrapper, self).all_info()
        del info['graph']
        return info

    @property
    def obj(self):
        """Getter property for primary object."""
        return self.graph

    @property
    def is_background(self):
        return not any((self.is_data, self.is_pseudo_data, self.is_signal))


class CanvasWrapper(Wrapper):
    """
    Wrapper class for a ROOT canvas TCanvas.

    **Keywords:** ``lumi`` and also see superclass.

    :raises: TypeError
    """
    def __init__(self, canvas, **kws):
        self._check_object_type(canvas, TCanvas)
        super(CanvasWrapper, self).__init__(**kws)
        self.canvas     = canvas
        self.name       = kws.get('name', canvas.GetName())
        self.title      = kws.get('title', canvas.GetTitle())
        self.main_pad   = kws.get('main_pad', canvas)
        self.second_pad = kws.get('second_pad')
        self.legend     = kws.get('legend')
        self.first_obj  = kws.get('first_obj')
        self.x_bounds   = kws.get('x_bounds')
        self.y_bounds   = kws.get('y_bounds')
        self.y_min_gr_0 = kws.get('y_min_gr_0')
        self.lumi       = kws.get('lumi', 1.)
        self._renderers = kws.get('_renderers', [])

    @property
    def obj(self):
        """Getter property for primary object."""
        self.canvas.Modified()
        self.canvas.Update()
        return self.canvas


class FileServiceWrapper(Wrapper):
    """
    Wrapper class for many histograms in one file.
    """

    def __init__(self, name, **kws):
        kws['name'] = name
        super(FileServiceWrapper, self).__init__(**kws)

    def makeTH1D(self, *args):
        """args need to be args for TH1D constructor."""
        self.append(TH1D(*args))

    def makeTH2D(self, *args):
        """args need to be args for TH2D constructor."""
        self.append(TH2D(*args))

    def makeTH3D(self, *args):
        """args need to be args for TH3D constructor."""
        self.append(TH3D(*args))

    def makeTH1D_from_dict(self, name, title, dictionary):
        """create a TH1D from the values in a dict."""
        hist = TH1D(name, title, len(dictionary), 0, len(dictionary))
        for k in sorted(dictionary.keys()):
            assert any(isinstance(dictionary[k], t) for t in (int, float))
            hist.Fill(str(k), dictionary[k])
        self.append(hist)

    def append(self, named_root_obj):
        name = named_root_obj.GetName()
        if hasattr(self, name):
            raise RuntimeError(
                'FileServiceWrapper: object with name exists: %s' % name)
        setattr(self, name, named_root_obj)

    def is_empty(self):
        return not any(
            isinstance(obj, TH1)
            for obj in self.__dict__.itervalues()
        )

if __name__ == '__main__':
    import doctest
    doctest.testmod()


# TODO merge_info(wrps) function that would return all common info -> rendering
