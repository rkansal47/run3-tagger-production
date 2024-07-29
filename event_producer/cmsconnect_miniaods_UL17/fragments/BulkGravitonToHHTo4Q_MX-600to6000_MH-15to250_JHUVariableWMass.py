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
    # energy not important since the method does not rely on it
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

import numpy as np
m_higgs = np.array([15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250])
m_res = np.arange(600, 6000, 100)
mpoints = [(mx, mh) for mx in m_res for mh in m_higgs]
# print(mpoints)

for mx, mh in mpoints:
    # print('BulkGravitonToHH_MX%.0f_MH%.0f' % (mx, mh))
    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(1),
            GridpackPath =  cms.string('instMG://BulkGravitonToHH_MX-600to6000_MH-15to250/MG5_aMC_v2.6.5/%.0f:%.0f' % (mx, mh)),
            ConfigDescription = cms.string('BulkGravitonToHH_MX%.0f_MH%.0f' % (mx, mh)),
            PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CP5SettingsBlock,
                pythia8PSweightsSettingsBlock,
                processParameters = cms.vstring(
                    '25:onMode = off',                     # higgs
                    '25:oneChannel = 1 0.33333 100 5 -5',  # bottom and anti-bottom quarks
                    '25:addChannel = 1 0.33333 100 4 -4',  # charm and anti-charm quarks
                    '25:addChannel = 1 0.11111 100 3 -3',  # strange and anti-strange quarks
                    '25:addChannel = 1 0.11111 100 2 -2',  # up and anti-up quarks
                    '25:addChannel = 1 0.11111 100 1 -1',  # down and anti-down quarks
                    # tau-tau?
                    'ResonanceDecayFilter:filter = on'
                ),
                parameterSets = cms.vstring(
                    'pythia8CommonSettings',
                    'pythia8CP5Settings',
                    'pythia8PSweightsSettings',
                    'processParameters',
                ),
            )
        )
    )

ProductionFilterSequence = cms.Sequence(generator)