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
m_top = np.arange(260, 660, 10)
m_z = 0.53 * m_top
m_z[m_z < 80] = 80  # to avoid unphysical m_w
m_res = np.arange(800, 8000, 100)
mpoints = [(mx, mx/100., mt, m_z[it], m_z[it]) for mx in m_res for it, mt in enumerate(m_top)]
# print(mpoints)

for mx, wx, mt, mz, ww in mpoints:
    # print('SpinToTT_VariableMass_WlepWlep_MX%.0f_WX%.0f_MH%.0f_MZ%.1f_WW80' % (mx, wx, mt, mz))
    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(1),
            GridpackPath =  cms.string('instMG://Spin0ToTT_VariableMass_WlepWlep/MG5_aMC_v2.6.5/%.0f:%.0f:%.0f:%.1f:%.1f' % (mx, wx, mt, mz, ww)),
            ConfigDescription = cms.string('Spin0ToTT_VariableMass_WlepWlep_MX%.0f_WX%.0f_MH%.0f_MZ%.1f_WW%.1f' % (mx, wx, mt, mz, ww)),
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
