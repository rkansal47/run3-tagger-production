import FWCore.ParameterSet.Config as cms

#Link to datacards:
#https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/BulkGraviton_hh_granular
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

import numpy as np
m_higgs = np.array([15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250])
htmins = np.arange(600, 6000, 100)
mpoints = [(mh, mh/100., htmin) for htmin in htmins for mh in m_higgs]
# print(mpoints)

for mh, wh, htmin in mpoints:
    # print('ChargedHiggs_HplusToCS_HminusToCS_MH%.0f_WH%.2f_HTmin%.0f' % (mh, wh, htmin))
    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(1),
            GridpackPath =  cms.string('instMG://ChargedHiggs_HplusToCS_HminusToCS_HT-600to6000_MH-15to250/MG5_aMC_v2.6.5/%.0f:%.2f:%.0f' % (mh, wh, htmin)),
            ConfigDescription = cms.string('ChargedHiggs_HplusToCS_HminusToCS_MH%.0f_WH%.2f_HTmin%.0f' % (mh, wh, htmin)),
            PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CP5SettingsBlock,
                pythia8PSweightsSettingsBlock,
                parameterSets = cms.vstring('pythia8CommonSettings',
                                            'pythia8CP5Settings',
                                            'pythia8PSweightsSettings',
		        )
            )
        )
    )
