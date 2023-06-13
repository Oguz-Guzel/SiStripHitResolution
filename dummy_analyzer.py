from ROOT import TFile, TH1F, TCanvas, TGraph, TLegend, TLine
from math import sqrt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--FilesList", help="input files list txt file", type=str, required=True)
args = parser.parse_args()

inputFile = args.FilesList

files_list = [fileName.replace('\n', '') for fileName in open(inputFile, 'r').readlines()]

def get_name(detId):
    return ["","","","TIB","TID","TOB","TEC"][get_subdet(detId)]+f" Layer {get_layer(detId)}"

def get_subdet(detId):
    return((detId>>25)&0x7)

def get_layer(detId):
    return (detId>>14)&0x7

def sign(x):
    if x == 0:
        return 0
    return -1+2*(x>0)

hist_dd = {}
hist_te = {}
pitches = {}

for file in files_list:
    print("Opening file: "+str(file))
    ff = TFile(file, "READ")
    tt = ff.Get("anResol/reso")
    for entry in tt:
        subDet = get_name(entry.detID1)
        print(entry.detID1)
        pitch  = entry.pitch1
        if entry.momentum < 3 or entry.pairPath > 7:# or entry.trackChi2 > 1e-3:
            continue
        # if entry.clusterW1 != entry.clusterW2:
        #     continue
        if entry.clusterW1 > 4 or entry.clusterW2 > 4:
            continue
        if entry.numHits < 6:
            continue

        if subDet not in hist_dd.keys():
            hist_dd[subDet] = TH1F("Double_difference_"+str(subDet),"Double_difference_"+str(subDet),21,-0.021,0.021)
            hist_te[subDet] = TH1F("Track_error_"+str(subDet),"Track_error_"+str(subDet),21,0,0.021)
            pitches[subDet] = pitch
        hist_dd[subDet].Fill((entry.hitDX-entry.trackDX))
        hist_te[subDet].Fill(entry.trackDXE)
    
    for subdetector in hist_dd:
        hist_dd[subdetector].SetDirectory(0)
        hist_te[subdetector].SetDirectory(0)


fo = TFile('/home/users/a/g/aguzel/CMSSW_13_1_0_pre1/src/CalibTracker/SiStripHitResolution/2023B-results/results_non_per_mod/'+str(inputFile).replace('.root', '_result.root').replace('outputs', ''), "RECREATE")
fo.cd()

res= {}


for subDet in hist_dd:
    dd = hist_dd[subDet]
    te = hist_te[subDet]
    if dd.GetEntries() > 20:
        dd.Fit("gaus","lq")
        dde = dd.GetFunction("gaus").GetParameter(2)
        tte = te.GetMean()
        dd.Write()
        te.Write()
        res[subDet] = 10000*sqrt(dde**2-tte**2)/sqrt(2)

detectors = [dd for dd in hist_dd]

from array import array
c = TCanvas("my_canvas","my_canvas",1000,1000)

gg = TGraph(len(detectors),array("f",[10000*pitches[s] for s in detectors]) , array("f",[res[s] for s in detectors]))
gg.Draw("AP")
gg.SetTitle("First try at hit resolution")
gg.SetMarkerStyle(20)
mp = 1.1*max([10000*pitches[d] for d in detectors])
gg.GetXaxis().SetLimits(0,mp)
gg.GetXaxis().SetTitle("Strip pitch [um]")
gg.GetYaxis().SetTitle("Hit Resolution [um]")
gg.GetYaxis().SetRangeUser(0,mp/sqrt(12))
leg = TLegend(0.2,0.7,0.52,0.8)
leg.AddEntry(gg,"TIB & TOB layers","p")

ll = TLine(0,0,mp,mp/sqrt(12))
ll.SetLineStyle(10)
ll.Draw("same")
leg.AddEntry(ll,"pitch/sqrt(12)","l")
leg.Draw("same")
gg.Write("res_vs_pitch")
c.Write("my_canvas")
fo.Close()