"""
Read/Write wrappers on disk. Directory based.

This io module is specialized for faster writing to disk while plotting. Instead
of producing individual .info and .root files for every plot, the info and root
content accumulated in single files and written at once.

Only generator modules are provided.
"""


from ROOT import TFile
import cPickle
import os

import settings  # init ROOT first
import generators
import analysis
import wrappers
import monitor


_rootfile = '_varial_rootobjects.root.rt'
_infofile = '_varial_infodata.pkl'
use_analysis_cwd = True


def bulk_read_info_dict(dir_path=None):
    """Returns dict of info-dicts (not wrapper instances)"""
    if use_analysis_cwd:
        dir_path = os.path.join(analysis.cwd, dir_path)
    infofile = os.path.join(dir_path, _infofile)
    if not os.path.exists(infofile):
        return {}

    with open(infofile) as f:
        res = cPickle.load(f)
    assert(type(res) == dict)
    for key in res:
        res[key] = wrappers.Wrapper(**res[key])
    return res


def bulk_write(wrps, name_func, dir_path='', suffices=None, linlog=False):
    """Writes wrps en block."""

    # prepare
    if use_analysis_cwd:
        dir_path = os.path.join(analysis.cwd, dir_path)
    if not suffices:
        suffices = settings.rootfile_postfixes
    infofile = os.path.join(dir_path, _infofile)
    rootfile = os.path.join(dir_path, _rootfile)

    # todo with(SyncWriteIo()): for all the next statements
    # make a dict name -> wrps
    wrps_dict = dict()
    for w in wrps:
        name = name_func(w)
        assert name, 'function "%s" returns %s for "%s"' % (name_func, repr(name), w)
        if name in wrps_dict:
            monitor.message(
                'sparseio',
                'WARNING Overwriting file "%s" from this session in path: %s' %
                (name, dir_path)
            )
        wrps_dict[name] = w

    # write out info
    info = dict((name, w.all_writeable_info())
                for name, w in wrps_dict.iteritems())
    with open(infofile, 'w') as f_info:
        cPickle.dump(info, f_info)

    # write out root file
    f_root = TFile.Open(rootfile, 'RECREATE')
    f_root.cd()
    for name, w in wrps_dict.iteritems():
        dirfile = f_root.mkdir(name, name)
        dirfile.cd()
        w.obj.Write(name)
        dirfile.Close()
    f_root.Close()

    # write with suffices
    for suffix in suffices:
        if suffix == '.root':
            continue

        for name, w in wrps_dict.iteritems():

            # root will not store filenames with '[]' correctly. fix:
            alt_name = name.replace('[', '(').replace(']', ')')
            img_path = os.path.join(dir_path, alt_name)
            good_path = os.path.join(dir_path, name)

            if linlog:
                w.main_pad.SetLogy(0)
                w.obj.SaveAs(img_path+'_lin'+suffix)

                generators.switch_log_scale_single_cnv(w, False, True)
                w.obj.SaveAs(img_path+'_log'+suffix)
                generators.switch_log_scale_single_cnv(w, False, False) # reset to lin

                if alt_name != name:
                    os.rename(img_path+'_lin'+suffix, good_path+'_lin'+suffix)
                    os.rename(img_path+'_log'+suffix, good_path+'_log'+suffix)
            else:
                w.obj.SaveAs(img_path+suffix)
                if alt_name != name:
                    os.rename(img_path+suffix, good_path+suffix)

    return wrps_dict.values()
