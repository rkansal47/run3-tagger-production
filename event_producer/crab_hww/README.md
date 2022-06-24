## HWW training sample producer with `crab`

1. Setup the CMSSW env, then create the tarball `cmssw.tar.gz`. The tarball is put to `inputs/` which will be sent to crab:

```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv

git cms-addpkg GeneratorInterface/Core
git cms-addpkg GeneratorInterface/LHEInterface
rsync ../../data/{run_generic_tarball_cvmfs_JHUVariableWMass.sh,lhe_modifier.py} GeneratorInterface/LHEInterface/data/
rsync ../../data/BaseHadronizer.cc GeneratorInterface/Core/src/

tar czf ../../inputs/cmssw.tar.gz GeneratorInterface

scram b -j4
cd ../..
```

2. Submit the crab job. An example is provided in `crab_example_cfg.py`. (please launch a small number of events for test first)
xw