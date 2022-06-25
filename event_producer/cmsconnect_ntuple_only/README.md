# Run DNNTuple step on CMSConnect

```bash
# Run following commands in this directory

mkdir output log # important!
voms-proxy-init -voms cms -valid 192:00

condor_submit jdl/test/submit_w_test.jdl
```