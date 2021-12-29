"""
Project histograms from trees with map/reduce.
"""


def _prepare_selection(params, quantity, weight=''):
    selection = params.get('selection')

    if any(isinstance(selection, t) for t in (list, tuple)):
        if params.get('nm1', True):
            # N-1 instruction: don't cut the plotted variable
            selection = list(s for s in selection if quantity not in s)
        selection = '(' + ')&&('.join(selection) + ')'

    return '%s*(%s)' % (weight or params.get('weight') or '1', selection or '1')


def map_projection(key_histo_filename, params, open_file=None, open_tree=None):
    """
    Map histogram projection to a root file

    :param key_histo_filename:      (str) e.g. ``'mysample myhisto /nfs/path/to/file.root'``
    :param params:                  dictionary with parameters (see below)
    :param open_file:               open TFile instance (can be None)
    :param open_tree:               TTree instance to be used (can be None)

    The param dict must have these contents:

    ======================= ================================================================
    histos                  dict of histoname -> tuple(title,n_bins,low bound,high bound)
                            IMPORTANT: the name of the histogram is also the plotted quantity
                            If another quantity should be plotted, it can be passed as the first
                            item in the tuple: tuple(quantity,title,n_bins,low bound,high bound).
                            If a six-tuple is provided, the first item is interpreted as a special
                            weight-expression for this histogram: tuple(weight,quantity,title,...).
    treename                name of the TTree in the ROOT File (not needed when open_tree is given)
    selection (optional)    selection string for TTree.Draw
    nm1 (optional)          create N-1 plots (not placing a selection on the plotted variable)
    weight (optional)       used in selection string for TTree.Draw
    aliases (optional)      dict alias -> function to be used with TTree.SetAlias
    ======================= ================================================================
    """
    from ROOT import TFile, TH1, TH1F, TTree

    key, histoname, filename = key_histo_filename.split()
    histoargs = params['histos'][histoname]
    if len(histoargs) == 6:
        weight, quantity, histoargs = histoargs[0], histoargs[1], histoargs[2:]
    elif len(histoargs) == 5:
        weight, quantity, histoargs = '', histoargs[0], histoargs[1:]
    else:
        weight, quantity = '', histoname

    histo_draw_cmd = '%s>>+%s' % (quantity, 'new_histo')
    input_file = open_tree or open_file or TFile(filename)
    selection = _prepare_selection(params, quantity, weight)

    try:
        if input_file.IsZombie():
            raise RuntimeError('input_file.IsZombie(): %s' % input_file)

        TH1.AddDirectory(True)
        histo_factory = params.get('histo_factory', TH1F)
        histo = histo_factory(histoname, *histoargs)
        histo.SetName('new_histo')

        tree = open_tree or input_file.Get(params['treename'])
        if not isinstance(tree, TTree):
            raise RuntimeError(
                'There seems to be no tree named "%s" in file "%s"'%(
                    params['treename'], input_file))

        for alias, fcn in params.get('aliases', {}).iteritems():
            if not tree.SetAlias(alias, fcn):
                raise RuntimeError(
                    'Error in TTree::SetAlias: it did not understand %s.'%alias
                )

        tree_prep = params.get('tree_prep')
        if tree_prep:
            tree = tree_prep(tree) or tree

        n_selected = tree.Draw(histo_draw_cmd, selection, 'goff')
        if n_selected < 0:
            raise RuntimeError(
                'Error in TTree::Project. Are variables, selections and '
                'weights are properly defined? cmd, selection: %s, %s' % (
                    histo_draw_cmd, selection
                )
            )

        histo.SetDirectory(0)
        histo.SetName(histoname)

    finally:
        TH1.AddDirectory(False)
        if not (open_file or open_tree):
            input_file.Close()

    yield key+' '+histoname, histo


def reduce_projection(iterator, params):
    """Reduce by sample and add containers."""

    def _kvgroup(it):  # returns iterator over (key, [val1, val2, ...])
        from itertools import groupby
        for k, kvs in groupby(it, lambda kv: kv[0]):
            yield k, (v for _, v in kvs)

    def _histo_sum(h_iter):  # returns single histogram
        h_sum = next(h_iter).Clone()
        for h in h_iter:
            h_sum.Add(h)
        return h_sum

    for key, histos in _kvgroup(sorted(iterator)):
        yield key, _histo_sum(histos)


################################################################## adapters ###
def map_projection_per_file(args, open_file=None):
    """
    Map histogram projection to a root file

    Use ``store_sample`` to store the reduced output of this projector.

    :param args:    tuple(sample, filename, params), see ``map_projection`` function for more info.
    """
    sample, filename, params = args
    histos = params['histos'].keys()

    import ROOT
    open_file_local = open_file or ROOT.TFile(filename)
    open_tree = open_file_local.Get(params['treename'])
    if not isinstance(open_tree, ROOT.TTree):
        raise RuntimeError(
            'There seems to be no tree named "%s" in file "%s"'%(
                params['treename'], open_file_local))
    if open_tree.GetEntriesFast() and not params.get('nm1', False):
        import uuid
        params = params.copy()
        selection = _prepare_selection(params, '')
        name = uuid.uuid1().hex
        open_tree.Draw('>>'+name, selection, 'goff')
        eventlist = ROOT.gDirectory.Get(name)
        eventlist.SetDirectory(0)
        open_tree.SetEventList(eventlist)
        params['selection'] = ''

    try:
        map_iter = (res
                    for h in histos
                    for res in map_projection(
                        '%s %s %s'%(sample, h, filename), params, None, open_tree))
        result = list(map_iter)
        open_tree.SetEventList(None)
    finally:
        if not open_file:
            open_file_local.Close()

    return result


def map_projection_per_file_with_all_sections(args):
    """
    As map_projection_per_file, but runs over all sections as well.

    Use ``store_sample_with_all_sections`` to store the reduced output of this projector.

    (This function allows to open every file only once)
    """
    sample, filename, list_of_sections_and_params = args

    import ROOT
    open_file = ROOT.TFile(filename)

    try:
        map_iter = (
            res
            for section, params in list_of_sections_and_params
            for res in map_projection_per_file(
                ('%s/%s' % (sample, section), filename, params),
                open_file
            )
        )
        result = list(map_iter)
    finally:
        open_file.Close()

    return result


def reduce_projection_by_two(one, two):
    return list(reduce_projection(one+two, None))


###################################################################### util ###
def store_sample(sample, section, result):
    import varial

    def do_store(key_histoname, histo):
        if section:
            _, name = key_histoname.split()
            sec = section
        else:
            sample_sec, name = key_histoname.split()
            _, sec = sample_sec.split('/')
        fs_wrp = varial.analysis.fileservice(sec)
        fs_wrp.sample = sample
        setattr(fs_wrp, name, histo)
        return key_histoname, histo

    # return a list - not a generator - to make sure that storing is executed
    return list(do_store(k, h) for k, h in result)


def store_sample_with_all_sections(sample, result):
    return store_sample(sample, None, result)
