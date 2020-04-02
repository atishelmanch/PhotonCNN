#!/usr/bin/env cmsRun

import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils

process = cms.Process("Analysis")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.source = cms.Source ("PoolSource",
                # fileNames = cms.untracked.vstring("file:abeMicroAODTest.root"),
                  
                # fileNames = cms.untracked.vstring("/store/user/spigazzi/flashgg/Era2016_RR-07Aug17_v1/legacyRun2TestV1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/Era2016_RR-07Aug17_v1-legacyRun2TestV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/190228_142907/0000/myMicroAODOutputFile_610.root"),  
                # GJet_Pt-20to40 file 
                fileNames = cms.untracked.vstring("/store/group/phys_higgs/cmshgg/atishelm/flashgg/GJet20to40/RunIIFall18-4_0_0-75-g71c3c6e9/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/GJet20to40-RunIIFall18-4_0_0-75-g71c3c6e9-v0-atishelm-crab_RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2-6da13d8da7acaa38134e2095306b5773/191129_004819/0000/myMicroAODOutputFile_77.root"),
            )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1 )
# process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = '94X_mc2017_realistic_v10'

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("test.root")
)

# process.load("flashgg.Taggers.flashggUpdatedIdMVADiPhotons_cfi") 
process.load("PhotonCNN.Taggers.flashggUpdatedIdMVADiPhotons_cfi") 
process.flashggUpdatedIdMVADiPhotons.reRunRegression = cms.bool(False)
process.flashggUpdatedIdMVADiPhotons.doNon5x5transformation = cms.bool(False)
process.flashggUpdatedIdMVADiPhotons.do5x5correction = cms.bool(False)
process.flashggUpdatedIdMVADiPhotons.doIsoCorrection = cms.bool(False)

# from flashgg.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
from PhotonCNN.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
process.kinPreselDiPhotons = flashggPreselectedDiPhotons.clone(
src = cms.InputTag("flashggUpdatedIdMVADiPhotons"),
cut=cms.string(
        "mass > 95"
        " && leadingPhoton.pt > 18 && subLeadingPhoton.pt > 18"
        " && abs(leadingPhoton.superCluster.eta)<2.5 && abs(subLeadingPhoton.superCluster.eta)<2.5 "
        " && ( abs(leadingPhoton.superCluster.eta)<1.4442 || abs(leadingPhoton.superCluster.eta)>1.566)"
        " && ( abs(subLeadingPhoton.superCluster.eta)<1.4442 || abs(subLeadingPhoton.superCluster.eta)>1.566)"
        " && (leadingPhoton.pt > 14 && leadingPhoton.hadTowOverEm < 0.15 && (leadingPhoton.full5x5_r9>0.8 || leadingPhoton.chargedHadronIso<20 || leadingPhoton.chargedHadronIso<(0.3*leadingPhoton.pt)))"
        " && (subLeadingPhoton.pt > 14 && subLeadingPhoton.hadTowOverEm < 0.15 && (subLeadingPhoton.full5x5_r9>0.8 || subLeadingPhoton.chargedHadronIso<20 || subLeadingPhoton.chargedHadronIso<(0.3*subLeadingPhoton.pt)))"
        )
)


process.flashggSinglePhotonViews = cms.EDProducer("FlashggSinglePhotonViewProducer",
                                                  DiPhotonTag=cms.InputTag('kinPreselDiPhotons'),                                         
                                                  maxCandidates = cms.int32(1),
                                                  EBreducedEcalRecHits                 = cms.InputTag("reducedEcalRecHitsEB"),
                                                  EEreducedEcalRecHits                 = cms.InputTag("reducedEcalRecHitsEE")
                                                  )

# process.load("flashgg.Taggers.photonViewDumper_cfi") ##  import diphotonDumper 
process.load("PhotonCNN.Taggers.photonViewDumper_cfi") ##  import diphotonDumper 
# import flashgg.Taggers.dumperConfigTools as cfgTools
import PhotonCNN.Taggers.dumperConfigTools as cfgTools

process.photonViewDumper.src = "flashggSinglePhotonViews"
process.photonViewDumper.dumpTrees = True
process.photonViewDumper.dumpWorkspace = False
process.photonViewDumper.quietRooFit = True


## list of variables to be dumped in trees/datasets. Same variables for all categories
variables=[
           "pt                     := photon.pt",
        #    "energy                 := photon.energy",
           "eta                    := photon.eta", # What's the difference between photon eta and photon supercluster eta?
           "phi                    := photon.phi",
           "scEta                  := photon.superCluster.eta", 
           "scPhi                  := photon.superCluster.phi", 
           "DOF1                   := DOF1",
           "DOF2                   := DOF2",
           "DOF3                   := DOF3"
        #    "SCRawE                 := photon.superCluster.rawEnergy",
        #    "etaWidth               := photon.superCluster.etaWidth",
        #    "phiWidth               := photon.superCluster.phiWidth",
        #    "covIphiIphi            := photon.sipip",
        #    "chgIsoWrtWorstVtx      := photon.pfChgIsoWrtWorstVtx03",
        #    "phoIso03               := photon.pfPhoIso03",
        #    "phoIsoCorr             := photon.pfPhoIso03Corr",
        #    "chgIsoWrtChosenVtx     := pfChIso03WrtChosenVtx",
        #    "hcalTowerSumEtConeDR03 := photon.hcalTowerSumEtConeDR03",
        #    "trkSumPtHollowConeDR03 := photon.trkSumPtHollowConeDR03",
        #    "hadTowOverEm           := photon.hadTowOverEm",
        #    "idMVA                  := phoIdMvaWrtChosenVtx",
        #    #"genIso                 := photon.userFloat('genIso')", 
        #    "eTrue                  := ? photon.hasMatchedGenPhoton ? photon.matchedGenPhoton.energy : 0",
        #    "sigmaIetaIeta          := photon.full5x5_sigmaIetaIeta",
        #    "r9                     := photon.full5x5_r9", 
        #    "esEffSigmaRR           := photon.esEffSigmaRR",
        #    "s4                     := photon.s4",
        #    "covIEtaIPhi            := photon.sieip",
        #    "esEnergy               := photon.superCluster.preshowerEnergy",
        #    "esEnergyOverRawE       := photon.superCluster.preshowerEnergy/photon.superCluster.rawEnergy",
        #    "ieta_0                 := ietas[0]",
        #    "iphi_0                 := iphis[0]",
        #    "recHit_0                := recHits[0]",
        #    "ietas                  := map(ietas::170,-85,85::ietas[0],ietas[1])"
        #    "recH"



           #"rho                    := global.rho",
           #"esEnergyPlane1         := photon.esEnergyPlane1",
           #"esEnergyPlane2         := photon.esEnergyPlane2",
           #"e1x3                   := photon.e1x3",
           #"e2x5max                := photon.e2x5max",
           #"e5x5                   := photon.e5x5"
           ]

# Doing this because don't know how to save a vector in variables

num_rec_hits = 100

# "jet0_pt                         := ? JetVector.size() >= 1 ? JetVector[0].pt() : -99 "
# "ietas_0                         := ? ietas.size()     >= 1 ? ietas[0]          : -9999 "
# variables.append("ietas_size := ietas.size()")
# variables.append("iphis_size := iphis.size()")
# variables.append("recHits_size := recHits.size()")
# variables.append("ieta_0 := ? ietas.size() >= 1 ? ietas[0] : -9999")
for i in range(num_rec_hits):
        variables.append("DOF1s_" + str(i) + " := DOF1s[" + str(i) + "] ")
        variables.append("DOF2s_" + str(i) + " := DOF2s[" + str(i) + "] ")
        variables.append("DOF3s_" + str(i) + " := DOF3s[" + str(i) + "] ")
        variables.append("recHit_" + str(i) + " := recHits[" + str(i) + "] ")
                
        # print"var = ","ietas_" + str(i) + " := ? ietas.size() >= " + str(i+1) + " ? ietas[" + str(i) + "] : -9999 "
        # variables.append("ietas_" + str(i) + " := ? ietas.size() >= " + str(i+1) + " ? ietas[" + str(i) + "] : -9999 ")
        # variables.append("iphis_" + str(i) + " := ? iphis.size() >= " + str(i+1) + " ? iphis[" + str(i) + "] : -9999 ")
        # variables.append("recHit_" + str(i) + " := ? recHits.size() >= " + str(i+1) + " ? recHits[" + str(i) + "] : -9999 ")

# variables.append("ietas_0 := ietas[0]")
# print'variables = ',variables 

## list of histograms to be plotted
histograms=[
            "r9>>r9(110,0,1.1)",
            "scEta>>scEta(100,-2.5,2.5)",
        #     "ietas>>ietas(170,-85,85)",
        #     "iphis>>iphis(720,-360,360)",
        #     "recHits>>recHits(1000,0,100)",
            ]

## define categories and associated objects to dump
cfgTools.addCategory(process.photonViewDumper,
                     "Reject",
                     "abs(photon.superCluster.eta)>=1.4442&&abs(photon.superCluster.eta)<=1.566||abs(photon.superCluster.eta)>=2.5",
                     -1 ## if nSubcat is -1 do not store anythings
                     )

# interestng categories 
cfgTools.addCategories(process.photonViewDumper,
                       ## categories definition
                       ## cuts are applied in cascade. Events getting to these categories have already failed the "Reject" selection
                       [("promptPhotons","photon.genMatchType == 1",0), 
                        ("fakePhotons",  "photon.genMatchType != 1",0),
                        ],
                       ## variables to be dumped in trees/datasets. Same variables for all categories
                       ## if different variables wanted for different categories, can add categorie one by one with cfgTools.addCategory
                       variables=variables,
                       ## histograms to be plotted. 
                       ## the variables need to be defined first
                       histograms=histograms,
                       )

# process.p = cms.Path(process.flashggUpdatedIdMVADiPhotons*
process.p = cms.Path( 

                      process.flashggUpdatedIdMVADiPhotons*
                      process.kinPreselDiPhotons*
                      process.flashggSinglePhotonViews*
                      process.photonViewDumper

                      )


# from flashgg.MetaData.JobConfig import customize
from PhotonCNN.MetaData.JobConfig import customize
customize.setDefault("maxEvents",10000)
customize(process)
