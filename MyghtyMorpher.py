import ROOT as R
from ROOT import RooDataHist, RooHistPdf, RooArgList, RooFit, RooArgSet
import os

###  Cole Helling, November 3rd 2018, UC Santa Cruz ###
# The purpose of this script is to read in template histograms at
# various masses (say 100, 125, 150, 175, and 200 in this case) 
# and produce interpolated histograms every 5 Gev or so.  Each
# new histogram is then saved as a separate root file.

############### VERSION 6 TODO LIST #############################
# Make a function to construct root filenames
	# should pass in val, possibly have it construct it 
	# automatically from the original string
# Make a function to get the correct number of events
	# I would imagine we could make a list of mass values and 
	# another with number of events, then fit a line
	# (or whatever) to it.  
# Fix the 'MakePDF' function.  Something needs to be done about 
	# the 1ms/2ms/3ms cases.
# Restructure the loop at the end
	# First loop will be the morphs
	# second loop will be interpolation values
# Find a more clever way to deal with files/directories if possible
################## END TODO LIST   ##############################



# Get the Directories for files inside the Files directory
DirectoryList = os.listdir('Files/')
# For storing the filenames to be looped over
Nominal_files   = []

Base_m1s_files  = []
Base_m2s_files  = []
Base_m3s_files  = []
Base_p1s_files  = []
Base_p2s_files  = []
Base_p3s_files  = []

Mod_m1s_files   = []
Mod_m2s_files   = []
Mod_m3s_files   = []
Mod_p1s_files   = []
Mod_p2s_files   = []
Mod_p3s_files   = []

Stat_m1s_files  = []
Stat_m2s_files  = []
Stat_m3s_files  = []
Stat_p1s_files  = []
Stat_p2s_files  = []
Stat_p3s_files  = []

Track_m1s_files = []
Track_m2s_files = []
Track_m3s_files = []
Track_p1s_files = []
Track_p2s_files = []
Track_p3s_files = []
# OtherThing_files = []

# TODO Can this be made better?
# Scans through the directories contained in 'Files/' and
# creates a directory listing for each.
for folder in DirectoryList:
	if 'Nominal' in folder:
		# get contents for 'Nominal' directory
		fileList = os.listdir('Files/Nominal/')
		for name in fileList:
			if name.endswith('.root'):
				Nominal_files.append('Files/Nominal/' + name)
        elif 'Base' in folder:
               	# get contents for 'Base' directory
		fileList = os.listdir('Files/Base/')
		for name in fileList:
			if name.endswith('.root'):
				if 'm1s' in name:
					Base_m1s_files.append('Files/Base/' + name)
				elif 'm2s' in name:
					Base_m2s_files.append('Files/Base/' + name)
				elif 'm3s' in name:
					Base_m3s_files.append('Files/Base/' + name)
				elif 'p1s' in name:
					Base_p1s_files.append('Files/Base/' + name)
				elif 'p2s' in name:
					Base_p2s_files.append('Files/Base/' + name)
				elif 'p3s' in name:
					Base_p3s_files.append('Files/Base/' + name)
	elif 'Mod' in folder:
		# get contents for 'Mod' directory
		fileList = os.listdir('Files/Mod/')
		for name in fileList:
			if name.endswith('.root'):
				if 'm1s' in name:
					Mod_m1s_files.append('Files/Mod/' + name)
				elif 'm2s' in name:
					Mod_m2s_files.append('Files/Mod/' + name)
				elif 'm3s' in name:
					Mod_m3s_files.append('Files/Mod/' + name)
				elif 'p1s' in name:
					Mod_p1s_files.append('Files/Mod/' + name)
				elif 'p2s' in name:
					Mod_p2s_files.append('Files/Mod/' + name)
				elif 'p3s' in name:
					Mod_p3s_files.append('Files/Mod/' + name)
	elif 'Stat' in folder:
		# get contents for 'Stat' directory
		fileList = os.listdir('Files/Stat/')
		for name in fileList:
			if name.endswith('.root'):
				if 'm1s' in name:
					Stat_m1s_files.append('Files/Stat/' + name)
				elif 'm2s' in name:
					Stat_m2s_files.append('Files/Stat/' + name)
				elif 'm3s' in name:
					Stat_m3s_files.append('Files/Stat/' + name)
				elif 'p1s' in name:
					Stat_p1s_files.append('Files/Stat/' + name)
				elif 'p2s' in name:
					Stat_p2s_files.append('Files/Stat/' + name)
				elif 'p3s' in name:
					Stat_p3s_files.append('Files/Stat/' + name)
	elif 'Track' in folder:
		# get contents for 'Track' directory
		fileList = os.listdir('Files/Track/')
		for name in fileList:
			if name.endswith('.root'):
				if 'm1s' in name:
					Track_m1s_files.append('Files/Track/' + name)
				elif 'm2s' in name:
					Track_m2s_files.append('Files/Track/' + name)
				elif 'm3s' in name:
					Track_m3s_files.append('Files/Track/' + name)
				elif 'p1s' in name:
					Track_p1s_files.append('Files/Track/' + name)
				elif 'p2s' in name:
					Track_p2s_files.append('Files/Track/' + name)
				elif 'p3s' in name:
					Track_p3s_files.append('Files/Track/' + name)
		
## ------------------------- Make inputfiles ------------------------- ##
# Constructs input files as a list filled with [(mass, filename),....]
# Which will be looped over later.
def inputFileMaker(fileList, inputFiles):
	for i in range(0,len(fileList)):
        	mass = int(fileList[i].partition("zp")[2].partition("_70")[0])
		inputFiles.append((mass, fileList[i])) 

## ----------------------- Fill paramVecs ---------------------------- ##
# Simply takes the mass values from the inputfiles and places it
# into a TVectorD object, which is required for RooMomentMorph
def fillParamVecs(paramVec, inputFiles):
	for i in range(len(inputFiles)):
		paramVec[i] = inputFiles[i][0]

## ------------------ Load Histograms -------------------------------- ##
# Takes the input filename, makes a TFile, and gets the histogram 
# named 'my_model_hist'.  Then set it to the primary directory (0).
def load_histos(filename):
        inputFile = R.TFile(filename)
        histo = inputFile.Get('my_model_hist')
        # Without this, the histogram returns 'none'
        histo.SetDirectory(0)
        return histo

## ----------------------- Make Pdfs --------------------------------- ##
# Loads histograms using the above function, then makes a RooDataHist 
# which in then made into a RooHistPdf.
# TODO  For now, this only helps with the p/m1s files.  I will either
# do away with this, or make it applicable to the 2 and 3 cases.
def makePDFs(Files, pdf_list):
	for (inputMass, inputFilename) in Files:		
		histo = load_histos(inputFilename)
		# could construct name and title from inputmass
		if 'nom' in inputFilename:
			myString = inputFilename.partition("230_")[2].partition("_result")[0] + str(inputMass)
		else:
			myString = inputFilename.partition("jes_")[2].partition("_result")[0] + str(inputMass) 
		# Convert the TH1F Histogram (data_hist) into a RooDataHist object
		data_hist = RooDataHist(myString, myString, RooArgList(x), histo)  
		# Turn the RooDataHist object into a RooHistPdf object
		pdf = RooHistPdf(myString, myString, RooArgSet(x), data_hist)
		# both the data_hist and pdf must survive
		pdf_list.append([data_hist,pdf])

def PdfAdd(pdfList, pdfArgList):
	for i in range(len(pdfList)):
		pdfArgList.add(pdfList[i][1])

# Used to hold the Zprime masses and filenames
Nominal_inputFiles  = []

Base_m1s_inputFiles = []
Base_m2s_inputFiles = []
Base_m3s_inputFiles = []
Base_p1s_inputFiles = []
Base_p2s_inputFiles = []
Base_p3s_inputFiles = []

Stat_m1s_inputFiles = []
Stat_m2s_inputFiles = []
Stat_m3s_inputFiles = []
Stat_p1s_inputFiles = []
Stat_p2s_inputFiles = []
Stat_p3s_inputFiles = []

Mod_m1s_inputFiles = []
Mod_m2s_inputFiles = []
Mod_m3s_inputFiles = []
Mod_p1s_inputFiles = []
Mod_p2s_inputFiles = []
Mod_p3s_inputFiles = []

Track_m1s_inputFiles = []
Track_m2s_inputFiles = []
Track_m3s_inputFiles = []
Track_p1s_inputFiles = []
Track_p2s_inputFiles = []
Track_p3s_inputFiles = []

# Used to hold the Zprime masses
Nominal_paramVec  = R.TVectorD(len(Nominal_files))

Base_m1s_paramVec  = R.TVectorD(len(Base_m1s_files))
Base_m2s_paramVec  = R.TVectorD(len(Base_m2s_files))
Base_m3s_paramVec  = R.TVectorD(len(Base_m3s_files))
Base_p1s_paramVec  = R.TVectorD(len(Base_p1s_files))
Base_p2s_paramVec  = R.TVectorD(len(Base_p2s_files))
Base_p3s_paramVec  = R.TVectorD(len(Base_p3s_files))

Stat_m1s_paramVec  = R.TVectorD(len(Stat_m1s_files))
Stat_m2s_paramVec  = R.TVectorD(len(Stat_m2s_files))
Stat_m3s_paramVec  = R.TVectorD(len(Stat_m3s_files))
Stat_p1s_paramVec  = R.TVectorD(len(Stat_p1s_files))
Stat_p2s_paramVec  = R.TVectorD(len(Stat_p2s_files))
Stat_p3s_paramVec  = R.TVectorD(len(Stat_p3s_files))

Mod_m1s_paramVec   = R.TVectorD(len(Mod_m1s_files))
Mod_m2s_paramVec   = R.TVectorD(len(Mod_m2s_files))
Mod_m3s_paramVec   = R.TVectorD(len(Mod_m3s_files))
Mod_p1s_paramVec   = R.TVectorD(len(Mod_p1s_files))
Mod_p2s_paramVec   = R.TVectorD(len(Mod_p2s_files))
Mod_p3s_paramVec   = R.TVectorD(len(Mod_p3s_files))

Track_m1s_paramVec = R.TVectorD(len(Track_m1s_files))
Track_m2s_paramVec = R.TVectorD(len(Track_m2s_files))
Track_m3s_paramVec = R.TVectorD(len(Track_m3s_files))
Track_p1s_paramVec = R.TVectorD(len(Track_p1s_files))
Track_p2s_paramVec = R.TVectorD(len(Track_p2s_files))
Track_p3s_paramVec = R.TVectorD(len(Track_p3s_files))
# _paramVec = R.TVectorD(len( _files ))

# Input templates must be in order, otherwise coefficients
# end up negative.
inputFileMaker(Nominal_files, Nominal_inputFiles)
Nominal_inputFiles  = sorted(Nominal_inputFiles)

inputFileMaker(Base_m1s_files, Base_m1s_inputFiles)
inputFileMaker(Base_m2s_files, Base_m2s_inputFiles)
inputFileMaker(Base_m3s_files, Base_m3s_inputFiles)
inputFileMaker(Base_p1s_files, Base_p1s_inputFiles)
inputFileMaker(Base_p2s_files, Base_p2s_inputFiles)
inputFileMaker(Base_p3s_files, Base_p3s_inputFiles)
Base_m1s_inputFiles = sorted(Base_m1s_inputFiles)
Base_m2s_inputFiles = sorted(Base_m2s_inputFiles)
Base_m3s_inputFiles = sorted(Base_m3s_inputFiles)
Base_p1s_inputFiles = sorted(Base_p1s_inputFiles)
Base_p2s_inputFiles = sorted(Base_p2s_inputFiles)
Base_p3s_inputFiles = sorted(Base_p3s_inputFiles)

inputFileMaker(Mod_m1s_files, Mod_m1s_inputFiles)
inputFileMaker(Mod_m2s_files, Mod_m2s_inputFiles)
inputFileMaker(Mod_m3s_files, Mod_m3s_inputFiles)
inputFileMaker(Mod_p1s_files, Mod_p1s_inputFiles)
inputFileMaker(Mod_p2s_files, Mod_p2s_inputFiles)
inputFileMaker(Mod_p3s_files, Mod_p3s_inputFiles)
Mod_m1s_inputFiles = sorted(Mod_m1s_inputFiles)
Mod_m2s_inputFiles = sorted(Mod_m2s_inputFiles)
Mod_m3s_inputFiles = sorted(Mod_m3s_inputFiles)
Mod_p1s_inputFiles = sorted(Mod_p1s_inputFiles)
Mod_p2s_inputFiles = sorted(Mod_p2s_inputFiles)
Mod_p3s_inputFiles = sorted(Mod_p3s_inputFiles)

inputFileMaker(Stat_m1s_files, Stat_m1s_inputFiles)
inputFileMaker(Stat_m2s_files, Stat_m2s_inputFiles)
inputFileMaker(Stat_m3s_files, Stat_m3s_inputFiles)
inputFileMaker(Stat_p1s_files, Stat_p1s_inputFiles)
inputFileMaker(Stat_p2s_files, Stat_p2s_inputFiles)
inputFileMaker(Stat_p3s_files, Stat_p3s_inputFiles)
Stat_m1s_inputFiles = sorted(Stat_m1s_inputFiles)
Stat_m2s_inputFiles = sorted(Stat_m2s_inputFiles)
Stat_m3s_inputFiles = sorted(Stat_m3s_inputFiles)
Stat_p1s_inputFiles = sorted(Stat_p1s_inputFiles)
Stat_p2s_inputFiles = sorted(Stat_p2s_inputFiles)
Stat_p3s_inputFiles = sorted(Stat_p3s_inputFiles)

inputFileMaker(Track_m1s_files, Track_m1s_inputFiles)
inputFileMaker(Track_m2s_files, Track_m2s_inputFiles)
inputFileMaker(Track_m3s_files, Track_m3s_inputFiles)
inputFileMaker(Track_p1s_files, Track_p1s_inputFiles)
inputFileMaker(Track_p2s_files, Track_p2s_inputFiles)
inputFileMaker(Track_p3s_files, Track_p3s_inputFiles)
Track_m1s_inputFiles = sorted(Track_m1s_inputFiles)
Track_m2s_inputFiles = sorted(Track_m2s_inputFiles)
Track_m3s_inputFiles = sorted(Track_m3s_inputFiles)
Track_p1s_inputFiles = sorted(Track_p1s_inputFiles)
Track_p2s_inputFiles = sorted(Track_p2s_inputFiles)
Track_p3s_inputFiles = sorted(Track_p3s_inputFiles)

# Put mass values into the TVectors.
fillParamVecs(Nominal_paramVec , Nominal_inputFiles )

fillParamVecs(Base_m1s_paramVec, Base_m1s_inputFiles)
fillParamVecs(Base_m2s_paramVec, Base_m2s_inputFiles)
fillParamVecs(Base_m3s_paramVec, Base_m3s_inputFiles)
fillParamVecs(Base_m1s_paramVec, Base_m1s_inputFiles)
fillParamVecs(Base_m2s_paramVec, Base_m2s_inputFiles)
fillParamVecs(Base_m3s_paramVec, Base_m3s_inputFiles)

fillParamVecs(Mod_m1s_paramVec, Mod_m1s_inputFiles)
fillParamVecs(Mod_m2s_paramVec, Mod_m2s_inputFiles)
fillParamVecs(Mod_m3s_paramVec, Mod_m3s_inputFiles)
fillParamVecs(Mod_m1s_paramVec, Mod_m1s_inputFiles)
fillParamVecs(Mod_m2s_paramVec, Mod_m2s_inputFiles)
fillParamVecs(Mod_m3s_paramVec, Mod_m3s_inputFiles)

fillParamVecs(Stat_m1s_paramVec, Stat_m1s_inputFiles)
fillParamVecs(Stat_m2s_paramVec, Stat_m2s_inputFiles)
fillParamVecs(Stat_m3s_paramVec, Stat_m3s_inputFiles)
fillParamVecs(Stat_m1s_paramVec, Stat_m1s_inputFiles)
fillParamVecs(Stat_m2s_paramVec, Stat_m2s_inputFiles)
fillParamVecs(Stat_m3s_paramVec, Stat_m3s_inputFiles)

fillParamVecs(Track_m1s_paramVec, Track_m1s_inputFiles)
fillParamVecs(Track_m2s_paramVec, Track_m2s_inputFiles)
fillParamVecs(Track_m3s_paramVec, Track_m3s_inputFiles)
fillParamVecs(Track_m1s_paramVec, Track_m1s_inputFiles)
fillParamVecs(Track_m2s_paramVec, Track_m2s_inputFiles)
fillParamVecs(Track_m3s_paramVec, Track_m3s_inputFiles)

# Setup workspace, x variable, Canvas and frame
w = R.RooWorkspace('w')
x = w.factory('x[70,230]')
# This should set the binning correctly, but it doesn't
x.setBins(32)

# Make Histograms and PDFs and return them into an array
# Both need to 'survive' in order to use the pdfs
Nominal_pdf_list  = []

Base_m1s_pdf_list = []
Base_m2s_pdf_list = []
Base_m3s_pdf_list = []
Base_p1s_pdf_list = []
Base_p2s_pdf_list = []
Base_p3s_pdf_list = []

Mod_m1s_pdf_list = []
Mod_m2s_pdf_list = []
Mod_m3s_pdf_list = []
Mod_p1s_pdf_list = []
Mod_p2s_pdf_list = []
Mod_p3s_pdf_list = []

Stat_m1s_pdf_list = []
Stat_m2s_pdf_list = []
Stat_m3s_pdf_list = []
Stat_p1s_pdf_list = []
Stat_p2s_pdf_list = []
Stat_p3s_pdf_list = []

Track_m1s_pdf_list = []
Track_m2s_pdf_list = []
Track_m3s_pdf_list = []
Track_p1s_pdf_list = []
Track_p2s_pdf_list = []
Track_p3s_pdf_list = []

# Make the Pdfs	
makePDFs(Nominal_inputFiles , Nominal_pdf_list )

makePDFs(Base_m1s_inputFiles, Base_m1s_pdf_list)
makePDFs(Base_m2s_inputFiles, Base_m2s_pdf_list)
makePDFs(Base_m3s_inputFiles, Base_m3s_pdf_list)
makePDFs(Base_p1s_inputFiles, Base_p1s_pdf_list)
makePDFs(Base_p2s_inputFiles, Base_p2s_pdf_list)
makePDFs(Base_p3s_inputFiles, Base_p3s_pdf_list)

makePDFs(Mod_m1s_inputFiles, Mod_m1s_pdf_list)
makePDFs(Mod_m2s_inputFiles, Mod_m2s_pdf_list)
makePDFs(Mod_m3s_inputFiles, Mod_m3s_pdf_list)
makePDFs(Mod_p1s_inputFiles, Mod_p1s_pdf_list)
makePDFs(Mod_p2s_inputFiles, Mod_p2s_pdf_list)
makePDFs(Mod_p3s_inputFiles, Mod_p3s_pdf_list)

makePDFs(Stat_m1s_inputFiles, Stat_m1s_pdf_list)
makePDFs(Stat_m2s_inputFiles, Stat_m2s_pdf_list)
makePDFs(Stat_m3s_inputFiles, Stat_m3s_pdf_list)
makePDFs(Stat_p1s_inputFiles, Stat_p1s_pdf_list)
makePDFs(Stat_p2s_inputFiles, Stat_p2s_pdf_list)
makePDFs(Stat_p3s_inputFiles, Stat_p3s_pdf_list)

makePDFs(Track_m1s_inputFiles, Track_m1s_pdf_list)
makePDFs(Track_m2s_inputFiles, Track_m2s_pdf_list)
makePDFs(Track_m3s_inputFiles, Track_m3s_pdf_list)
makePDFs(Track_p1s_inputFiles, Track_p1s_pdf_list)
makePDFs(Track_p2s_inputFiles, Track_p2s_pdf_list)
makePDFs(Track_p3s_inputFiles, Track_p3s_pdf_list)

# Place the pdfs into a RooArgList
Nominal_pdfs  = RooArgList()

Base_m1s_pdfs = RooArgList()
Base_m2s_pdfs = RooArgList()
Base_m3s_pdfs = RooArgList()
Base_p1s_pdfs = RooArgList()
Base_p2s_pdfs = RooArgList()
Base_p3s_pdfs = RooArgList()

Mod_m1s_pdfs = RooArgList()
Mod_m2s_pdfs = RooArgList()
Mod_m3s_pdfs = RooArgList()
Mod_p1s_pdfs = RooArgList()
Mod_p2s_pdfs = RooArgList()
Mod_p3s_pdfs = RooArgList()

Stat_m1s_pdfs = RooArgList()
Stat_m2s_pdfs = RooArgList()
Stat_m3s_pdfs = RooArgList()
Stat_p1s_pdfs = RooArgList()
Stat_p2s_pdfs = RooArgList()
Stat_p3s_pdfs = RooArgList()

Track_m1s_pdfs = RooArgList()
Track_m2s_pdfs = RooArgList()
Track_m3s_pdfs = RooArgList()
Track_p1s_pdfs = RooArgList()
Track_p2s_pdfs = RooArgList()
Track_p3s_pdfs = RooArgList()


PdfAdd(Nominal_pdf_list , Nominal_pdfs )

PdfAdd(Base_m1s_pdf_list, Base_m1s_pdfs)
PdfAdd(Base_m2s_pdf_list, Base_m2s_pdfs)
PdfAdd(Base_m3s_pdf_list, Base_m3s_pdfs)
PdfAdd(Base_p1s_pdf_list, Base_p1s_pdfs)
PdfAdd(Base_p2s_pdf_list, Base_p2s_pdfs)
PdfAdd(Base_p3s_pdf_list, Base_p3s_pdfs)

PdfAdd(Mod_m1s_pdf_list, Mod_m1s_pdfs)
PdfAdd(Mod_m2s_pdf_list, Mod_m2s_pdfs)
PdfAdd(Mod_m3s_pdf_list, Mod_m3s_pdfs)
PdfAdd(Mod_p1s_pdf_list, Mod_p1s_pdfs)
PdfAdd(Mod_p2s_pdf_list, Mod_p2s_pdfs)
PdfAdd(Mod_p3s_pdf_list, Mod_p3s_pdfs)

PdfAdd(Stat_m1s_pdf_list, Stat_m1s_pdfs)
PdfAdd(Stat_m2s_pdf_list, Stat_m2s_pdfs)
PdfAdd(Stat_m3s_pdf_list, Stat_m3s_pdfs)
PdfAdd(Stat_p1s_pdf_list, Stat_p1s_pdfs)
PdfAdd(Stat_p2s_pdf_list, Stat_p2s_pdfs)
PdfAdd(Stat_p3s_pdf_list, Stat_p3s_pdfs)

PdfAdd(Track_m1s_pdf_list, Track_m1s_pdfs)
PdfAdd(Track_m2s_pdf_list, Track_m2s_pdfs)
PdfAdd(Track_m3s_pdf_list, Track_m3s_pdfs)
PdfAdd(Track_p1s_pdf_list, Track_p1s_pdfs)
PdfAdd(Track_p2s_pdf_list, Track_p2s_pdfs)
PdfAdd(Track_p3s_pdf_list, Track_p3s_pdfs)

# Linear Interpolation Setting
setting = R.RooMomentMorph.Linear

# For the interpolated mass points
m  = w.factory('m[70,230]')

Zords = [['_nominal_' , Nominal_pdfs   , Nominal_paramVec ],
	 ['_base_m1s_', Base_m1s_pdfs  , Base_m1s_paramVec],
	 ['_base_m2s_', Base_m2s_pdfs  , Base_m2s_paramVec], 
	 ['_base_m3s_', Base_m3s_pdfs  , Base_m3s_paramVec],
	 ['_base_p1s_', Base_p1s_pdfs  , Base_p1s_paramVec],
	 ['_base_p2s_', Base_p2s_pdfs  , Base_p2s_paramVec],
	 ['_base_p3s_', Base_p3s_pdfs  , Base_p3s_paramVec],
	 ['_mod_m1s_', Mod_m1s_pdfs    , Mod_m1s_paramVec],
	 ['_mod_m2s_', Mod_m2s_pdfs    , Mod_m2s_paramVec], 
	 ['_mod_m3s_', Mod_m3s_pdfs    , Mod_m3s_paramVec],
	 ['_mod_p1s_', Mod_p1s_pdfs    , Mod_p1s_paramVec],
	 ['_mod_p2s_', Mod_p2s_pdfs    , Mod_p2s_paramVec],
	 ['_mod_p3s_', Mod_p3s_pdfs    , Mod_p3s_paramVec],
	 ['_stat_m1s_', Stat_m1s_pdfs  , Stat_m1s_paramVec],
	 ['_stat_m2s_', Stat_m2s_pdfs  , Stat_m2s_paramVec], 
	 ['_stat_m3s_', Stat_m3s_pdfs  , Stat_m3s_paramVec],
	 ['_stat_p1s_', Stat_p1s_pdfs  , Stat_p1s_paramVec],
	 ['_stat_p2s_', Stat_p2s_pdfs  , Stat_p2s_paramVec],
	 ['_stat_p3s_', Stat_p3s_pdfs  , Stat_p3s_paramVec],
	 ['_track_m1s_', Track_m1s_pdfs, Track_m1s_paramVec],
	 ['_track_m2s_', Track_m2s_pdfs, Track_m2s_paramVec], 
	 ['_track_m3s_', Track_m3s_pdfs, Track_m3s_paramVec],
	 ['_track_p1s_', Track_p1s_pdfs, Track_p1s_paramVec],
	 ['_track_p2s_', Track_p2s_pdfs, Track_p2s_paramVec],
	 ['_track_p3s_', Track_p3s_pdfs, Track_p3s_paramVec]]


# Desired interpolation points
#interp = range(110,190,20)
# For debugging
interp = [130, 140]

def GetFilename(val, label):
	str0 = 'rootFiles/'
	str1 = 'g3_zp'
	str2 = str(val)
	str3 = '_70_230_jes'
	str4 = label
	str5 = 'result.root'
	if label == '_nominal_':
		filename = str0 + str1 + str2 + str3[:-4] + str4 + str5
	else:
		filename = str0 + str1 + str2 + str3 + str4 + str5
	
	return filename

def GetEventNumber(val, label):
	return 10000

# The morphed objects have the wrong binning, and I'm having trouble fixing it.
# For now, I'm creating a histo generated with 100k points and making a pdf from that.
# Super wasteful, I know... still working on it.
m = w.factory('m[70,230]')
for [label, pdfs, paramVec] in Zords:
	print("things are coming....................")
	print(label)
	pdfs.Print()
	paramVec.Print()
	morph = R.RooMomentMorph( label[1:-1], label[1:-1], m, RooArgList(x), pdfs, paramVec, setting)
	getattr(w, 'import')(label[1:-1])
	morph.Print() 
	c1 = R.TCanvas('c1', 'c1', 1200, 900)
	frame = x.frame()
	frame.SetXTitle('Z\' candidate large-R jet mass [GeV]')
	frame.SetYTitle(' ')
	frame.SetTitle('RooMomentMorphing with Histograms')
	for val in interp:
		m.setVal(val)
		SaveFilename = GetFilename(val, label)
		numEvents = GetEventNumber(val, label)
		hist = morph.generateBinned(RooArgSet(x), numEvents, R.kTRUE)
		hist.plotOn(frame)
		hist_TH1 = hist.createHistogram('x',32)
		hist_TH1.SaveAs(SaveFilename)


frame.Draw()
#c1.SaveAs('RooMomentMorph_Histograms.png')
raw_input()
