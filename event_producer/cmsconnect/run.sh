#!/bin/bash -xe

## NOTE: difference made w.r.t. common exe script
## 1. __NEVENT__ not specify in the fragment
## 2. no LHE step, also need to change externalLHEProducer to generator
## 3. seeds have width 100

## in addition to cmsconnect_higgs version:
## 4. use custom cmssw (rsync from cvmfs)
## 5. download MG
## 6. use provided DIGI cfg
## 7. stop running dnntuples

sleep $(( ( RANDOM % 200 ) + 1 ))

wget --tries=3 https://github.com/colizz/hww-tagging/archive/refs/heads/dev-miniaods.tar.gz
tar xaf dev-miniaods.tar.gz
mv hww-tagging-dev-miniaods/event_producer/cmsconnect_miniaods_UL17/{inputs,fragments} .
# rsync -a /afs/cern.ch/user/c/coli/work/hww/hww-tagging-minis/event_producer/cmsconnect_miniaods_UL17/{inputs,fragments} . # test-only

wget --no-check-certificate https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.6.5.tar.gz
mv MG5_aMC_v2.6.5.tar.gz inputs/

if [ -d /afs/cern.ch/user/${USER:0:1}/$USER ]; then
  export HOME=/afs/cern.ch/user/${USER:0:1}/$USER # crucial on lxplus condor but cannot set on cmsconnect!
fi
env

JOBNUM=${1##*=} # hard coded by crab
NEVENT=${2##*=} # ordered by crab.py script
NTHREAD=${3##*=} # ordered by crab.py script
PROCNAME=${4##*=} # ordered by crab.py script
BEGINSEED=${5##*=}
if ! [ -z "$6" ]; then
  LHEPRODSCRIPT=${6##*=}
fi

WORKDIR=`pwd`

export SCRAM_ARCH=slc7_amd64_gcc700
export RELEASE=CMSSW_10_6_30
export RELEASE_HLT=CMSSW_9_4_14_UL_patch1
source /cvmfs/cms.cern.ch/cmsset_default.sh

if [ -r $RELEASE/src ] ; then
  echo release $RELEASE already exists
else
  scram p CMSSW $RELEASE
fi
cd $RELEASE/src
eval `scram runtime -sh`
CMSSW_BASE_ORIG=${CMSSW_BASE}

# customize CMSSW code

mkdir $CMSSW_BASE/src/GeneratorInterface
cp -rf /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/cmssw/$CMSSW_VERSION/src/GeneratorInterface/{Core,LHEInterface} $CMSSW_BASE/src/GeneratorInterface/
# copy customized LHE production script
cp -f $WORKDIR/inputs/scripts/{lhe_modifier.py,run_instMG.sh} GeneratorInterface/LHEInterface/data/
# use customized LHE production script, if specified
if ! [ -z $LHEPRODSCRIPT ]; then
  cp -f $WORKDIR/inputs/scripts/$LHEPRODSCRIPT GeneratorInterface/LHEInterface/data/
  sed -i "s|run_generic_tarball_cvmfs.sh|${LHEPRODSCRIPT}|g" GeneratorInterface/Core/src/BaseHadronizer.cc
else
  sed -i "s|run_generic_tarball_cvmfs.sh|run_instMG.sh|g" GeneratorInterface/Core/src/BaseHadronizer.cc
fi

# copy the fragment
mkdir -p Configuration/GenProduction/python/
cp $WORKDIR/fragments/${PROCNAME}.py Configuration/GenProduction/python/${PROCNAME}.py
# replace the event number
# NOTE: this routine does not specify NEVENT in the fragment
# grep -q "__NEVENT__" Configuration/GenProduction/python/${PROCNAME}.py || exit $? ;
sed "s/__NEVENT__/$NEVENT/g" -i Configuration/GenProduction/python/${PROCNAME}.py
eval `scram runtime -sh`
scram b -j $NTHREAD

cd $WORKDIR

# following workflows 20UL chain
# copied from https://cms-pdmv.cern.ch/mcm/chained_requests?contains=SUS-RunIISummer20UL17NanoAODv9-00044&page=0&shown=15

# begin LHEGEN
# SEED=$(($(date +%s) % 100000 + 1))
# SEED=$((${BEGINSEED} + ${JOBNUM}))
SEED=$(((${BEGINSEED} + ${JOBNUM}) * 100))

# need to specify seeds otherwise gridpacks will be chosen from the same routine!!
# remember to identify process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" and externalLHEProducer->generator!!
cmsDriver.py Configuration/GenProduction/python/${PROCNAME}.py --python_filename wmLHEGEN_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN --fileout file:lhegen.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.RandomNumberGeneratorService.generator.initialSeed="int(${SEED})"\\nprocess.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" --step GEN --geometry DB:Extended --era Run2_2017 --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;

# begin SIM
cmsDriver.py --python_filename SIM_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:sim.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --geometry DB:Extended --filein file:lhegen.root --era Run2_2017 --runUnscheduled --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;

# begin DRPremix
# cmsDriver.py --python_filename DIGIPremix_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:digi.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX" --conditions 106X_mc2017_realistic_v6 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:sim.root --datamix PreMix --era Run2_2017 --runUnscheduled --mc --nThreads $NTHREAD -n $NEVENT > digi.log 2>&1 || exit $? ; # too many output, log into file 
# using provided DIGIPremix cfg
cmsRun inputs/scripts/DIGIPremix_UL2017_template_cfg.py maxEvents=$NEVENT nThreads=$NTHREAD

# begin HLT
# load new cmssw env
if [ -r $RELEASE_HLT/src ] ; then
  echo release $RELEASE_HLT already exists
else
  scram p CMSSW $RELEASE_HLT
fi
cd $RELEASE_HLT/src
eval `scram runtime -sh`
cd $WORKDIR
cmsDriver.py --python_filename HLT_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:hlt.root --conditions 94X_mc2017_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2e34v40 --geometry DB:Extended --filein file:digi.root --era Run2_2017 --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;

# begin RECO
# reload original env
cd ${CMSSW_BASE_ORIG}/src
eval `scram runtime -sh`
cd $WORKDIR

cmsDriver.py --python_filename RECO_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:reco.root --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:hlt.root --era Run2_2017 --runUnscheduled --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;

# # begin MiniAODv2
# cmsDriver.py --python_filename MiniAODv2_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:miniv2.root --conditions 106X_mc2017_realistic_v9 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein file:reco.root --era Run2_2017 --runUnscheduled --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;

# # begin NanoAODv9
# cmsDriver.py --python_filename NanoAODv9_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:nanov9.root --conditions 106X_mc2017_realistic_v9 --step NANO --filein file:miniv2.root --era Run2_2017,run2_nanoAOD_106Xv2 --no_exec --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;
# cmsRun -j FrameworkJobReport.xml NanoAODv9_cfg.py # produce FrameworkJobReport.xml in the last step


## Run MiniAODv2 with -j FrameworkJobReport.xml 
cmsDriver.py --python_filename MiniAODv2_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:miniv2.root --conditions 106X_mc2017_realistic_v9 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein file:reco.root --era Run2_2017 --runUnscheduled --no_exec --mc --nThreads $NTHREAD -n $NEVENT || exit $? ;
cmsRun -j FrameworkJobReport.xml MiniAODv2_cfg.py

# ############ Start DNNTuples ############
# # use CMSSW_11_1_0_pre8 which has Puppi V14
# export SCRAM_ARCH=slc7_amd64_gcc820
# scram p CMSSW CMSSW_11_1_0_pre8
# cd CMSSW_11_1_0_pre8/src
# eval `scram runtime -sh`

# git cms-addpkg PhysicsTools/ONNXRuntime
# # clone this repo into "DeepNTuples" directory
# git clone https://github.com/colizz/DNNTuples.git DeepNTuples -b dev-UL-hww
# # Use a faster version of ONNXRuntime
# $CMSSW_BASE/src/DeepNTuples/Ntupler/scripts/install_onnxruntime.sh
# scram b -j $NTHREAD

# # Must run inside the test folder..
# cd DeepNTuples/Ntupler/test/
# cmsRun DeepNtuplizerAK8.py inputFiles=file:${WORKDIR}/miniv2.root outputFile=${WORKDIR}/dnntuple.root
