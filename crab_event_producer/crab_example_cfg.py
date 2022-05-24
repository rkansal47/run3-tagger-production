from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferLogs = False
config.General.transferOutputs = True
config.General.workArea = 'crab_projects_2017_mc_run1'
config.General.requestName = 'BulkGravitonToHHTo4W_MX-600to6000_MH-15to250_JHUVariableWMass_part1'
config.section_('JobType')
config.JobType.outputFiles = ['dnntuple.root']
config.JobType.numCores = 1
config.JobType.sendExternalFolder = True
config.JobType.scriptArgs = ['nevent=500', 'nthread=1', 'procname=BulkGravitonToHHTo4W_MX-600to6000_MH-15to250_JHUVariableWMass_part1', 'beginseed=0']
config.JobType.scriptExe = 'exe.sh'
config.JobType.pluginName = 'PrivateMC'
config.JobType.allowUndistributedCMSSW = True
config.JobType.psetName = 'FAKEMiniAODv2_cfg.py'
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'inputs']
config.JobType.maxMemoryMB = 2500
config.section_('Data')
config.Data.outputDatasetTag = 'DNNTuples_PrivateMC'
config.Data.totalUnits = 2000000
config.Data.unitsPerJob = 500
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.allowNonValidInputDataset = True
config.Data.outLFNDirBase = '/store/group/cmst3/group/vhcc/sfTuples/20220523_HWW_JHUVariableWMass/2017/mc'
config.Data.outputPrimaryDataset = 'BulkGravitonToHHTo4W_MX-600to6000_MH-15to250_JHUVariableWMass_part1'
config.Data.publication = False
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.section_('User')
config.section_('Debug')