python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c ttbar_med_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&controlSample==11&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0  -s systematics_Wlnshapes2017STXS.txt  -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_ttbar_med_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c ttbar_med_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&controlSample==11&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_ttbar_med_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_med_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&H_mass<90&&controlSample==13&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_Whf_med_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_med_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&H_mass<90&&controlSample==13&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_Whf_med_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_med_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&H_mass>150&&controlSample==13&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0  -s systematics_Wlnshapes2017STXS.txt  -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_Whf_med_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_med_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&H_mass>150&&controlSample==13&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_Whf_med_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Wlf_med_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&controlSample==12&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_Wlf_med_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Wlf_med_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&controlSample==12&&V_pt<=250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_Wlf_med_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c ttbar_high_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&controlSample==11&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0  -s systematics_Wlnshapes2017STXS.txt  -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_ttbar_high_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c ttbar_high_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&controlSample==11&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_ttbar_high_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_high_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&H_mass<90&&controlSample==13&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_Whf_high_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_high_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&H_mass<90&&controlSample==13&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_Whf_high_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_high_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&H_mass>150&&controlSample==13&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0  -s systematics_Wlnshapes2017STXS.txt  -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_Whf_high_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Whf_high_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&H_mass>150&&controlSample==13&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_Whf_high_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Wlf_high_Wmn -p "usingBEnriched&&V_pt>=150&&isWmunu&&controlSample==12&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0  -o $ORIG_DIR/hists_Wlf_high_Wmn_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True
python splitSamples.py -i /nfs/dust/cms/user/dewita/VHbbAnalysisNtuples/vhbb_2017_1802/haddjobs/ -c Wlf_high_Wen -p "usingBEnriched&&V_pt>=150&&isWenu&&controlSample==12&&V_pt>250" -s "" -v "Jet_btagDeepB[hJetInd2]" --xlow 0.0 --xhigh 1.0 -s systematics_Wlnshapes2017STXS.txt   -d 1 -n 15 -w 1.0 -o $ORIG_DIR/hists_Wlf_high_Wen_SAMP.root -r 0 -sa SAMP --year '2017' --channel 'Wln' --drawFromNom True