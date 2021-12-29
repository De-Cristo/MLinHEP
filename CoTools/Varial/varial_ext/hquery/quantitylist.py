import multiprocessing as mp
import json
import ROOT


plain_types = {'int': int, 'float': float, 'long': long, 'bool': bool}
plain_types_list = plain_types.values()
plain_c_types = plain_types.keys() + ['double', 'short']


def get_proc(filenames, treename):
    proc = mp.Process(target=make_json, args=(filenames, treename))
    proc.start()
    return proc


def make_json(filenames, treename):
    filenames = iter(filenames)
    f, t = None, None
    while not t:
        if f:
            f.Close()
        f = ROOT.TFile(next(filenames))
        t = f.Get(treename)
        t = _get_content(t)

    names = list(b.GetName() for b in t.GetListOfBranches())
    names = list(
        res
        for bname in names
        for res in _handle_item(bname, getattr(t, bname), 0)
    )
    f.Close()
    with open('sections/branch_names.json', 'w') as f:
        json.dump(names, f)


def _handle_item(name, item, depth):
    item_typ = type(item)

    if item is None or depth > 1:
        return []

    elif item_typ in plain_types_list:
        return [name]

    elif 'vector<' in str(item_typ):
        data_typ = str(item_typ).split('vector<')[1].split('>')[0]
        if data_typ in plain_types:
            return [name, '@%s.size()' % name]
        else:
            typ_inst = getattr(ROOT, data_typ)()
            object_items = _handle_item('', typ_inst, depth)
            object_items = list(
                name + conj + res
                for res in object_items
                for conj in ('.', '[0].')
            )
            return ['@%s.size()' % name] + object_items

    elif callable(item):
        func_doc = getattr(item, 'func_doc', '')
        if func_doc.startswith('void '):
            return []
        elif any(func_doc.startswith(t + ' ') for t in plain_c_types):
            return [name+'()']
        else:
            return []

    else:
        name = name + '.' if name else ''
        return list(
            name + res
            for funcname in dir(item)
            if not funcname.startswith('_')
            for res in _handle_item(
                funcname, getattr(item, funcname), depth+1)
        )


def _get_content(t):
    try:
        return next(iter(t))    # try to iterate on events
    except StopIteration:
        return None             # return None for empty files
