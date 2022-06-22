# MLinHEP


<!-- TOC -->

- [1. VHHAnalysis](#1.-VHHAnalysis)
    - [1. XGBoost Tools](#1.-XGBoost-Tools)
    - [2. Standard generation process in CMSSW](#2.-Standard-generation-process-in-CMSSW)
- [2. BDT Toolkits (for HEP)](#2.-BDT-Toolkits-(for-HEP))
<!-- /TOC -->


## 1. VHHAnalysis
Contains the tools that mainly developed for VHH analysis on CMS experiment. But they are flexible!
### 1. XGBoost Tools
BDT classifiers based on XGBoost with the python sk-learn interface/API. They can be used for variable plotting, correlation calculation, etc. Also the training results are also visiable, such as variable importances, validation plots, etc.

Now the main parts of this tool has been independantly implemented in [BDT4HEP](#2.-BDT-Toolkits-(for-HEP)), but you can still find examples in this [part](VHHAnalysis/)
### 2. Standard generation process in CMSSW
The implemented scripts to generate samples from the truth level until NANO-AOD files.

## 2. BDT Toolkits (for HEP)