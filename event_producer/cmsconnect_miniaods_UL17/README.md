# MiniAOD production for training/test samples

This directory contains all samples to be produced in the current 15-250 GeV mass range.

To launch *all training samples* (on cmsconnect):
 - all samples used for training are defined in the .jdl files in [`jdl/train`](jdl/train);
 - do `condor_submit jdl/train/submit_XXX.jdl` for all jdl files in this directory;
 - the number of jobs to launch for each sample corresponds exactly to the samples used for current training.
 - output MiniAODs are transfered back to the specific subfolder in `output`;
 - in case of failures, use `condor_release <ClusterID>` to resubmit the failed jobs.

Note: remember to change the `BEGINSEED` in the condor jdl file so that the produced LHE events are not overlapping.

## To submit 
e.g.:
condor_submit jdl/train/submit_hbs_highmass.jdl