from SM_util import *
from file_config import *

R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--InputFile", dest="inFile", type=str, default='/data/pubfs/zhanglic/workspace/newbox/MLinHEP/BTVatHLT/datasample/',   help="Ntuple direction" )
parser.add_argument("-o", "--OnputFile", dest="outFile",type=str, default='/data/pubfs/zhanglic/workspace/newbox/MLinHEP/BTVatHLT/mergedsample/', help="Output Ntuple direction" )
parser.add_argument("-m", "--MultThread",dest="MT",     type=int, default=16,   help="How many threads will be used (default = 16)" )
parser.add_argument("-p", "--MultProc",  dest="MP",     type=int, default=8,    help="How many sub processes will be started (default = 8)" )
args = parser.parse_args()

R.EnableImplicitMT(args.MT)
rdf = {}
pdf = {}

inDir = os.path.abspath(args.inFile)
outDir = os.path.abspath(args.outFile)

print('Input files in '+inDir)
print('Output file in '+outDir)

os.system('mkdir -p '+outDir)
os.system('mkdir -p '+outDir+'/training/')
os.system('mkdir -p '+outDir+'/validation/')
os.system('mkdir -p '+outDir+'/testing/')

ourDir_train = outDir+'/training/'
ourDir_train = outDir+'/validation/'
ourDir_train = outDir+'/testing/'

Sample_Name_Lines = os.listdir(inDir)
Sample_type, Training_Samples, Testing_Samples = ClassifySamples(Sample_Lines)

tree_name = 'deepntuplizer/tree' # for HLT samples from DeepNtuplizer

# Testing Sample
test_ratio = 0.2
test_file_list = []

for sample in Testing_Samples:
    _file_list = os.listdir(sample)
    for _file in _file_list:
        test_file_list.append(sample+_file)
#end

rdf['raw_test'] = R.RDataFrame(tree_name, _file_list)
pdf['raw_test'] = pd.DataFrame(rdf['raw_test'].AsNumpy())
pdf['raw_test'].info()

newDf=df.loc[r,:]

N = np.arange(0,10)
batch = 3
n_cats, sublist = data_split(N, batch, shuffle=True)

for cat in range(0,n_cats):
    print(sublist[cat])


exit(0)