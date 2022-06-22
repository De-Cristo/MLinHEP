# MLinHEP


<!-- TOC -->

- [1. VHHAnalysis](#1.-VHHAnalysis)
    - [1. XGBoost Tools](#1.-XGBoost-Tools)
    - [2. Standard generation process in CMSSW](#2.-Standard-generation-process-in-CMSSW)
- [2. BDT Toolkits (for HEP)](#2.-BDT-Toolkits-(for-HEP))
<!-- /TOC -->

---
## 1. VHHAnalysis
Contains the tools that mainly developed for VHH analysis on CMS experiment. But they are flexible!
### 1. XGBoost Tools
BDT classifiers based on [XGBoost](https://xgboost.readthedocs.io/en/stable/tutorials/index.html) with the python sk-learn interface/API. They can be used for variable plotting, correlation calculation, etc. Also the training results are also visiable, such as variable importances, validation plots, etc.

> Now the main parts of this tool has been independantly implemented in [BDT4HEP](#2.-BDT-Toolkits-(for-HEP), but you can still find examples in this [part](VHHAnalysis/).

### 2. Standard generation process in CMSSW
The implemented scripts to generate samples from the truth level until NANO-AOD files.


### 3. Higgs pair analysis tools
The scripts in this [part](VHHAnalysis/Tools) can be used for simple tasks that are useful for Higgs pair studies. 
For example, to calculate the interference between the Feynman diagrams in ggHH/VBFHH/VHH production mode. There are also scripts for ROOT based analysis tasks such as a self defined tree slimmer. 
What's more, for official tools recommended by CMS higgs group, the [HiggsCombinationTool](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/) and [HH inference tool](https://cms-hh.web.cern.ch/cms-hh/tools/inference/index.html), you can find some usefull commands or scripts in [HiggsCombine](VHHAnalysis/Tools/HiggsCombine). More details and usage can be found at this [note](VHHAnalysis/README.ipynb).

---
## 2. BDT Toolkits (for HEP)
Boost Decision Tree is one of the most popular Reinforcement Learning technique adapted in Particle Physics experiment study. This repo provide the python interface to apply BDT to the HEP data.

