import ROOT as R
from ROOT import RooDataHist, RooHistPdf, RooArgList, RooFit, RooArgSet

# Root files used to make model
f1 = 'Files/Nominal/g3_zp125_70_230_nominal_result.root'
f2 = 'Files/Nominal/g3_zp175_70_230_nominal_result.root'

# To Check against, I'm using the 150 GeV value and checking it
f3 = 'Files/Nominal/g3_zp150_70_230_nominal_result.root'

# Take in files and make histograms
# Z = 125 GeV
file1 = R.TFile(f1)
hist1 = file1.Get('my_model_hist')
hist1.SetDirectory(0)
hist1_events = hist1.Integral()
# Z = 175 GeV
file2 = R.TFile(f2)
hist2 = file2.Get('my_model_hist')
hist2.SetDirectory(0)
hist2_events = hist2.Integral()

# Not to be included in the Moment Morphing (just a check)
file3 = R.TFile(f3)
hist3 = file3.Get('my_model_hist')
hist3.SetDirectory(0)
hist3_events = hist3.Integral()

# Setup Workspace and frame
w = R.RooWorkspace('w')
x = w.factory('x[70,230]')
x.setBins(32)
frame = x.frame()

# Z = 125 GeV
data_hist1 = RooDataHist('dhist1', 'dhist1', RooArgList(x), hist1)
pdf1 	   = RooHistPdf( 'phist1', 'phist1', RooArgSet(x), data_hist1)
pdf1.plotOn(frame, RooFit.LineColor(R.kGreen), RooFit.Normalization(hist1_events))
# Z = 175 GeV
data_hist2 = RooDataHist('dhist2', 'dhist2', RooArgList(x), hist2)
pdf2 	   = RooHistPdf( 'phist2', 'phist2', RooArgSet(x), data_hist2)
pdf2.plotOn(frame, RooFit.LineColor(R.kGreen), RooFit.Normalization(hist2_events))

# Not to be included in the Moment Morphing (just a check)
data_hist3 = RooDataHist('dhist3', 'dhist3', RooArgList(x), hist3)
pdf3 	   = RooHistPdf( 'phist3', 'phist3', RooArgSet(x), data_hist3)
pdf3.plotOn(frame,RooFit.LineColor(R.kBlue), RooFit.Normalization(hist3_events))
data_hist3.plotOn(frame)
# Create a RooArgList to store pdfs and fill it
pdfs = RooArgList()
pdfs.add(pdf1)
pdfs.add(pdf2)

# Create a TVector and store model mass values in it
masses = [125, 175]
paramVec = R.TVectorD(len(masses))
paramVec[0] = masses[0]
paramVec[1] = masses[1]

# Set up morphing
m = w.factory('m[70,230]')
setting = R.RooMomentMorph.Linear
morph = R.RooMomentMorph('morph', 'morph', m, RooArgList(x), pdfs, paramVec, setting)
getattr(w, 'import')(morph)

# Pick an interpolation value (150 in this case to check against real value)
m.setVal(150)
# Signal Efficiency is linear, so I'll interpolate the number of events manually
numOfEvents = int((masses[0]*hist1_events + masses[1]*hist2_events)/(masses[0] + masses[1])) 
# Create a TFile to store this in.
# kTRUE removes statistical fluctuations in the data.
hist = morph.generateBinned(RooArgSet(x), numOfEvents, R.kTRUE)
c1 = R.TCanvas('c1', 'c1', 1200, 900)
hist_pdf = RooHistPdf('phist', 'phist', RooArgSet(x), hist)
hist_pdf.plotOn(frame, RooFit.LineColor(R.kRed), RooFit.LineStyle(R.kDashed), RooFit.Normalization(1))
morph.plotOn(frame,RooFit.LineColor(R.kBlack))
myTH1 = hist.createHistogram('x',32)
myTH1.SaveAs('myInterpolation.root')
frame.SetXTitle('Z\' candidate large-R jet mass [GeV]')
frame.SetYTitle('Events/ (5 GeV)')
frame.SetTitle('RooMomentMorph Example')
frame.Draw()
raw_input()


