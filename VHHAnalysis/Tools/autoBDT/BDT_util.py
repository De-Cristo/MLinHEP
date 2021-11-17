import os
from cfg_BDT_setting import signal_list, background_list

def ReadSamples(_input_filename_list):
    _sample_files_in = open(_input_filename_list, 'r')
    _sample_lines = _sample_files_in.readlines()
    _sample_lines = [line.strip("\n") for line in _sample_lines]
#     for _line in _sample_lines:
#         print(_line)
#     #end
    _sample_files_in.close()
    return _sample_lines
#END

def ClassifySamples(_file_list):
    _sample_type = []
    _signal_samples = []
    _background_samples  = []
    for _file_name in _file_list:
        _type = -1
        for _flag in signal_list:
            if _flag in _file_name:
                print(_file_name + ' will be used as signal sample.')
                _signal_samples.append(_file_name)
                _type = 0
                break
            else:
                continue
        #end
        for _flag in background_list:
            if _flag in _file_name:
                print(_file_name + ' will be used as background sample.')
                _background_samples.append(_file_name)
                _type = 1
                break
            else:
                continue
        #end
        if _type==-1:
            print('WARNING:: ' + _file_name + ' is not concluded in the sample lists! It will not be used.')
        _sample_type.append(_type)
    #end
    return _sample_type, _signal_samples, _background_samples
#END

def getabsroute(path):
    listdir = os.listdir(path)
    fout = open('VHH_BDT_sample.txt', 'a+')
    for file in listdir:
        fout.write(path + '/' + file + '\n')
    return 1

def change_file(scriptname, replacements):
    ## make a backup copy
    bkpname = scriptname + '.bak'
    print(scriptname, bkpname)
    os.system('mv %s %s' % (scriptname, bkpname))

    # edit new script
    fin  = open(bkpname, 'r')
    fout = open(scriptname, 'w')

    for line in fin:
        for old, new in replacements.items():
            line = line.replace(old, new)
        fout.write(line)
    #end

    fin.close()
    fout.close()

    # delete backup file
    os.system('rm %s' % bkpname)
#END