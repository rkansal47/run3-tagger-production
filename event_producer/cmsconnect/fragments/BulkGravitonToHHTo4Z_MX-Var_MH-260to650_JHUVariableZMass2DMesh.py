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
# low mass list
low_m_higgs = np.array([15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250])
low_m_res = np.arange(600, 6000, 100)

# high mass list
m_higgs = np.arange(260, 660, 10)
# # minimum m_res changes s.t. it is always > 2x m_higgs to avoid off-shell Higgses
# m_res_min = np.linspace(600, 1600, len(m_higgs))  

# reweight points such that there are the same number of events at 260 as 250 GeV
# and then continuously decrease the weight from there till 650 GeV
num_low_points = float(len(low_m_higgs))
num_high_points = float(len(m_higgs))

# solve system of equations s.t. 1) total weight sums to 1, and 2) the first weight is 1 / (# of low points) i.e. same # of events as 260 GeV
m = np.array([[num_high_points, num_high_points * (num_high_points - 1) / 2], [1, num_high_points]])
b = np.array([1.0, 1.0 / num_low_points])
# a is smallest weight, d is spacing between weights
a, d = np.linalg.solve(m, b)


def mh_weight(mh):
    idx = np.where(m_higgs == mh)[0][0]
    return a + d * (len(m_higgs) - idx - 1)


def mres_min(mh):
    """Choose mX for mH s.t. mX^2 - 4mH^2 remains constant for each mH"""
    mdel = 600**2 - 4 * 250**2
    return np.sqrt(mdel + 4 * mh ** 2)


for mh in m_higgs:
    m_res = np.linspace(mres_min(mh), mres_min(mh) * 10, len(low_m_res), endpoint=False)
    for mx in m_res:
        print('BulkGravitonToHH_MX%.0f_MH%.0f weight %.5f' % (mx, mh, mh_weight(mh)))
        generator.RandomizedParameters.append(
            cms.PSet(
                ConfigWeight = cms.double(mh_weight(mh)),
                GridpackPath =  cms.string('instMG://BulkGravitonToHH_MX-Var_MH-260to650/MG5_aMC_v2.6.5/%.0f:%.0f' % (mx, mh)),
                ConfigDescription = cms.string('BulkGravitonToHH_MX%.0f_MH%.0f' % (mx, mh)),
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
