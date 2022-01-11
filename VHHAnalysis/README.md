# VHH Analysis TOOLS

---
After set up CMS basic environment by cvmfs, one can set up the working environment by

```shell
source initial.sh
```

Other dependent packages can be setup with conda. Relavant envs has been listed in the LINK(under development...)

---
## TOOLS

### Analysis sample preparing
The Analysis sample preparing tool can be found in `Tools`, the `slim_training_samples.py`. Here's an example:

```shell
python slim_analysis_samples.py -m 16 -p 8 -d /PATH/TO/FILE/
```

Only specific branches will be kept after slimming, which can be set in `analysis_branch.py`.

### Training sample preparing

Different script will be used to combine the Analysis samples to generate training samples.

### Coupling Merge Tool
The coupling merge tool can be found in `Tools`, the `CouplingMergingTool.py`.
Here's an example:

```shell
python CouplingMergingTool.py -m 4 -v 1 -n 6 -hh VHH -c c2v -r -30 30 -d 0 -w 10
```

`-m` is the number of threads to be used, `-v` is the verbose level, `-n` is the basic samples to be used to form the basic metrix, `-c` defines the coupling type(such as `c2v,kl,cv,kt`), `-r` sets the range of the scan, `-d` is the trigger if we do merge, `-w` is the new coupling of the merged sample, `-hh` defines the Di-Higgs Model (now we have updated models for GGF, VBF, VHH processes).

---
## Training

### BDT

XGBoost Toolkit will be used.

### NN(??)

Consider Pytorch and Keras as candidates.
