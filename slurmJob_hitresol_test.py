from CP3SlurmUtils.Configuration import Configuration

config = Configuration()

#--------------------------------------------------------------------------------
# 1. SLURM sbatch command options
#--------------------------------------------------------------------------------

config.sbatch_partition = "cp3"
config.sbatch_qos = "cp3"
config.sbatch_chdir = "."
config.sbatch_memPerCPU = "2048"
config.sbatch_output = "/dev/null"
config.sbatch_error = "/dev/null"
config.sbatch_additionalOptions = []

#--------------------------------------------------------------------------------
# 2. User batch script parameters that are same for all jobs
#--------------------------------------------------------------------------------

config.scratchDir = "${LOCALSCRATCH}"
config.handleScratch = False

config.environmentType = ""
config.cmsswDir = ""

config.inputSandboxContent = []
config.inputSandboxDir = ""
config.inputSandboxFilename = ""

config.batchScriptsDir = config.sbatch_chdir + "/slurm_batch_scripts"
config.batchScriptsFilename = ""

config.stageout = True
config.stageoutFiles = []
# We chose the filename of the outputs to be independent of the job array id number (but dependent on the job array task id number).
# So let's put the output files in a directory whose name contains the job array id number,
# so that each job array we may submit will write in a different directory.
config.stageoutDir = config.sbatch_chdir + "/slurm_outputs/job_array_${SLURM_ARRAY_JOB_ID}"

config.writeLogsOnWN = True
config.separateStdoutStderrLogs = False
config.stdoutFilename = ""
config.stderrFilename = ""
config.stageoutLogs = True
# The default filename of the slurm logs has already a job array id number and a job array task id number in it.
# So we can put all logs together (even from different job arrays we may submit) in a unique directory; they won't overwrite each other.
config.stageoutLogsDir = config.sbatch_chdir + "/slurm_logs"

config.useJobArray = True
config.maxRunningJobs = None

# 2 jobs will be submitted, because the config parameter 'inputParams' has length 2.
config.numJobs = None

#--------------------------------------------------------------------------------
# 3 Job-specific input parameters and payload
#--------------------------------------------------------------------------------

config.inputParamsNames = ['inputFile']

config.inputParams = [[file.replace('\n', '')] for file in open('filesList.txt', 'r').readlines()]

config.payload = \
"""
cd /home/ucl/cp3/aguzel/CMSSW_13_1_0_pre1/src/
eval `scramv1 runtime -sh`
cd CalibTracker/SiStripHitResolution/2023C/
cmsRun test/SiStripHitResol_testULcosmics_test.py inputFiles=/home/ucl/cp3/aguzel/CMSSW_13_1_0_pre1/src/CalibTracker/SiStripHitResolution/2023C/${inputFile}
"""
