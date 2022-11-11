# Introduction

## DNNTuple v6 (2022.10.23)

### Jet labels

| Jet types | Labels | Sample source |
| ------- | ------ | ------ |
| H→WW→qqqq | `label_H_WqqWqq_0c`, `label_H_WqqWqq_1c`, `label_H_WqqWqq_2c`, `label_H_WqqWq_0c`, `label_H_WqqWq_1c`, `label_H_WqqWq_2c` | `BulkGravitonToHHTo4W_MX-600to6000_MH-15to250_JHUVariableWMass` |
| H→WW→e/μνqq | `label_H_WqqWev_0c`, `label_H_WqqWev_1c`, `label_H_WqqWmv_0c`, `label_H_WqqWmv_1c` | same as above |
| H→WW→τνqq | `label_H_WqqWtauev_0c`, `label_H_WqqWtauev_1c`, `label_H_WqqWtaumv_0c`, `label_H_WqqWtaumv_1c`, `label_H_WqqWtauhv_0c`, `label_H_WqqWtauhv_1c` | same as above |
| H→bb/cc/ss/qq/ττ | `label_H_bb`, `label_H_cc`, `label_H_ss`, `label_H_qq`, `label_H_tauhtaue`, `label_H_tauhtaum`, `label_H_tauhtauh` | `BulkGravitonToHHTo4QTau_MX-600to6000_MH-15to250` |
| QCD | `label_QCD_bb`, `label_QCD_cc`, `label_QCD_b`, `label_QCD_c`, `label_QCD_others` | `QCD_Pt_170toInf_ptBinned_TuneCP5_13TeV_pythia8` |
| t→bW→bqq | `label_Top_bWqq_0c`, `label_Top_bWqq_1c`, `label_Top_bWq_0c`, `label_Top_bWq_1c` | `Spin0ToTT_VariableMass_WhadWhad_MX-600to6000_MH-15to250` |
| t→bW→bℓν | `label_Top_bWev`, `label_Top_bWmv`, `label_Top_bWtauhv`, `label_Top_bWtauev`, `label_Top_bWtaumv` | `Spin0ToTT_VariableMass_WlepWlep_MX-600to6000_MH-15to250` |

### Sample defination

The samples are produced in Run-2 UL2017 condition.

For samples used above:

 - `BulkGravitonToHHTo4W_MX-600to6000_MH-15to250_JHUVariableWMass`: bulk graviton to HH to four Ws samples produced by MadGraph, where graviton mass and Higgs mass are allowed to vary. The graviton mass is set in 600-6000 GeV range and Higgs mass in 15-250 GeV. The cascade decay of H→WW→qqqq/ℓνqq is treated by JHUGen, with the W mass configured to maintain the m_W/m_H ratio constant.
 - `BulkGravitonToHHTo4QTau_MX-600to6000_MH-15to25`: bulk graviton to HH to four quarks sample produced by MadGraph, where graviton mass and Higgs mass are allowed to vary, same as above. Note that this sample configuration is the same as the one used for official ParticleNet-MD training.
 - `Spin0ToTT_VariableMass_Whad(lep)Whad(lep)_MX-600to6000_MH-15to250`: bulk graviton to tt̅ to all top final states produced by MadGraph. The graviton mass is allowed to vary from 600-6000 GeV and top mass from 15-250 GeV range. The W boson mass is configured to maintain the m_W/m_t ratio constant, with a minimum threshold of 80 GeV. The width of the W is set equal to the W mass so that the truth W mass is allowed to further vary in a wide range.
 - `QCD_Pt_170toInf_ptBinned_TuneCP5_13TeV_pythia8`: HT-binned QCD multijet MadGraph sample.

Other samples:

 - `ZprimeToTT_M1200to4500_W12to45_TuneCP2_PSweights`: Z' to tt̅ to all top final states produced by MadGraph. The top mass is fixed in SM value while the mass of the Z' resonance is allowed to vary from 1200-4500 GeV.

# Included scores

The ntuple also includes

 - existing ParticleNet AK8 scores and regressed mass;
 - [ParticleNet-based DeepHWW MD V1 tagger](https://github.com/colizz/DNNTuples/tree/dev-UL-hww/Ntupler/data/DeepHWW-MD/ak8/V01) scores (superseded);
 - [all-inclusive ParticleTransformer-based MD V1 tagger](https://github.com/colizz/DNNTuples/tree/dev-UL-hww/Ntupler/data/InclParticleTransformer-MD/ak8/V01) scores (37 classes in total), one regressed mass, and 128 hidden neuron scores.

--------------------

# Run DNNTuple step on CMSConnect

```label_bash
# Run following commands in this directory

mkdir output log # important!
voms-proxy-init -voms cms -valid 192:00

condor_submit jdl/test/submit_w_test.jdl
```