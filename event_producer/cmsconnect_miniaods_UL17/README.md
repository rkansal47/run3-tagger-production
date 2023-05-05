# MiniAOD production for training/test samples

This directory contains all samples to be produced in the current 15-250 GeV mass range.

Number of jobs to launch for each sample corresponds exactly to the samples used for current training.

To launch all sample production (on cmsconnect):
 - for all .jdl files in `jdl/train` `submit_xxx.jdl`;
 - do `condor_submit jdl/train/submit_XXX.jdl` in this directory;
 - output MiniAODs are transfered back to the specific subfolder in `output`;
 - in case of failures, use `condor_release <ClusterID>` to resubmit again.

Note: remember to change the `BEGINSEED` in the condor jdl file so that the produced LHE events are not overlapping.
