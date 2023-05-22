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
m_higgs = np.arange(260, 660, 10)
htmins = np.arange(800, 8000, 100)
mpoints = [(mh, mh/100., htmin) for htmin in htmins for mh in m_higgs]
# print(mpoints)

for mh, wh, htmin in mpoints:
    # print('ChargedHiggs_HplusToBC_HminusToBC_MH%.0f_WH%.2f_HTmin%.0f' % (mh, wh, htmin))
    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(1),
            GridpackPath =  cms.string('instMG://ChargedHiggs_HplusToBC_HminusToBC_HT-800to8000_MH-260to650/MG5_aMC_v2.6.5/%.0f:%.2f:%.0f' % (mh, wh, htmin)),
            ConfigDescription = cms.string('ChargedHiggs_HplusToBC_HminusToBC_MH%.0f_WH%.2f_HTmin%.0f' % (mh, wh, htmin)),
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
