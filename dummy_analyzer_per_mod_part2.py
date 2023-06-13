from ROOT import TFile, TH1F
from math import sqrt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputFile", help="input file")
args = parser.parse_args()

inputFile = args.inputFile

def get_name(detId):
    return ["", "", "", "TIB", "TID", "TOB", "TEC"][get_subdet(detId)]+f" Layer {get_layer(detId)}"


def get_subdet(detId):
    return ((detId >> 25) & 0x7)


def get_layer(detId):
    return (detId >> 14) & 0x7


def sign(x):
    if x == 0:
        return 0
    return -1+2*(x > 0)


ff = TFile(str(inputFile), "READ")

tt = ff.Get("anResol/reso")
for bb in tt.GetListOfBranches():
    print(bb)
    
pitches = {}
for i in range(6):
    pitches[i] = set()

hist_dd = {}
hist_te = {}

detId_nclust = {}
for entry in tt:
    subDet = get_name(entry.detID1)
    pitch = entry.pitch1
    if entry.momentum < 3 or entry.pairPath > 7:  # or entry.trackChi2 > 1e-3:
        continue
    # if entry.clusterW1 != entry.clusterW2:
    #     continue
    if entry.clusterW1 > 4 or entry.clusterW2 > 4:
        continue
    if entry.numHits < 6:
        continue
    if entry.detID1 not in detId_nclust.keys():
        detId_nclust[entry.detID1] = 1
    else:
        detId_nclust[entry.detID1] += 1

    if entry.detID1 not in hist_dd.keys():
        hist_dd[entry.detID1] = TH1F("Double_difference_"+str(
            entry.detID1), "Double_difference_"+str(entry.detID1), 21, -0.021, 0.021)
        hist_te[entry.detID1] = TH1F(
            "Track_error_"+str(entry.detID1), "Track_error_"+str(entry.detID1), 21, 0, 0.021)
    # hist_dd[entry.detID1].Fill((entry.hitDX-entry.trackDX))
    # hist_te[entry.detID1].Fill(entry.trackDXE)


# # n = 0
# for x in detId_nclust:
#     if detId_nclust[x] > 20:
#         n+=1
#     # print(x, detId_nclust[x])
# print(n)

fo = TFile('/home/ucl/cp3/aguzel/CMSSW_13_1_0_pre1/src/CalibTracker/SiStripHitResolution/2023B-results/results_per_mod/result.root', "RECREATE")
fo.cd()

hist_res = {}

n = 0
for detId in hist_dd:
    dd = hist_dd[detId]
    te = hist_te[detId]
    if dd.GetEntries() > 20:
        dd.Fit("gaus", "lq")
        dde = dd.GetFunction("gaus").GetParameter(2)
        tte = te.GetMean()
        subDet = get_name(detId)
        if subDet not in hist_res.keys():
            hist_res[subDet] = TH1F(
                "Resolution"+subDet, "Resolution"+subDet, 25, 0, 0.01*10000)
        if tte < dde:
            hist_res[subDet].Fill(10000*sqrt(dde**2-tte**2)/sqrt(2))

for hh in hist_res:
    print(hh)
    hist_res[hh].Fit("gaus", "l")
    hist_res[hh].Write()

fo.Close()