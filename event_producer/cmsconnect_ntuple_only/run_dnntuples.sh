#!/bin/bash -x

INPUTFILES=$1
WORKDIR=`pwd`

source /cvmfs/cms.cern.ch/cmsset_default.sh

############ Start DNNTuples ############
# use CMSSW_11_1_0_pre8 which has Puppi V14
export SCRAM_ARCH=slc7_amd64_gcc820
scram p CMSSW CMSSW_11_1_0_pre8
cd CMSSW_11_1_0_pre8/src
eval `scram runtime -sh`

git cms-addpkg PhysicsTools/ONNXRuntime
# clone this repo into "DeepNTuples" directory
git clone https://github.com/colizz/DNNTuples.git DeepNTuples -b dev-UL-hww
# Use a faster version of ONNXRuntime
$CMSSW_BASE/src/DeepNTuples/Ntupler/scripts/install_onnxruntime.sh
scram b

cd DeepNTuples/Ntupler/test/

### process files iteratively
IFS=',' read -ra ADDR <<< "$INPUTFILES"
idx=0
for infile in "${ADDR[@]}"; do
  echo $infile $idx
  cmsRun DeepNtuplizerAK8.py inputFiles=${infile}
  mv output.root dnntuple_raw${idx}.root
  idx=$(($idx+1))
done
if [ $idx == 1 ]; then
  mv dnntuple_raw0.root dnntuple.root
else
  hadd dnntuple.root dnntuple_raw*.root
fi
### end processing file

mv dnntuple.root ${WORKDIR}/dnntuple.root
