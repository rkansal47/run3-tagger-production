#!/bin/bash -xe

INPUTFILES=$1
WORKDIR=`pwd`

source /cvmfs/cms.cern.ch/cmsset_default.sh

############ Start DNNTuples ############
export SCRAM_ARCH=slc7_amd64_gcc700
scram p CMSSW CMSSW_10_6_30
cd CMSSW_10_6_30/src
eval `scram runtime -sh`

# use an updated onnxruntime package
bash <(curl -s https://raw.githubusercontent.com/colizz/DNNTuples/dev-UL-hww/Ntupler/scripts/install_onnxruntime.sh)

# clone this repo into "DeepNTuples" directory
git clone https://github.com/colizz/DNNTuples.git DeepNTuples -b dev-UL-hww

scram b

cd DeepNTuples/Ntupler/test/

function retry {
  local n=1
  local max=10
  local delay=5
  while true; do
    "$@" && break || {
      if [[ $n -lt $max ]]; then
        ((n++))
        echo "Command failed. Attempt $n/$max:"
        sleep $delay;
      else
        echo "The command has failed after $n attempts."
        return 1
      fi
    }
  done
}

### process files iteratively
IFS=',' read -ra ADDR <<< "$INPUTFILES"
idx=0
for infile in "${ADDR[@]}"; do
  echo $infile $idx
  retry cmsRun DeepNtuplizerAK8.py inputFiles=${infile}
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
