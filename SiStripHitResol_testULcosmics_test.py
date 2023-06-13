from Configuration.AlCa.GlobalTag import GlobalTag
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("HitEff")
process.load("Configuration/StandardSequences/MagneticField_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

options = VarParsing.VarParsing ('analysis')
options.inputFiles = ''
options.parseArguments()


process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

file_list = open(options.inputFiles[0], 'r')

files = file_list.readlines()

UL = 1

if UL == 0:
    InputTagName = "ALCARECOSiStripCalCosmics"

    OutputRootFile = "hitresol_ALCARECO_1.root"

    fileNames = cms.untracked.vstring(
        "root://cms-xrd-global.cern.ch//store/data/Run2018C/Cosmics/ALCARECO/SiStripCalCosmics-UL18-v1/40000/68F16890-CF8F-284A-8818-EF0E0E786EFE.root")

else:
    InputTagName = "ALCARECOSiStripCalMinBias"

    OutputRootFile = options.inputFiles[0].replace(".txt", ".root")

    fileNames = cms.untracked.vstring(files)


process.source = cms.Source("PoolSource", fileNames=fileNames)
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")

# process.load("RecoLocalTracker.SiStripRecHitConverter.StripCPEfromTrackAngle_cfi")
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")

process.refitTracks = process.TrackRefitterP5.clone(
    src=cms.InputTag(InputTagName))

process.load("CalibTracker.SiStripHitResolution.SiStripHitResol_cff")
process.anResol.combinatorialTracks = cms.InputTag("refitTracks")
process.anResol.trajectories = cms.InputTag("refitTracks")

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(OutputRootFile)
                                   )

process.allPath = cms.Path(process.MeasurementTrackerEvent *
                           process.offlineBeamSpot*process.refitTracks*process.hitresol)
