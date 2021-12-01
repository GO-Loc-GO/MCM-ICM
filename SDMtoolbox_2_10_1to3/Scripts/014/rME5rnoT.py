# 
#-------------------------------------------------------------
# Name:       SpatialJackkinfeMaxentModel.py
# Purpose:    Runs a Maxent model using Stephen Phillips'
#             javascript Maxent application
# ArcGIS Version:   10.1-10.5
# Python Version:   2.7
# Author: Jason L. Brown
# Last revision:12/21/2018
#-------------------------------------------------------------
#
import arcpy, os, csv ,arcgisscripting, glob, math
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True
gp = arcgisscripting.create()


# get the location to the maxent jar file
MaxEntJar = arcpy.GetParameterAsText(0)
# Get the csv file to model
csvFile =arcpy.GetParameterAsText(1)
csvSpp =arcpy.GetParameterAsText(2)
x_coords =arcpy.GetParameterAsText(3)
y_coords =arcpy.GetParameterAsText(4)
# get the name of the folder containing the bioclimatic data
climatedataFolder = arcpy.GetParameterAsText(5)
climatedataFolderIN = climatedataFolder ##*new
# get categorical variables
catVars = arcpy.GetParameterAsText(6)
if catVars != "":
   catVarsTd= ""
   for i in catVars.split(';'):
      inASCII = str(i)
      outName = os.path.split(inASCII)[1]
      outNameSh = " -t "+str(outName)[:-4]
      try:
         catVarsTd += outNameSh
      except:
         arcpy.AddMessage("")
   catVarsT= catVarsTd

# exclude variables
excVars = arcpy.GetParameterAsText(7)
if excVars != "":
   excVarsTd= ""
   for i in excVars.split(';'):
      inASCII = str(i)
      outName = os.path.split(inASCII)[1]
      outNameSh = " -N "+str(outName)[:-4]
      try:
         excVarsTd += outNameSh
      except:
         arcpy.AddMessage("")
   excVarsT= excVarsTd
#input bias file
BiasFileFolder= arcpy.GetParameterAsText(8)

# get the name of the folder to save the Maxent model results to
outFolder = arcpy.GetParameterAsText(9)

#get the type of model to generate
optOutputFormat = arcpy.GetParameterAsText(10)

# get the type of output file to save
optOutputFileType = arcpy.GetParameterAsText(11)

# get options
optResponseCurves= arcpy.GetParameterAsText(12)
optPredictionPictures = arcpy.GetParameterAsText(13)
optJackknife = arcpy.GetParameterAsText(14)
optSkipifExists = arcpy.GetParameterAsText(15)
supressWarnings = arcpy.GetParameterAsText(16)
#regularization values
BVal=arcpy.GetParameterAsText(17).replace(" ","")
#threshold models#randomseed
doThres=arcpy.GetParameterAsText(18)#21

#projection stuff
#projection layers
ProLyrs = arcpy.GetParameterAsText(19)#28
if ProLyrs != "":
    ProLyrsTa = arcpy.GetParameterAsText(19).replace(";",",")
    ProLyrsT =" -j "+str(ProLyrsTa)+" "
#clamping
doClamp=arcpy.GetParameterAsText(20)#29
#extrapolate
doExtrp=arcpy.GetParameterAsText(21)#30
#Other, num of processors
OERthenAUCFull=arcpy.GetParameterAsText(22)
if OERthenAUCFull == "Omission error rate, then AUC":
    OERthenAUC= "OERtoAUC"
if OERthenAUCFull == "AUC, then Omission error rate":
    OERthenAUC= "AUCtoOER"
if OERthenAUCFull == "Maximum total AUC & Prediction rate (1-OER)":
    OERthenAUC= "maxPRandAUC"
#scriptPath = sys.path[0]
#GUI silent
nCPUin = arcpy.GetParameterAsText(23)#32
nCPU=int(nCPUin)
GUIsil = "true"
#spatialJacknife
sptJack=arcpy.GetParameterAsText(24)#33
#do not use threshold feature class
noTrshld=arcpy.GetParameterAsText(25)
#Minpoints to model
minMOD=arcpy.GetParameterAsText(26)#36
minModN= int(minMOD)
#MinNumvbertoJackknife
minJack=arcpy.GetParameterAsText(27)#36
minJackN= int(minJack)
#replicate number
pReps=arcpy.GetParameterAsText(28)#18
if int(pReps) > 0:
    pRepsSJ=" replicates="+ str(pReps)+ " randomseed randomtestpoints=25 replicatetype=subsample"
#spatialJacknifeGroups
sptJackGrp=arcpy.GetParameterAsText(29)#34
#spatialJacknifeType
sptJackT=arcpy.GetParameterAsText(30)#35
NSJpReps=arcpy.GetParameterAsText(31)#18
NSJpRepType=arcpy.GetParameterAsText(32)#19
if NSJpRepType!= 'crossvalidate':
  NSJpRepType+= ' randomseed=true'
if int(NSJpReps) > 1:
  NSJpRepsT=" replicates="+ str(NSJpReps)+ " replicatetype="+ NSJpRepType
# get name of species from input file
randTpts= arcpy.GetParameterAsText(33)#20
if int(randTpts) > 0:
  randTptsT=" randomtestpoints="+ str(randTpts)
##specify feature classes
FeatAut=arcpy.GetParameterAsText(34)#22
FeatLin=arcpy.GetParameterAsText(35)#23
FeatQua=arcpy.GetParameterAsText(36)#24
FeatHin=arcpy.GetParameterAsText(37)#25
FeatPrd=arcpy.GetParameterAsText(38)#26
FeatThr=arcpy.GetParameterAsText(39)#27 

# replicate number
STpReps=arcpy.GetParameterAsText(40)#18
STpRepType=arcpy.GetParameterAsText(41)#19
if STpRepType!= 'crossvalidate':
  STpRepType+= ' randomseed=true'
if int(STpReps) > 1:
  STpRepsT=" replicates="+ str(STpReps)+ " replicatetype="+ STpRepType 
# get name of species from input file
STrandTpts= arcpy.GetParameterAsText(42)#20
if int(STrandTpts) > 0:
  STrandTptsT=" randomtestpoints="+ str(STrandTpts)

Nthreads=nCPU


if doThres == "maximum test sensitivity plus specificity":
   doThres = "maximum training sensitivity plus specificity"
if doThres == "equal test sensitivity and specificity":
   doThres = "equal training sensitivity and specificity"

#Makesure no temp mask are lingering
ZzinMASKt = (climatedataFolder+"\\MaskTemp.asc").replace("\\","/")
if arcpy.Exists(ZzinMASKt):
  arcpy.Delete_management(ZzinMASKt) 

#########################################
##############END of INPUTS##############
#########################################

#########################################
########START Spatial Jackknife##########
#########################################
if sptJack =='true':
  gp.AddMessage("*******************************************")
  gp.AddMessage("*************Spatial Jackknife*************")
  arcpy.CreateFolder_management(outFolder,"TEMP_ilUli")
  arcpy.CreateFolder_management(outFolder,"TEMP_ilUlii")
  arcpy.CreateFolder_management(outFolder,"TEMP_ilUliii")
  outFolderTemp= outFolder + "/TEMP_ilUli"
  outFolderTemp2= outFolder + "/TEMP_ilUlii"
  outFolderTemp3= outFolder + "/TEMP_ilUliii"
  #get projection from climate data
  gp.workspace = climatedataFolder
  GridsProj = gp.ListRasters("", "ALL")
  GridProjA = GridsProj.next()
  sr=arcpy.Describe(GridProjA).spatialReference
  srUse=sr.factoryCode
  srName=sr.Name
  arcpy.env.extent = GridProjA
  arcpy.env.cellSize = GridProjA
  gp.AddMessage("Input grid used for spatial environment template: " + str(GridProjA))
  gp.AddMessage("Environmental Cell Size: " + str(arcpy.env.cellSize))
  gp.AddMessage("Projection in: " + str(srName))
  if srUse==0:
    gp.AddMessage("Please define the projection "+ str(GridProjA)+ " in your input climate data folder")
    del gp
  ####splitCSV_by_species
  outfileShp = outFolder + "/All_Occ.shp"
  ###convert table to shp
  infileShp = arcpy.MakeXYEventLayer_management(csvFile, x_coords, y_coords, "TEMP",srUse, "#")
  arcpy.CopyFeatures_management(infileShp, outfileShp)
  #### add unique ID
  arcpy.AddField_management(outfileShp,"UN_ID","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
  arcpy.CalculateField_management(outfileShp,"UN_ID","[FID] +1","VB","#")
  ###SPLIT SHAPEFILE BY SPECIES INTO FOLDER 2
  ########RUN CODE HERE######################
  from Scripts import MaxEnt
  ####Locate Python.exe
  PyLoc=os.__file__
  PyLocT=PyLoc.replace("Lib\\os.pyc","pythonw.exe").replace("/","\\")
  ####Create empty master batch files
  outFolderPy=outFolder.replace("\\","/")
  newLine =""
  file = open(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat", "w")
  file.write(newLine)
  file.close()
  file = open(outFolderPy+"/Step2_Run_Optimized_MaxEnt_Models.bat", "w")
  file.write(newLine)
  file.close()
  ##*new-start
  if nCPU > 1:
    nCPUi = [i for i in range(1,nCPU+1)]
    for i in nCPUi:
      if i == int(nCPU):
          file = open(outFolderPy+"\\_CPU"+str(i)+"_code.bat", "w")
          file.write(newLine)
          file.close()
      if i < int(nCPU):
          file = open(outFolderPy+"\\_CPU"+str(i)+"_code.bat", "w")
          file.write(newLine)
          file.close()
          import shutil
          SOURCE = climatedataFolder
          CLIMCOPY = outFolder + "\\_CPU"+str(i+1)+"_climate"
          # create a backup directory
          shutil.copytree(SOURCE, CLIMCOPY)
  ##*new-end
  #Makesure input and bias files names agree
  theFilesZz = glob.glob(outFolderTemp2+"/*.shp")
  ZzinName=str(theFilesZz[0]).replace("\\","/")
  ZzoutName = os.path.split(ZzinName)[1] 
  ZzoutNameSht = str(ZzoutName)[:-4]
  ZzinASCII = (BiasFileFolder + "/" + ZzoutNameSht +".asc").replace("\\","/")
  if (not arcpy.Exists(ZzinASCII)):
       arcpy.AddMessage("**********************************************")
       arcpy.AddMessage("**********************************************")
       arcpy.AddMessage("ERROR.... FILE NAME     " + ZzinASCII + " DOES NOT EXIST.  Please ensure your bias file names match this format: "+ ZzinASCII + ".asc")
       arcpy.AddMessage("**********************************************")
       arcpy.AddMessage("**********************************************")
       sys.exit(0)
  ##########################################
  #####RUN FOR EACH SPECIES#################
  ##########################################
  theFilesA = glob.glob(outFolderTemp2+"/*.shp")
  ##*new-start
  nSppR = -1
  nSppRLabel = 0
  if nCPU > 0:
    TnSppR = len(theFilesA)
    BsppCPU = math.floor(TnSppR/nCPU)
    uEvCPU=int(TnSppR-(BsppCPU*nCPU))
    uEvCPUi = [i for i in range(1,uEvCPU+1)]
    nCPUi = [i for i in range(1,nCPU+1)]
    nCPUii = [i for i in range(1,nCPU)]
    TnSppRi = [i for i in range(1,TnSppR+1)]
    #create a vector to partition species number - in list- -upper per cpu
    #vTs is start of cpu block, vTe is end of each cpu block, vtZ is a vector = nSpp with each corresponding CPU
    #create a vector to partition species number - in list- -upper per cpu
    vTe =[]
    vT=0
    for i in nCPUi:
      if i > int(uEvCPU):
        vT=vT+BsppCPU 
      if i <= int(uEvCPU):
        vT=vT+BsppCPU+1   
      vT=int(vT)
      vTe.append(vT)
    ##code for env folder - vector of 'core' where input/remove masks go
    vTs =[]
    vT=1
    for i in nCPUi:
      if i == 1:
        vT=1
      if i > 1:
        vT=vTe[i-2]+1   
      vT=int(vT)
      vTs.append(vT)
    vTz=[]
    Nci=1
    for i in TnSppRi:
      if i < vTe[Nci-1]:
        Vz=int(Nci)
      if i == vTe[Nci-1]:
        Vz=int(Nci)
        Nci=Nci+1
      vTz.append(Vz)
    #vTs=sorted(vTs, reverse=True)
    #vTe=sorted(vTe, reverse=True)
    vTz=sorted(vTz, reverse=True)
    TnSppRi=sorted(TnSppRi, reverse=True)
    ##*new-end
  for i in theFilesA:
    nSppR = nSppR+1 ##*new
    nSppRLabel = TnSppRi[nSppR]
    if vTz[nSppR] >1:##*new
       climatedataFolder=outFolder + "\_CPU"+str(vTz[nSppR])+"_climate"##*new
    if vTz[nSppR] ==1:##*new
       climatedataFolder= climatedataFolderIN##*new
    inSHP = str(i).replace("\\","/")
    outName = os.path.split(inSHP)[1] 
    outNamesp = outName[:-4] 
    outFoldsp = (outNamesp)
    outFsp = (outFolderTemp3+"/"+outFoldsp+".shp").replace("\\","/")
    outFsp2 = (outFolder + "/"+outNamesp + "/GISinputs/ABCDE_Sp_Occ.shp").replace("\\","/")
    outFspABCD = (outFolder + "/"+outNamesp + "/GISinputs/ABCD_Sp_Occ.shp").replace("\\","/")
    outFspACDE = (outFolder + "/" +outNamesp + "/GISinputs/ACDE_Sp_Occ.shp").replace("\\","/")
    outFspBCDE = (outFolder + "/" +outNamesp + "/GISinputs/BCDE_Sp_Occ.shp").replace("\\","/")
    outFspABDE = (outFolder + "/" +outNamesp + "/GISinputs/ABDE_Sp_Occ.shp").replace("\\","/")
    outFspABCE = (outFolder + "/" +outNamesp + "/GISinputs/ABCE_Sp_Occ.shp").replace("\\","/")
    outFspA = (outFolder + "/" +outNamesp + "/GISinputs/A_Sp_Occ.shp").replace("\\","/")
    outFspB = (outFolder + "/" +outNamesp + "/GISinputs/B_Sp_Occ.shp").replace("\\","/")
    outFspC = (outFolder + "/" +outNamesp + "/GISinputs/C_Sp_Occ.shp").replace("\\","/")
    outFspD = (outFolder + "/" +outNamesp + "/GISinputs/D_Sp_Occ.shp").replace("\\","/")
    outFspE = (outFolder + "/" +outNamesp + "/GISinputs/E_Sp_Occ.shp").replace("\\","/")
    outFspPoly = (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen.shp").replace("\\","/")
    spgpMASK = (outFolder + "/" +outNamesp + "/GISinputs/ThiessenRaster.tif").replace("\\","/")
    BiFiIn =(BiasFileFolder + "/" +outNamesp +".asc").replace("\\","/")
    BiFiOut =(outFolder + "/" +outNamesp + "/GISinputs/SpatialGroups.TIF").replace("\\","/")
    BiFiT =(outFolderTemp +"/TEMP").replace("\\","/")
    gp.AddMessage("Preparing data for: " + inSHP)
    LatLongIn='"'+str(y_coords)+";"+str(x_coords)+'"'
    BiFiABCD=(outFolder + "/" +outNamesp + "/GISinputs/BiasFileABCD.asc").replace("\\","/")
    BiFiACDE=(outFolder + "/" +outNamesp + "/GISinputs/BiasFileACDE.asc").replace("\\","/")
    BiFiBCDE=(outFolder + "/" +outNamesp + "/GISinputs/BiasFileBCDE.asc").replace("\\","/")
    BiFiABDE=(outFolder + "/" +outNamesp + "/GISinputs/BiasFileABDE.asc").replace("\\","/")
    BiFiABCE=(outFolder + "/" +outNamesp + "/GISinputs/BiasFileABCE.asc").replace("\\","/")
    myCommandi =""
    myCommandSp =""
    nuMpTS = int(arcpy.GetCount_management(inSHP).getOutput(0))
    if nuMpTS < minModN:
      gp.AddMessage("***************************************************")
      gp.AddMessage("**WARNING: TOO FEW OCCURRENCE POINTS TO RUN MAXENT**")
      gp.AddMessage("***********"+outNamesp+" will be skipped************")
      gp.AddMessage("****  "+str(nuMpTS)+" occurrence points input,        ********")
      gp.AddMessage("****  "+str(minModN)+" is the minimum number required  ********")
    if nuMpTS < minJackN and nuMpTS >= minModN:
      gp.AddMessage("***************************************************")
      gp.AddMessage("**WARNING: TOO FEW OCCURRENCE POINTS TO SPATIALLY**")
      gp.AddMessage("****JACKKNIFE "+outNamesp+"      *************")
      gp.AddMessage("****  "+str(nuMpTS)+" occurrence points input,        ********")
      gp.AddMessage("****  "+str(minJackN)+" is the minimum number required  ********")
      gp.AddMessage("****Will use "+str(NSJpRepType)+" to evaluate "+str(NSJpReps)+" replicates")
      gp.AddMessage("****All feature classes and input regularization***")
      gp.AddMessage("****multipliers will be independently tested*******")
      gp.AddMessage("***************************************************")
      gp.AddMessage("**Step 1 of 2**************************************")
      gp.AddMessage("Creating GIS layers: " + outFoldsp)
      arcpy.CreateFolder_management(outFolder,outFoldsp)
      outFoldspF=outFolder+"/"+outFoldsp
      arcpy.CreateFolder_management(outFoldspF,"TRAIN")
      arcpy.CreateFolder_management(outFoldspF,"ABC")
      arcpy.CreateFolder_management(outFoldspF,"FINAL")
      arcpy.CreateFolder_management(outFoldspF,"GISinputs")
      outFoldspTRAIN = outFoldspF+"/TRAIN"
      outFoldspABC = outFoldspF+"/ABC"
      outFoldspFINAL = outFoldspF+"/FINAL"
      outFoldGIS=outFoldspF+"/GISinputs"
      outFsp2 = (outFolder + "/"+outNamesp + "/GISinputs/ABC_Sp_Occ.shp").replace("\\","/")
      arcpy.CopyFeatures_management(inSHP,outFsp2)
      #now save shp table as CSV
      theFilesB= glob.glob(outFoldGIS+"/*Sp_Occ.dbf")
      for Z in theFilesB:
        inShp = str(Z).replace("\\","/")
        outNameA = os.path.split(inShp)[1] 
        outNamespA = outNameA[:-4] 
        CSVFile = outFoldGIS +"/" +outNamespA +"T.csv"
        fieldnames = [f.name for f in arcpy.ListFields(inShp) if f.type <> 'Geometry']
        with open(CSVFile, 'w') as f:
           f.write(','.join(fieldnames)+'\n') #csv headers
           with arcpy.da.SearchCursor(inShp, fieldnames) as cursor:
             for row in cursor:
                 f.write(','.join([str(r) for r in row])+'\n')
        del cursor 
      #delete unnecessary fields for Maxent
      theFilesC= glob.glob(outFoldGIS+"/*Sp_OccT.csv")
      for Z in theFilesC:
          inCSV = str(Z).replace("\\","/")
          outNameA = os.path.split(inCSV)[1] 
          outNamespA = outNameA[:-5] 
          CSVFile = outFoldGIS +"/" +outNamespA +".csv"
          with open(inCSV,"rb") as source:
             rdr= csv.reader( source )
             with open(CSVFile,"wb") as result:
                 wtr= csv.writer(result)
                 for r in rdr:
                    wtr.writerow((r[1], r[3], r[2]))
      gp.AddMessage("Successfully created GIS layers for: " + outFoldsp)
      gp.AddMessage("************************************************")
      gp.AddMessage("************************************************")
      gp.AddMessage("***Step 2 of 2 *********************************")
      gp.AddMessage("Generating batch code for running MaxEnt models: " + outFoldsp)
      #define text folders for script
      outFoldspFi =outFoldspF.replace("/","\\")
      outFoldGISi=outFoldGIS.replace("/","\\")
      outFoldspFii =outFoldspF.replace("\\","/")
      outFoldGISii=outFoldGIS.replace("\\","/")
      ###Create Python Script 1: Move input bias file to climate folder
      OutBfin=BiFiIn.replace("/","\\")
      PythSMoBF1 ="import shutil, os\n"
      PythSMoBF1 +="shutil.copyfile('"+OutBfin+"','"+climatedataFolder+"\\MaskTemp.asc')\n"
      #write Python Script 1
      newLine = PythSMoBF1.replace("\\","/")
      file = open(outFoldGIS+"/importMask.py", "w")
      file.write(newLine)
      file.close()
      #create code to run python script from batch file and create myCommand##*new
      RunPySpt1 = ("##start"+str(int(nSppRLabel))+"\n")
      RunPySpt1+=("start "+PyLocT+" "+outFoldGIS+"/importMask.py").replace("/","\\")
      RunPySpt1+=" \n"
      myCommandOLD=RunPySpt1
      ###Create Python Script 2: Delete input bias file to climate folder
      PythSDeBF2 ="import os\n"
      PythSDeBF2 +="os.remove('"+climatedataFolder+"\\MaskTemp.asc')\n"
      PythSDeBF2 +="os.remove('"+climatedataFolder+"\\maxent.cache\\MaskTemp.mxe')\n"
      PythSDeBF2 +="os.remove('"+climatedataFolder+"\\maxent.cache\\MaskTemp.info')\n"
      #Write Python Script 2
      newLine = PythSDeBF2.replace("\\","/")
      file = open(outFoldGIS+"/deleteMask.py", "w")
      file.write(newLine)
      file.close()
      #create code to run python script from batch file##*new
      RunPySpt2=("start "+PyLocT+" "+outFoldGIS+"\\deleteMask.py").replace("/","\\")
      RunPySpt2+=" \n"
      RunPySpt2+= ("##end"+str(int(nSppRLabel))+"\n")
      #****************************************************
      #create code to add header to summary stats, copy to new, then sort 
      PythAHd4="import numpy as np \n"
      PythAHd4+="import csv, os, operator \n"    
      PythAHd4+="csvfile = '"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv' \n"
      PythAHd4+='resA = "Species,Regularization Multiplier, Feature Type, Feature N, weighted PR, AUC"\n' 
      PythAHd4+='file = open(csvfile, "r") \n'
      PythAHd4+="filedata = file.read() \n"
      PythAHd4+="file.close() \n"
      PythAHd4+="newLine = resA+os.linesep+filedata \n"
      PythAHd4+='file = open(csvfile, "w") \n'
      PythAHd4+="file.write(newLine) \n"
      PythAHd4+="file.close() \n"
      #****************************************************
      ###NEWCODEsort
      ###NEWCODEsort-default (OER then AUC)
      if OERthenAUC =='OERtoAUC':
        PythAHd4+="dataDO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', usecols=(4,5),skiprows=1)\n"
        PythAHd4+="dataDO = dataDO[~np.isnan(dataDO).any(1)]\n"
        PythAHd4+="Dn = dataDO.shape[0]\n"
        PythAHd4+="dataDO2 = dataDO.sum(axis=1)\n"
        PythAHd4+="dataDO2 = dataDO2.reshape(Dn,1)\n"
        PythAHd4+="dataRO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', 	usecols=(1,3,4,5),skiprows=1)\n"
        PythAHd4+="dataRO = dataRO[~np.isnan(dataRO).any(1)]\n"
        PythAHd4+="dataRO = np.concatenate((dataRO,dataDO2),axis=1)\n"
        PythAHd4+="dataRO = dataRO[~(dataRO[:,4]==1.5), :]\n"
        PythAHd4+="list1 = sorted(dataRO, key=operator.itemgetter(1))\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(3), reverse=True)\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(2), reverse=True)\n"
        PythAHd4+="np.savetxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', list1,delimiter=',',fmt='%1.15s')\n"
      ###To this block for AUC first (changing or sorted)
      if OERthenAUC =='AUCtoOER':
        PythAHd4+="dataRO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', usecols=(1,3,4,5),skiprows=1)\n"
        PythAHd4+="dataRO = dataRO[~np.isnan(dataRO).any(1)]\n"
        PythAHd4+="list1 = sorted(dataRO, key=operator.itemgetter(1))\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(2), reverse=True)\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(3), reverse=True)\n"
        PythAHd4+="np.savetxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', list1,delimiter=',',fmt='%1.15s')\n"
      if OERthenAUC =='maxPRandAUC':
        PythAHd4+="dataDO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', usecols=(4,5),skiprows=1)\n"
        PythAHd4+="dataDO = dataDO[~np.isnan(dataDO).any(1)]\n"
        PythAHd4+="Dn = dataDO.shape[0]\n"
        PythAHd4+="dataDO2 = dataDO.sum(axis=1)\n"
        PythAHd4+="dataDO2 = dataDO2.reshape(Dn,1)\n"
        PythAHd4+="dataRO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', 	usecols=(1,3,4,5),skiprows=1)\n"
        PythAHd4+="dataRO = dataRO[~np.isnan(dataRO).any(1)]\n"
        PythAHd4+="dataRO = np.concatenate((dataRO,dataDO2),axis=1)\n"
        PythAHd4+="dataRO = dataRO[~(dataRO[:,4]==1.5), :]\n"
        PythAHd4+="list1 = sorted(dataRO, key=operator.itemgetter(1))\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(4), reverse=True)\n"
        PythAHd4+="np.savetxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', list1,delimiter=',',fmt='%1.15s')\n"
      #***************************************************
      #save sorted data
      PythAHd4+="input_file = open('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', 'r')\n"
      PythAHd4+="data = csv.reader(input_file, delimiter=',', quoting=csv.QUOTE_NONE)\n"
      PythAHd4+="line = next(data)\n"
      PythAHd4+="Reg=line[0]\nFeat=line[1]\nRegN=float(Reg)\nFeatN=float(Feat)\n"
      #Write Python Script 4
      #python script 4 copy write text for step2
      PythAHd4wr="      file = open('"+outFolderPy+"/Step2_Run_Optimized_MaxEnt_Models.bat', 'r')\n"
      PythAHd4wr+='      filedata = file.read()\n      file.close()\n      newLine =resA+os.linesep+filedata \n'
      PythAHd4wr+="      file = open('"+outFolderPy+"/Step2_Run_Optimized_MaxEnt_Models.bat', 'w')\n"
      PythAHd4wr+='      file.write(newLine)\n      file.close()\n'
      #****************************************************
      #create code to run python script4 from batch file
      RunPyAHd4=("timeout 1 \nstart "+PyLocT+" "+outFoldGIS+"\\FinalRank.py").replace("/","\\")
      RunPyAHd4+=" \ntimeout 1 \n"
      ##create summary stats
      csvfile = outFoldspF+"/"+outFoldsp+"_SUMSTATS_ALL.csv"
      newLine = ""
      file = open(csvfile, "w")
      file.write(newLine)
      file.close()
      ###python code to delete all .asc from training
      PythDel5="import os, fnmatch \n"
      PythDel5+="src="+"'"+outFoldspTRAIN.replace("\\","/")+"'\n"
      PythDel5+="for root, dirnames, filenames in os.walk(src):\n"
      PythDel5+="   for filename in fnmatch.filter(filenames, '*.asc'):\n"
      PythDel5+="      delFile=os.path.join(root, filename)\n"
      PythDel5+="      os.remove(delFile)\n"
      ###iterate thought beta values
      #create code to run python script4 from batch file
      RunPyDel5=("start "+PyLocT+" "+outFoldGIS+"\\DeleteASCIIs.py").replace("/","\\")
      RunPyDel5+=" \n"
      #Write Python Script 2
      newLine = PythDel5
      file = open(outFoldGIS+"/DeleteASCIIs.py", "w")
      file.write(newLine)
      file.close()
      ###***************************
      ###iterate thought beta values
      if BVal=="AutomaticSettings":
            BVal="1"
      for Bn in BVal.split(';'):
         Bvalx = str(Bn)
         Bvalf = "b"+str(Bn).replace(".","_")          
         gp.AddMessage("Creating batch files for Beta value: "+Bvalx)
         arcpy.CreateFolder_management(outFoldspTRAIN,Bvalf)
         arcpy.CreateFolder_management(outFoldspABC,Bvalf)
         outFoldspTRAIN_B = outFoldspTRAIN+"/"+Bvalf
         outFoldspABC_B = outFoldspABC+"/"+Bvalf         
         arcpy.CreateFolder_management(outFoldspTRAIN_B,"L")
         arcpy.CreateFolder_management(outFoldspTRAIN_B,"LQ")
         arcpy.CreateFolder_management(outFoldspTRAIN_B,"H")
         arcpy.CreateFolder_management(outFoldspTRAIN_B,"LQH")
         arcpy.CreateFolder_management(outFoldspTRAIN_B,"LQHPT")
         arcpy.CreateFolder_management(outFoldspABC_B,"L")
         arcpy.CreateFolder_management(outFoldspABC_B,"LQ")
         arcpy.CreateFolder_management(outFoldspABC_B,"H")
         arcpy.CreateFolder_management(outFoldspABC_B,"LQH")
         arcpy.CreateFolder_management(outFoldspABC_B,"LQHPT")
         #TrAiNiNgDaT=location of training CSV file (either AB, BC, AC, ABC), oUtFoLdEr=outfolder (AB+Beta, AC+Beta, BC+beta, ABC+beta, FeTuRe2R= feature classes,4 types: Linear, Linear+Quadratic, Hinge, Linear+Quadratric+Hinge, BiAsFiLeLoc= biasfile
         myCommandi = "java -mx512m -jar " + MaxEntJar + " -e " + climatedataFolder +" -s TrAiNiNgDaT -o oUtFoLdEr noautofeature FeTuRe2R pictures=true biasfile=BiAsFiLeLoc biastype=3 betamultiplier="+Bvalx+"eXtRaPaR"
         # add options
         if int(NSJpReps) > 1:
           myCommandi +=NSJpRepsT
         if int(randTpts) > 0:
           myCommandi +=randTptsT
         if optSkipifExists  == 'true':
           myCommandi += " -S"
         if int(Nthreads) > 1:
           myCommandi +=" threads="+str(Nthreads)
         if doThres == "no threshold":
           myCommandi +=' "applythresholdrule=10 percentile training presence"'
         if doThres != "no threshold":
           myCommandi +=' "applythresholdrule='+str(doThres)+'"'
         if excVars != "":
           myCommandi +=str(excVarsT)
         if catVars != "":
           myCommandi +=str(catVarsT)
         if GUIsil == 'true' and supressWarnings  == 'true':
           myCommandi +=" -z warnings=false"
         if GUIsil == 'true' and supressWarnings  == 'false':
           myCommandi +=" -z warnings=false"
         if GUIsil == 'false' and supressWarnings  == 'true':
           myCommandi +="warnings=false"
         if GUIsil == 'false' and supressWarnings  == 'false':
           myCommandi +="warnings=true"
         myCommandi +=" -a \n" 
         myCommandiShT=myCommandi[:-2]
         NSJpRepsN =int(NSJpReps)
         if int(NSJpRepsN) <= 1:
           myCommandi +="java -cp "+ MaxEntJar +" density.AUC TeStCsV oUtFoLdEr\\"
           myCommandi +=outFoldsp+ ".asc >> "+ outFoldGISi +"\\tempAUC.csv \n"
           myCommandi +="java -cp "+ MaxEntJar +" density.Getval TeStCsV oUtFoLdEr\\"
           myCommandi +=outFoldsp+"_thresholded.asc >> "+outFoldGISi+"\\tempOC.csv \n"
         if int(NSJpRepsN) > 1:
            for i in range(NSJpRepsN): 
               myCommandi +="java -cp "+ MaxEntJar +" density.AUC TeStCsV oUtFoLdEr\\"
               myCommandi +=outFoldsp+"_"+str(i)+".asc >> "+ outFoldGISi +"\\tempAUC.csv \n"
               myCommandi +="java -cp "+ MaxEntJar +" density.Getval TeStCsV oUtFoLdEr\\"
               myCommandi +=outFoldsp+"_"+str(i)+"_thresholded.asc >> "+outFoldGISi+"\\tempOC.csv \n"

         ########################################################
         #create code to run python script from batch file
         #createSubGroups
         ##create dictionary of terms to replace
         OutFiABL = (outFoldspTRAIN_B+"/L").replace("/","\\")
         OutFiABLQ = (outFoldspTRAIN_B+"/LQ").replace("/","\\")
         OutFiABH = (outFoldspTRAIN_B+"/H").replace("/","\\")
         OutFiABLQH = (outFoldspTRAIN_B+"/LQH").replace("/","\\")
         OutFiABLQHPT = (outFoldspTRAIN_B+"/LQHPT").replace("/","\\")
         OutFiFINAL = (outFoldspFINAL).replace("/","\\")
         OutFiABCL = (outFoldspABC_B+"/L").replace("/","\\")
         OutFiABCLQ = (outFoldspABC_B+"/LQ").replace("/","\\")
         OutFiABCH = (outFoldspABC_B+"/H").replace("/","\\")
         OutFiABCLQH = (outFoldspABC_B+"/LQH").replace("/","\\")
         OutFiABCLQHPT = (outFoldspABC_B+"/LQHPT").replace("/","\\")
         OutTrAB=(outFoldGIS+"/ABC_Sp_Occ.csv").replace("/","\\")
         OutTeAB=(outFoldGIS+"/ABC_Sp_Occ.csv").replace("/","\\")
         OutTeABC=(outFoldGIS+"/ABC_Sp_Occ.csv").replace("/","\\")
         myCommandExtra=""
         if optJackknife  == 'true':
               myCommandExtra+= " -J"
         if optResponseCurves == 'true':
               myCommandExtra += " -P"
         if doClamp== 'false':
               myCommandExtra +=" nodoclamp"
         if doExtrp== 'false':
               myCommandExtra +=" noextrapolate"
         if ProLyrs != "":
               myCommandExtra +=str(ProLyrsT) 
         ###complie final code
         ###calculate summary stats for each B and Feature Class
         RunPySpt3t="start "+PyLocT+" oUtFoLdEr\\"+outFoldsp+".py"
         RunPySpt3=RunPySpt3t.replace("/","\\")
         RunPySpt3+=" \n"
         RunPySpt3L=RunPySpt3.replace("oUtFoLdEr",OutFiABCL)
         RunPySpt3LQ=RunPySpt3.replace("oUtFoLdEr",OutFiABCLQ) 
         RunPySpt3H=RunPySpt3.replace("oUtFoLdEr",OutFiABCH)
         RunPySpt3LQH=RunPySpt3.replace("oUtFoLdEr",OutFiABCLQH)
         RunPySpt3LQHPT=RunPySpt3.replace("oUtFoLdEr",OutFiABCLQHPT)
         #TRAIN
         gp.AddMessage("Compiling batch code for "+outFoldsp+": training group and Beta "+Bvalx)
         myCommandiABL = myCommandi.replace("FeTuRe2R","-q -h -p nothreshold").replace("oUtFoLdEr",OutFiABL).replace("BiAsFiLeLoc",OutBfin).replace("TeStCsV",OutTeAB).replace("TrAiNiNgDaT",OutTrAB).replace("eXtRaPaR","")
         myCommandiABLQ = myCommandi.replace("TeStCsV",OutTeAB).replace("oUtFoLdEr",OutFiABLQ).replace("TrAiNiNgDaT",OutTrAB).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR","")
         myCommandiABH = myCommandi.replace("TeStCsV",OutTeAB).replace("oUtFoLdEr",OutFiABH).replace("TrAiNiNgDaT",OutTrAB).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR","")
         myCommandiABLQH = myCommandi.replace("TeStCsV",OutTeAB).replace("oUtFoLdEr",OutFiABLQH).replace("TrAiNiNgDaT",OutTrAB).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR","")
         myCommandiABLQHPT = myCommandi.replace("TeStCsV",OutTeAB).replace("oUtFoLdEr",OutFiABLQHPT).replace("TrAiNiNgDaT",OutTrAB).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR","")
         #ABC
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Final Optimized Run")
         myCommandiABCL = myCommandiShT.replace("TeStCsV",OutTeABC).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABC).replace("FeTuRe2R","-q -h -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/").replace(NSJpRepsT,"").replace(randTptsT,"")
         myCommandiABCLQ = myCommandiShT.replace("TeStCsV",OutTeABC).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABC).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/").replace(NSJpRepsT,"").replace(randTptsT,"")
         myCommandiABCH = myCommandiShT.replace("TeStCsV",OutTeABC).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABC).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/").replace(NSJpRepsT,"").replace(randTptsT,"")
         myCommandiABCLQH = myCommandiShT.replace("TeStCsV",OutTeABC).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABC).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/").replace(NSJpRepsT,"").replace(randTptsT,"")
         myCommandiABCLQHPT = myCommandiShT.replace("TeStCsV",OutTeABC).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABC).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/").replace(NSJpRepsT,"").replace(randTptsT,"")
         #
         myCommandOLD+=myCommandSp
         myCommandSp=myCommandiABL+RunPySpt3L+myCommandiABLQ+RunPySpt3LQ+myCommandiABH+RunPySpt3H+myCommandiABLQH+RunPySpt3LQH+myCommandiABLQHPT+RunPySpt3LQHPT
         myCommandNew= myCommandOLD+myCommandSp
         gp.AddMessage(myCommandNew)
         ####Python Code 4: full run of best parameters
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==1.0:\n"
         PythAHd4+="      resA='"+myCommandiABCL+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==2.0:\n"
         PythAHd4+="      resA='"+myCommandiABCLQ+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==3.0:\n"
         PythAHd4+="      resA='"+myCommandiABCH+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==4.0:\n"
         PythAHd4+="      resA='"+myCommandiABCLQH+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==5.0:\n"
         PythAHd4+="      resA='"+myCommandiABCLQHPT+"'"+"\n"+PythAHd4wr
         ########create python code 2
         ### 1. AVERAGE OC and AUC and store as value
         OutFiABCHt=OutFiABCH.replace("\\","/")
         OutFiABCLt=OutFiABCL.replace("\\","/")
         OutFiABCLQt=OutFiABCLQ.replace("\\","/")
         OutFiABCLQHt=OutFiABCLQH.replace("\\","/")
         OutFiABCLQHPTt=OutFiABCLQHPT.replace("\\","/")
         FeTuReClAsSsHtL="L,1"
         FeTuReClAsSsHtLQ="LQ,2"
         FeTuReClAsSsHtH="H,3" 
         FeTuReClAsSsHtLQH="LQH,4" 
         FeTuReClAsSsHtLQHPT="LQHPF,5" 
         PythScOC="import numpy as np \n"
         PythScOC+="import csv, os \n"
         PythScOC+="csvfile = '"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv' \n"
         PythScOC+="dataRO=np.genfromtxt('"+outFoldGISii+"/tempOC.csv', delimiter=',', usecols=(3),skiprows=1) \n"
         PythScOC+="dataRO = dataRO[~np.isnan(dataRO)] \n"
         PythScOC+="ROtemp=dataRO.mean() \n"
         PythScOC+="ROtempS=str(ROtemp) \n"
         PythScOC+="dataAUC=np.genfromtxt('"+outFoldGISii+"/tempAUC.csv', delimiter=',', usecols=(0),skiprows=0) \n"
         PythScOC+="dataAUC = dataAUC[~np.isnan(dataAUC)] \n"
         PythScOC+="AUCtemp= dataAUC.mean() \n"
         PythScOC+="AUCtempS=str(AUCtemp) \n"
         PythScOC+="resA ='"+outFoldsp+","+Bvalx+",FeTuReClAsSsHt,'+ROtempS+','+AUCtempS \n"
         PythScOC+='file = open(csvfile, "r") \n'
         PythScOC+="filedata = file.read() \n"
         PythScOC+="file.close() \n"
         PythScOC+="newLine = resA+os.linesep+filedata \n"
         PythScOC+='file = open(csvfile, "w") \n'
         PythScOC+="file.write(newLine) \n"
         PythScOC+="file.close() \n"
         PythScOC+="os.remove('"+outFoldGISii+"/tempOC.csv') \n"
         PythScOC+="os.remove('"+outFoldGISii+"/tempAUC.csv') \n"
         myCommandiH_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtH)
         myCommandiL_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtL)
         myCommandiLQ_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtLQ)
         myCommandiLQH_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtLQH)
         myCommandiLQHPT_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtLQHPT)
         file = open(OutFiABCHt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiH_P)
         file.close()
         file = open(OutFiABCLt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiL_P)
         file.close()
         file = open(OutFiABCLQt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiLQ_P)
         file.close()
         file = open(OutFiABCLQHt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiLQH_P)
         file.close()
         file = open(OutFiABCLQHPTt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiLQHPT_P)
         file.close()
         #gp.AddMessage(myCommandSp)
         gp.AddMessage("Batch Code successfully compiled and output for "+outFoldsp+": Beta "+Bvalx)
         gp.AddMessage("Successfully created GIS layers for: " + outFoldsp)
         gp.AddMessage("************************************************")
         gp.AddMessage("************************************************")
         gp.AddMessage("Generating final python scripts for spatial jackknifing MaxEnt models: " + outFoldsp)
      PythAHd4ft="csvfile = '"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv' \n"
      PythAHd4ft+='resA = "Reg Multi, Feature N, weighted PR, AUC, PR & AUC"\n'
      PythAHd4ft+='file = open(csvfile, "r") \n'
      PythAHd4ft+="filedata = file.read() \n"
      PythAHd4ft+="file.close() \n"
      PythAHd4ft+="newLine = resA+os.linesep+filedata \n"
      PythAHd4ft+='file = open(csvfile, "w") \n'
      PythAHd4ft+="file.write(newLine) \n"
      PythAHd4ft+="file.close() \n"
      PythAHd4Fin=PythAHd4+PythAHd4ft
      file = open(outFoldGIS+"/FinalRank.py", "w")
      file.write(PythAHd4Fin)
      file.close()
      myCommandFinal=myCommandNew+RunPyAHd4+RunPyDel5+RunPySpt2
      file = open(outFoldspF+"/spatial_jackknife.bat", "w")
      file.write(myCommandFinal)
      file.close()
      file = open(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat", "r")
      filedata = file.read()
      file.close()
      newLine =myCommandFinal+filedata
      file = open(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat", "w")
      file.write(newLine)
      file.close()
     #cleanup workspace
    else:
     if nuMpTS >= minModN:
      gp.AddMessage("************************************************")
      gp.AddMessage("************************************************")
      gp.AddMessage("***Step 1 of 2**********************************")
      gp.AddMessage("Creating GIS layers for spatial jackknifing: " + outFoldsp)
      arcpy.CreateFolder_management(outFolder,outFoldsp)
      outFoldspF=outFolder+"/"+outFoldsp
      arcpy.CreateFolder_management(outFoldspF,"ABCD")
      arcpy.CreateFolder_management(outFoldspF,"BCDE")
      arcpy.CreateFolder_management(outFoldspF,"ACDE")
      arcpy.CreateFolder_management(outFoldspF,"ABDE")
      arcpy.CreateFolder_management(outFoldspF,"ABCE")
      arcpy.CreateFolder_management(outFoldspF,"ABCDE")
      arcpy.CreateFolder_management(outFoldspF,"FINAL")
      arcpy.CreateFolder_management(outFoldspF,"GISinputs")
      outFoldspABCD = outFoldspF+"/ABCD"
      outFoldspBCDE = outFoldspF+"/BCDE"
      outFoldspACDE = outFoldspF+"/ACDE" 
      outFoldspABDE = outFoldspF+"/ABDE" 
      outFoldspABCE = outFoldspF+"/ABCE" 
      outFoldspABCDE = outFoldspF+"/ABCDE"
      outFoldspFINAL = outFoldspF+"/FINAL"
      outFoldGIS=outFoldspF+"/GISinputs"
      gp.AddMessage("Generating spatial groups for spatial jackknifing: " + outFoldsp)
      ##########################################
      #CODE TO RANDOMLY SPLIT LANDSCAPE
      ##########################################
      ###NEW CODE FOR NON-SPATIAL JACKNIFFING
      nuMpTS = int(arcpy.GetCount_management(inSHP).getOutput(0))
      nuMpTSt = int(nuMpTS/5)
      if nuMpTSt == int((nuMpTS+4)/5): #equals even break  
         nuMpTSt1=nuMpTSt
         nuMpTSt2=nuMpTSt
         nuMpTSt3=nuMpTSt
         nuMpTSt4=nuMpTSt
      if nuMpTSt != int((nuMpTS+4)/5) and nuMpTSt == int((nuMpTS+3)/5) and nuMpTSt == int((nuMpTS+2)/5) and nuMpTSt == int((nuMpTS+1)/5): #equals +1
         nuMpTSt1=nuMpTSt+1
         nuMpTSt2=nuMpTSt
         nuMpTSt3=nuMpTSt   
         nuMpTSt4=nuMpTSt   
      if nuMpTSt != int((nuMpTS+4)/5) and nuMpTSt != int((nuMpTS+3)/5) and nuMpTSt == int((nuMpTS+2)/5) and nuMpTSt == int((nuMpTS+1)/5): #equals +2
         nuMpTSt1=nuMpTSt+1
         nuMpTSt2=nuMpTSt1
         nuMpTSt3=nuMpTSt 
         nuMpTSt4=nuMpTSt 
      if nuMpTSt != int((nuMpTS+4)/5) and nuMpTSt != int((nuMpTS+3)/5) and nuMpTSt != int((nuMpTS+2)/5) and nuMpTSt == int((nuMpTS+1)/5): #equals +3
         nuMpTSt1=nuMpTSt+1
         nuMpTSt2=nuMpTSt1
         nuMpTSt3=nuMpTSt1 
         nuMpTSt4=nuMpTSt 
      if nuMpTSt != int((nuMpTS+4)/5) and nuMpTSt != int((nuMpTS+3)/5) and nuMpTSt != int((nuMpTS+2)/5) and nuMpTSt != int((nuMpTS+1)/5): #equals +4
         nuMpTSt1=nuMpTSt+1
         nuMpTSt2=nuMpTSt1
         nuMpTSt3=nuMpTSt1 
         nuMpTSt4=nuMpTSt1 
      ###creating thiessen polygons
      arcpy.CreateThiessenPolygons_analysis(inSHP,outFspPoly,"ALL")  #note use extent from input climate data
      #Execute AddField
      outFspPoly_1= (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen1.shp").replace("\\","/")
      outFspPoly_2= (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen2.shp").replace("\\","/")
      outFspPoly_3= (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen3.shp").replace("\\","/")
      outFspPoly_4= (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen4.shp").replace("\\","/")
      outFspPoly_5= (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen5.shp").replace("\\","/")
      outFspPoly_F= (outFolder + "/" +outNamesp + "/GISinputs/G_Sp_ThiessenF.shp").replace("\\","/")
      ###Adds new files to open map
      arcpy.AddField_management(outFspPoly,"SS_GROUP", "LONG")
      mxd = arcpy.mapping.MapDocument("CURRENT")
      df = arcpy.mapping.ListDataFrames(mxd)[0]
      addLayer1 = arcpy.mapping.Layer(outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen.shp")
      arcpy.mapping.AddLayer(df, addLayer1, "AUTO_ARRANGE")  
      #Round 1- first round
      arcpy.SubsetFeatures_ga(outFspPoly,outFspPoly_1,"#",nuMpTSt1,"ABSOLUTE_VALUE")
      arcpy.CalculateField_management(outFspPoly_1,"SS_GROUP", "1","#")
      #Round 2
      addLayer2 = arcpy.mapping.Layer(outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen1.shp")
      arcpy.mapping.AddLayer(df, addLayer2, "AUTO_ARRANGE")  
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","","#","SWITCH_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen1","#","REMOVE_FROM_SELECTION")
      arcpy.SubsetFeatures_ga("G_Sp_Thiessen",outFspPoly_2,"#",nuMpTSt2,"ABSOLUTE_VALUE")
      arcpy.SelectLayerByAttribute_management("G_Sp_Thiessen", "CLEAR_SELECTION")
      arcpy.CalculateField_management(outFspPoly_2,"SS_GROUP", "2","#")
      #Round 3
      addLayer3 = arcpy.mapping.Layer(outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen2.shp")
      arcpy.mapping.AddLayer(df, addLayer3, "AUTO_ARRANGE")  
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","","#","SWITCH_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen1","#","REMOVE_FROM_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen2","#","REMOVE_FROM_SELECTION")
      arcpy.SubsetFeatures_ga("G_Sp_Thiessen",outFspPoly_3,"#",nuMpTSt3,"ABSOLUTE_VALUE")
      arcpy.SelectLayerByAttribute_management("G_Sp_Thiessen", "CLEAR_SELECTION")
      arcpy.CalculateField_management(outFspPoly_3,"SS_GROUP", "3","#")
      #Round 4 
      addLayer4 = arcpy.mapping.Layer(outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen3.shp")
      arcpy.mapping.AddLayer(df, addLayer4, "AUTO_ARRANGE")  
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","","#","SWITCH_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen1","#","REMOVE_FROM_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen2","#","REMOVE_FROM_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen3","#","REMOVE_FROM_SELECTION")
      arcpy.SubsetFeatures_ga("G_Sp_Thiessen",outFspPoly_4,"#",nuMpTSt4,"ABSOLUTE_VALUE")
      arcpy.SelectLayerByAttribute_management("G_Sp_Thiessen", "CLEAR_SELECTION")
      arcpy.CalculateField_management(outFspPoly_4,"SS_GROUP", "4","#")
      #Round 4 Last Round
      addLayer5 = arcpy.mapping.Layer(outFolder + "/" +outNamesp + "/GISinputs/G_Sp_Thiessen4.shp")
      arcpy.mapping.AddLayer(df, addLayer5, "AUTO_ARRANGE")  
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","","#","SWITCH_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen1","#","REMOVE_FROM_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen2","#","REMOVE_FROM_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen3","#","REMOVE_FROM_SELECTION")
      arcpy.SelectLayerByLocation_management("G_Sp_Thiessen","ARE_IDENTICAL_TO","G_Sp_Thiessen4","#","REMOVE_FROM_SELECTION")      
      arcpy.CopyFeatures_management("G_Sp_Thiessen",outFspPoly_5)
      arcpy.SelectLayerByAttribute_management("G_Sp_Thiessen", "CLEAR_SELECTION")
      arcpy.CalculateField_management(outFspPoly_5,"SS_GROUP", "5","#")
      outFspPoly_Merge=str(outFspPoly_1)+";"+str(outFspPoly_2)+";"+str(outFspPoly_3)+";"+str(outFspPoly_4)+";"+str(outFspPoly_5)
      arcpy.Merge_management(outFspPoly_Merge,outFspPoly_F,"")  
      mxd = arcpy.mapping.MapDocument("CURRENT")
      for df in arcpy.mapping.ListDataFrames(mxd):
        for lyr in arcpy.mapping.ListLayers(mxd,"G_Sp_Thiessen*", df):
            if lyr.name.lower() != "":
               arcpy.mapping.RemoveLayer(df, lyr)
      del mxd
      arcpy.RefreshTOC()
      arcpy.RefreshActiveView() 
      ###Convert thiessen polygons to raster by group
      arcpy.PolygonToRaster_conversion(outFspPoly_F,"SS_GROUP",spgpMASK,"CELL_CENTER","NONE","#")
      ##########################################
      ###ENDNEW CODE FOR NON-SPATIAL JACKNIFFING
      ##########################################
      ###Clip theissen groups by bias file, then save to ascii
      arcpy.gp.Times_sa(BiFiIn,spgpMASK,BiFiOut)
      gp.AddMessage("Generating regional bias files for spatial jackknifing: " + outFoldsp)
      ###Reclassify masks, to leave one group out: create AB, AC, BC grids
      arcpy.gp.Reclassify_sa(BiFiOut,"Value","1 1;2 1;3 1;4 1;5 NODATA",BiFiT,"DATA")
      arcpy.RasterToASCII_conversion(BiFiT,BiFiABCD)
      arcpy.gp.Reclassify_sa(BiFiOut,"Value","1 NODATA;2 1;3 1;4 1;5 1",BiFiT,"DATA")    
      arcpy.RasterToASCII_conversion(BiFiT,BiFiBCDE)
      arcpy.gp.Reclassify_sa(BiFiOut,"Value","1 1;2 NODATA;3 1;4 1;5 1",BiFiT,"DATA")
      arcpy.RasterToASCII_conversion(BiFiT,BiFiACDE)
      arcpy.gp.Reclassify_sa(BiFiOut,"Value","1 1;2 1;3 NODATA;4 1;5 1",BiFiT,"DATA")
      arcpy.RasterToASCII_conversion(BiFiT,BiFiABDE)
      arcpy.gp.Reclassify_sa(BiFiOut,"Value","1 1;2 1;3 1;4 NODATA;5 1",BiFiT,"DATA")
      arcpy.RasterToASCII_conversion(BiFiT,BiFiABCE)
      gp.AddMessage("Generating test and training CSV files for spatial jackknifing: " + outFoldsp)
      #create spatial groups inSHP
      arcpy.CopyFeatures_management(inSHP,outFsp2)
      ##########################################
      ###LAST ITEM NEW CODE FOR NON-SPATIAL JACKNIFFING
      arcpy.JoinField_management(outFsp2,"UN_ID",outFspPoly_F,"UN_ID","SS_GROUP")
      ###END LAST ITEM NEW CODE FOR NON-SPATIAL JACKNIFFING
      ##########################################
      arcpy.CopyFeatures_management(outFsp2,outFspABCD)
      arcpy.CopyFeatures_management(outFsp2,outFspBCDE)
      arcpy.CopyFeatures_management(outFsp2,outFspACDE) 
      arcpy.CopyFeatures_management(outFsp2,outFspABDE)
      arcpy.CopyFeatures_management(outFsp2,outFspABCE)
      arcpy.CopyFeatures_management(outFsp2,outFspA)
      arcpy.CopyFeatures_management(outFsp2,outFspB)
      arcpy.CopyFeatures_management(outFsp2,outFspC)
      arcpy.CopyFeatures_management(outFsp2,outFspD)
      arcpy.CopyFeatures_management(outFsp2,outFspE)
      #trim shps to groups
      #ABDE
      shp = outFspABDE
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] == 3: 
          cursor.deleteRow()
      del cursor
      #BCDE
      shp = outFspBCDE
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] == 1: 
          cursor.deleteRow()
      del cursor
      #ACDE
      shp = outFspACDE
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] == 2: 
          cursor.deleteRow()
      del cursor
      #ABDE
      shp = outFspABCE
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] == 4: 
          cursor.deleteRow()
      del cursor
      #ABCD
      shp = outFspABCD
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] == 5: 
          cursor.deleteRow()
      del cursor
      #A
      shp = outFspA
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] != 1: 
          cursor.deleteRow()
      del cursor
      #B
      shp = outFspB
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] != 2: 
          cursor.deleteRow()
      del cursor
      #C
      shp = outFspC
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] != 3: 
          cursor.deleteRow()
      del cursor
      #D
      shp = outFspD
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] != 4: 
          cursor.deleteRow()
      del cursor
      #E
      shp = outFspE
      cursor = arcpy.da.UpdateCursor(shp, ["SS_GROUP"])
      for row in cursor:
         if row [0] != 5: 
          cursor.deleteRow()
      del cursor
      gp.AddMessage("Writing test and training CSV files for spatial jackknifing: " + outFoldsp)
      #now save shp table as CSV
      theFilesB= glob.glob(outFoldGIS+"/*Sp_Occ.dbf")
      for Z in theFilesB:
        inShp = str(Z).replace("\\","/")
        outNameA = os.path.split(inShp)[1] 
        outNamespA = outNameA[:-4] 
        CSVFile = outFoldGIS +"/" +outNamespA +"T.csv"
        fieldnames = [f.name for f in arcpy.ListFields(inShp) if f.type <> 'Geometry']
        with open(CSVFile, 'w') as f:
           f.write(','.join(fieldnames)+'\n') #csv headers
           with arcpy.da.SearchCursor(inShp, fieldnames) as cursor:
             for row in cursor:
                 f.write(','.join([str(r) for r in row])+'\n')
        del cursor 
       #delete unnecessary fields for Maxent
      theFilesC= glob.glob(outFoldGIS+"/*Sp_OccT.csv")
      for Z in theFilesC:
          inCSV = str(Z).replace("\\","/")
          outNameA = os.path.split(inCSV)[1] 
          outNamespA = outNameA[:-5] 
          CSVFile = outFoldGIS +"/" +outNamespA +".csv"
          with open(inCSV,"rb") as source:
             rdr= csv.reader( source )
             with open(CSVFile,"wb") as result:
                 wtr= csv.writer(result)
                 for r in rdr:
                    wtr.writerow((r[1], r[3], r[2]))
      gp.AddMessage("Successfully created GIS layers for: " + outFoldsp)
      gp.AddMessage("************************************************")
      gp.AddMessage("************************************************")
      gp.AddMessage("***Step 2 of 2 *********************************")
      gp.AddMessage("Generating batch code for running MaxEnt models: " + outFoldsp)
      #define text folders for script
      outFoldspFi =outFoldspF.replace("/","\\")
      outFoldGISi=outFoldGIS.replace("/","\\")
      outFoldspFii =outFoldspF.replace("\\","/")
      outFoldGISii=outFoldGIS.replace("\\","/")
      ###Create Python Script 1: Move input bias file to climate folder
      OutBfin=BiFiIn.replace("/","\\")
      PythSMoBF1 ="import shutil, os\n"
      PythSMoBF1 +="shutil.copyfile('"+OutBfin+"','"+climatedataFolder+"\\MaskTemp.asc')\n"
      #write Python Script 1
      newLine = PythSMoBF1.replace("\\","/")
      file = open(outFoldGIS+"/importMask.py", "w")
      file.write(newLine)
      file.close()
      #create code to run python script from batch file and create myCommand##*new
      RunPySpt1 = ("##start"+str(int(nSppRLabel))+"\n")
      RunPySpt1+=("start "+PyLocT+" "+outFoldGIS+"/importMask.py").replace("/","\\")
      RunPySpt1+=" \n"
      myCommandOLD=RunPySpt1
      ###Create Python Script 2: Delete input bias file to climate folder
      PythSDeBF2 ="import os\n"
      PythSDeBF2 +="os.remove('"+climatedataFolder+"\\MaskTemp.asc')\n"
      PythSDeBF2 +="os.remove('"+climatedataFolder+"\\maxent.cache\\MaskTemp.mxe')\n"
      PythSDeBF2 +="os.remove('"+climatedataFolder+"\\maxent.cache\\MaskTemp.info')\n"
      #Write Python Script 2
      newLine = PythSDeBF2.replace("\\","/")
      file = open(outFoldGIS+"/deleteMask.py", "w")
      file.write(newLine)
      file.close()
      #create code to run python script from batch file##*new
      RunPySpt2=("start "+PyLocT+" "+outFoldGIS+"\\deleteMask.py").replace("/","\\")
      RunPySpt2+=" \n"
      RunPySpt2+= ("##end"+str(int(nSppRLabel))+"\n")
      #****************************************************
      #create code to add header to summary stats, copy to new, then sort 
      PythAHd4="import numpy as np \n"
      PythAHd4+="import csv, os, operator \n"    
      PythAHd4+="csvfile = '"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv' \n"
      PythAHd4+='resA = "Species,Regularization Multiplier, Feature Type, Feature N, weighted PR, AUC"\n' 
      PythAHd4+='file = open(csvfile, "r") \n'
      PythAHd4+="filedata = file.read() \n"
      PythAHd4+="file.close() \n"
      PythAHd4+="newLine = resA+os.linesep+filedata \n"
      PythAHd4+='file = open(csvfile, "w") \n'
      PythAHd4+="file.write(newLine) \n"
      PythAHd4+="file.close() \n"
      #****************************************************
      ###NEWCODEsort
      ###NEWCODEsort-default (OER then AUC)
      if OERthenAUC =='OERtoAUC':
        PythAHd4+="dataDO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', usecols=(4,5),skiprows=1)\n"
        PythAHd4+="dataDO = dataDO[~np.isnan(dataDO).any(1)]\n"
        PythAHd4+="Dn = dataDO.shape[0]\n"
        PythAHd4+="dataDO2 = dataDO.sum(axis=1)\n"
        PythAHd4+="dataDO2 = dataDO2.reshape(Dn,1)\n"
        PythAHd4+="dataRO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', 	usecols=(1,3,4,5),skiprows=1)\n"
        PythAHd4+="dataRO = dataRO[~np.isnan(dataRO).any(1)]\n"
        PythAHd4+="dataRO = np.concatenate((dataRO,dataDO2),axis=1)\n"
        PythAHd4+="dataRO = dataRO[~(dataRO[:,4]==1.5), :]\n"
        PythAHd4+="list1 = sorted(dataRO, key=operator.itemgetter(1))\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(3), reverse=True)\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(2), reverse=True)\n"
        PythAHd4+="np.savetxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', list1,delimiter=',',fmt='%1.15s')\n"
      ###To this block for AUC first (changing or sorted)
      if OERthenAUC =='AUCtoOER':
        PythAHd4+="dataRO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', usecols=(1,3,4,5),skiprows=1)\n"
        PythAHd4+="dataRO = dataRO[~np.isnan(dataRO).any(1)]\n"
        PythAHd4+="list1 = sorted(dataRO, key=operator.itemgetter(1))\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(2), reverse=True)\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(3), reverse=True)\n"
        PythAHd4+="np.savetxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', list1,delimiter=',',fmt='%1.15s')\n"
      if OERthenAUC =='maxPRandAUC':
        PythAHd4+="dataDO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', usecols=(4,5),skiprows=1)\n"
        PythAHd4+="dataDO = dataDO[~np.isnan(dataDO).any(1)]\n"
        PythAHd4+="Dn = dataDO.shape[0]\n"
        PythAHd4+="dataDO2 = dataDO.sum(axis=1)\n"
        PythAHd4+="dataDO2 = dataDO2.reshape(Dn,1)\n"
        PythAHd4+="dataRO = np.genfromtxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv', delimiter=',', 	usecols=(1,3,4,5),skiprows=1)\n"
        PythAHd4+="dataRO = dataRO[~np.isnan(dataRO).any(1)]\n"
        PythAHd4+="dataRO = np.concatenate((dataRO,dataDO2),axis=1)\n"
        PythAHd4+="dataRO = dataRO[~(dataRO[:,4]==1.5), :]\n"
        PythAHd4+="list1 = sorted(dataRO, key=operator.itemgetter(1))\n"
        PythAHd4+="list1 = sorted(list1, key=operator.itemgetter(4), reverse=True)\n"
        PythAHd4+="np.savetxt('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', list1,delimiter=',',fmt='%1.15s')\n"
      #****************************************************
      #save sorted data
      PythAHd4+="input_file = open('"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv', 'r')\n"
      PythAHd4+="data = csv.reader(input_file, delimiter=',', quoting=csv.QUOTE_NONE)\n"
      PythAHd4+="line = next(data)\n"
      PythAHd4+="Reg=line[0]\nFeat=line[1]\nRegN=float(Reg)\nFeatN=float(Feat)\n"
      #Write Python Script 4
      #python script 4 copy write text for step2
      PythAHd4wr="      file = open('"+outFolderPy+"/Step2_Run_Optimized_MaxEnt_Models.bat', 'r')\n"
      PythAHd4wr+='      filedata = file.read()\n      file.close()\n      newLine =resA+os.linesep+filedata \n'
      PythAHd4wr+="      file = open('"+outFolderPy+"/Step2_Run_Optimized_MaxEnt_Models.bat', 'w')\n"
      PythAHd4wr+='      file.write(newLine)\n      file.close()\n'
      #****************************************************
      #create code to run python script4 from batch file
      RunPyAHd4=("timeout 1 \nstart "+PyLocT+" "+outFoldGIS+"\\FinalRank.py").replace("/","\\")
      RunPyAHd4+=" \ntimeout 1 \n"
      ##create summary stats
      csvfile = outFoldspF+"/"+outFoldsp+"_SUMSTATS_ALL.csv"
      newLine = ""
      file = open(csvfile, "w")
      file.write(newLine)
      file.close()
      ###python code to delete all .asc from training
      PythDel5="import os, fnmatch \n"
      PythDel5+="src="+"'"+outFoldspABCD.replace("\\","/")+"'\n"
      PythDel5+="for root, dirnames, filenames in os.walk(src):\n"
      PythDel5+="   for filename in fnmatch.filter(filenames, '*.asc'):\n"
      PythDel5+="      delFile=os.path.join(root, filename)\n"
      PythDel5+="      os.remove(delFile)\n"
      PythDel5+="src="+"'"+outFoldspACDE.replace("\\","/")+"'\n"
      PythDel5+="for root, dirnames, filenames in os.walk(src):\n"
      PythDel5+="   for filename in fnmatch.filter(filenames, '*.asc'):\n"
      PythDel5+="      delFile=os.path.join(root, filename)\n"
      PythDel5+="      os.remove(delFile)\n"
      PythDel5+="src="+"'"+outFoldspBCDE.replace("\\","/")+"'\n"
      PythDel5+="for root, dirnames, filenames in os.walk(src):\n"
      PythDel5+="   for filename in fnmatch.filter(filenames, '*.asc'):\n"
      PythDel5+="       delFile=os.path.join(root, filename)\n"
      PythDel5+="       os.remove(delFile)\n"
      PythDel5+="src="+"'"+outFoldspABDE.replace("\\","/")+"'\n"
      PythDel5+="for root, dirnames, filenames in os.walk(src):\n"
      PythDel5+="   for filename in fnmatch.filter(filenames, '*.asc'):\n"
      PythDel5+="       delFile=os.path.join(root, filename)\n"
      PythDel5+="       os.remove(delFile)\n"       
      PythDel5+="src="+"'"+outFoldspABCE.replace("\\","/")+"'\n"
      PythDel5+="for root, dirnames, filenames in os.walk(src):\n"
      PythDel5+="   for filename in fnmatch.filter(filenames, '*.asc'):\n"
      PythDel5+="       delFile=os.path.join(root, filename)\n"
      PythDel5+="       os.remove(delFile)\n"      
      ###iterate thought beta values
      #create code to run python script4 from batch file
      RunPyDel5=("start "+PyLocT+" "+outFoldGIS+"\\DeleteASCIIs.py").replace("/","\\")
      RunPyDel5+=" \n"
      #Write Python Script 2
      newLine = PythDel5
      file = open(outFoldGIS+"/DeleteASCIIs.py", "w")
      file.write(newLine)
      file.close()
      ###***************************
      ###iterate thought beta values
      if BVal=="AutomaticSettings":
            BVal="1"
      for Bn in BVal.split(';'):
         Bvalx = str(Bn)
         Bvalf = "b"+str(Bn).replace(".","_")          
         gp.AddMessage("Creating batch files for Beta value: "+Bvalx)
         arcpy.CreateFolder_management(outFoldspABCD,Bvalf)
         arcpy.CreateFolder_management(outFoldspBCDE,Bvalf)
         arcpy.CreateFolder_management(outFoldspACDE,Bvalf)
         arcpy.CreateFolder_management(outFoldspABDE,Bvalf)
         arcpy.CreateFolder_management(outFoldspABCE,Bvalf)
         arcpy.CreateFolder_management(outFoldspABCDE,Bvalf)
         outFoldspABCD_B = outFoldspABCD+"/"+Bvalf
         outFoldspBCDE_B = outFoldspBCDE+"/"+Bvalf
         outFoldspACDE_B = outFoldspACDE+"/"+Bvalf
         outFoldspABCDE_B = outFoldspABCDE+"/"+Bvalf
         outFoldspABDE_B = outFoldspABDE+"/"+Bvalf
         outFoldspABCE_B = outFoldspABCE+"/"+Bvalf
         arcpy.CreateFolder_management(outFoldspABCD_B,"L")
         arcpy.CreateFolder_management(outFoldspABCD_B,"LQ")
         arcpy.CreateFolder_management(outFoldspABCD_B,"H")
         arcpy.CreateFolder_management(outFoldspABCD_B,"LQH")
         arcpy.CreateFolder_management(outFoldspABCD_B,"LQHPT")
         arcpy.CreateFolder_management(outFoldspACDE_B,"L")
         arcpy.CreateFolder_management(outFoldspACDE_B,"LQ")
         arcpy.CreateFolder_management(outFoldspACDE_B,"H")
         arcpy.CreateFolder_management(outFoldspACDE_B,"LQH")
         arcpy.CreateFolder_management(outFoldspACDE_B,"LQHPT")
         arcpy.CreateFolder_management(outFoldspBCDE_B,"L")
         arcpy.CreateFolder_management(outFoldspBCDE_B,"LQ")
         arcpy.CreateFolder_management(outFoldspBCDE_B,"H")
         arcpy.CreateFolder_management(outFoldspBCDE_B,"LQH")
         arcpy.CreateFolder_management(outFoldspBCDE_B,"LQHPT")
         arcpy.CreateFolder_management(outFoldspABCDE_B,"L")
         arcpy.CreateFolder_management(outFoldspABCDE_B,"LQ")
         arcpy.CreateFolder_management(outFoldspABCDE_B,"H")
         arcpy.CreateFolder_management(outFoldspABCDE_B,"LQH")
         arcpy.CreateFolder_management(outFoldspABCDE_B,"LQHPT")
         arcpy.CreateFolder_management(outFoldspABDE_B,"L")
         arcpy.CreateFolder_management(outFoldspABDE_B,"LQ")
         arcpy.CreateFolder_management(outFoldspABDE_B,"H")
         arcpy.CreateFolder_management(outFoldspABDE_B,"LQH")
         arcpy.CreateFolder_management(outFoldspABDE_B,"LQHPT")
         arcpy.CreateFolder_management(outFoldspABCE_B,"L")
         arcpy.CreateFolder_management(outFoldspABCE_B,"LQ")
         arcpy.CreateFolder_management(outFoldspABCE_B,"H")
         arcpy.CreateFolder_management(outFoldspABCE_B,"LQH")
         arcpy.CreateFolder_management(outFoldspABCE_B,"LQHPT")
         #TrAiNiNgDaT=location of training CSV file (either ABC, BCD, ACD, ABD, ABCD), oUtFoLdEr=outfolder (AB+Beta, AC+Beta, BC+beta, ABC+beta, FeTuRe2R= feature classes,4 types: Linear, Linear+Quadratic, Hinge, Linear+Quadratric+Hinge, BiAsFiLeLoc= biasfile
         myCommandi = "java -mx512m -jar " + MaxEntJar + " -e " + climatedataFolder +" -s TrAiNiNgDaT -o oUtFoLdEr noautofeature FeTuRe2R pictures=true biasfile=BiAsFiLeLoc biastype=3 betamultiplier="+Bvalx+"eXtRaPaR"
         # add options
         if optSkipifExists  == 'true':
           myCommandi += " -S"
         if int(pReps) > 1:
           myCommandi +=pRepsSJ
         if int(Nthreads) > 1:
           myCommandi +=" threads="+str(Nthreads)
         if doThres == "no threshold":
           myCommandi +=' "applythresholdrule=10 percentile training presence"'
         if doThres != "no threshold":
           myCommandi +=' "applythresholdrule='+str(doThres)+'"'
         if excVars != "":
           myCommandi +=str(excVarsT)
         if catVars != "":
           myCommandi +=str(catVarsT)
         if GUIsil == 'true' and supressWarnings  == 'true':
           myCommandi +=" -z warnings=false"
         if GUIsil == 'true' and supressWarnings  == 'false':
           myCommandi +=" -z warnings=false"
         if GUIsil == 'false' and supressWarnings  == 'true':
           myCommandi +="warnings=false"
         if GUIsil == 'false' and supressWarnings  == 'false':
           myCommandi +="warnings=true"
         myCommandi +=" -a \n" 
         myCommandiShT=myCommandi[:-2]
         if int(pReps) <= 1:
           myCommandi +="java -cp "+ MaxEntJar +" density.AUC TeStCsV oUtFoLdEr\\"
           myCommandi +=outFoldsp+ ".asc >> "+ outFoldGISi +"\\tempAUC.csv \n"
           myCommandi +="java -cp "+ MaxEntJar +" density.Getval TeStCsV oUtFoLdEr\\"
           myCommandi +=outFoldsp+"_thresholded.asc >> "+outFoldGISi+"\\tempOC.csv \n"
         ###############
         if int(pReps) > 1:
           pRepsB= int(pReps)
           for i in range(pRepsB): 
               myCommandi +="java -cp "+ MaxEntJar +" density.AUC TeStCsV oUtFoLdEr\\"
               myCommandi +=outFoldsp+"_"+str(i)+".asc >> "+ outFoldGISi +"\\tempAUC.csv \n"
               myCommandi +="java -cp "+ MaxEntJar +" density.Getval TeStCsV oUtFoLdEr\\"
               myCommandi +=outFoldsp+"_"+str(i)+"_thresholded.asc >> "+outFoldGISi+"\\tempOC.csv \n"
         ########################################################
         #create code to run python script from batch file
         #createSubGroups
         ##create dictionary of terms to replace
         OutFiABCDL = (outFoldspABCD_B+"/L").replace("/","\\")
         OutFiABCDLQ = (outFoldspABCD_B+"/LQ").replace("/","\\")
         OutFiABCDH = (outFoldspABCD_B+"/H").replace("/","\\")
         OutFiABCDLQH = (outFoldspABCD_B+"/LQH").replace("/","\\")
         OutFiABCDLQHPT = (outFoldspABCD_B+"/LQHPT").replace("/","\\")
         OutFiBCDEL = (outFoldspBCDE_B+"/L").replace("/","\\")
         OutFiBCDELQ = (outFoldspBCDE_B+"/LQ").replace("/","\\")
         OutFiBCDEH = (outFoldspBCDE_B+"/H").replace("/","\\")
         OutFiBCDELQH = (outFoldspBCDE_B+"/LQH").replace("/","\\")
         OutFiBCDELQHPT = (outFoldspBCDE_B+"/LQHPT").replace("/","\\")
         OutFiACDEL = (outFoldspACDE_B+"/L").replace("/","\\")
         OutFiACDELQ = (outFoldspACDE_B+"/LQ").replace("/","\\")
         OutFiACDEH = (outFoldspACDE_B+"/H").replace("/","\\")
         OutFiACDELQH = (outFoldspACDE_B+"/LQH").replace("/","\\")
         OutFiACDELQHPT = (outFoldspACDE_B+"/LQHPT").replace("/","\\")
         OutFiFINAL = (outFoldspFINAL).replace("/","\\")
         OutFiABCDEL = (outFoldspABCDE_B+"/L").replace("/","\\")
         OutFiABCDELQ = (outFoldspABCDE_B+"/LQ").replace("/","\\")
         OutFiABCDEH = (outFoldspABCDE_B+"/H").replace("/","\\")
         OutFiABCDELQH = (outFoldspABCDE_B+"/LQH").replace("/","\\")
         OutFiABCDELQHPT = (outFoldspABCDE_B+"/LQHPT").replace("/","\\")
         OutFiABDEL = (outFoldspABDE_B+"/L").replace("/","\\")
         OutFiABDELQ = (outFoldspABDE_B+"/LQ").replace("/","\\")
         OutFiABDEH = (outFoldspABDE_B+"/H").replace("/","\\")
         OutFiABDELQH = (outFoldspABDE_B+"/LQH").replace("/","\\")
         OutFiABDELQHPT = (outFoldspABDE_B+"/LQHPT").replace("/","\\")
         OutFiABCEL = (outFoldspABCE_B+"/L").replace("/","\\")
         OutFiABCELQ = (outFoldspABCE_B+"/LQ").replace("/","\\")
         OutFiABCEH = (outFoldspABCE_B+"/H").replace("/","\\")
         OutFiABCELQH = (outFoldspABCE_B+"/LQH").replace("/","\\")
         OutFiABCELQHPT = (outFoldspABCE_B+"/LQHPT").replace("/","\\")
         OutBfABCD=BiFiABCD.replace("/","\\")
         OutBfACDE=BiFiACDE.replace("/","\\")
         OutBfBCDE=BiFiBCDE.replace("/","\\")
         OutBfABDE=BiFiABDE.replace("/","\\")
         OutBfABCE=BiFiABCE.replace("/","\\")
         OutTrABCD=(outFoldGIS+"/ABCD_Sp_Occ.csv").replace("/","\\")
         OutTeABCD=(outFoldGIS+"/E_Sp_Occ.csv").replace("/","\\")
         OutTrACDE=(outFoldGIS+"/ACDE_Sp_Occ.csv").replace("/","\\")
         OutTeACDE=(outFoldGIS+"/B_Sp_Occ.csv").replace("/","\\")
         OutTrBCDE=(outFoldGIS+"/BCDE_Sp_Occ.csv").replace("/","\\")
         OutTeBCDE=(outFoldGIS+"/A_Sp_Occ.csv").replace("/","\\")
         OutTeABCDE=(outFoldGIS+"/ABCDE_Sp_Occ.csv").replace("/","\\")
         OutTrABDE=(outFoldGIS+"/ABDE_Sp_Occ.csv").replace("/","\\")
         OutTeABDE=(outFoldGIS+"/C_Sp_Occ.csv").replace("/","\\")
         OutTrABCE=(outFoldGIS+"/ABCE_Sp_Occ.csv").replace("/","\\")
         OutTeABCE=(outFoldGIS+"/D_Sp_Occ.csv").replace("/","\\")
         myCommandExtra=""
         if optJackknife  == 'true':
               myCommandExtra+= " -J"
         if optResponseCurves == 'true':
               myCommandExtra += " -P"
         if doClamp== 'false':
               myCommandExtra +=" nodoclamp"
         if doExtrp== 'false':
               myCommandExtra +=" noextrapolate"
         if ProLyrs != "":
               myCommandExtra +=str(ProLyrsT) 
         ###complie final code
         ###calculate summary stats for each B and Feature Class
         RunPySpt3t="start "+PyLocT+" oUtFoLdEr\\"+outFoldsp+".py"
         RunPySpt3=RunPySpt3t.replace("/","\\")
         RunPySpt3+=" \n"
         RunPySpt3L=RunPySpt3.replace("oUtFoLdEr",OutFiABCDEL)
         RunPySpt3LQ=RunPySpt3.replace("oUtFoLdEr",OutFiABCDELQ) 
         RunPySpt3H=RunPySpt3.replace("oUtFoLdEr",OutFiABCDEH)
         RunPySpt3LQH=RunPySpt3.replace("oUtFoLdEr",OutFiABCDELQH)
         RunPySpt3LQHPT=RunPySpt3.replace("oUtFoLdEr",OutFiABCDELQHPT)
         #ABCD
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Group ABCD and Beta "+Bvalx)
         myCommandiABCDL = myCommandi.replace("FeTuRe2R","-q -h -p nothreshold").replace("oUtFoLdEr",OutFiABCDL).replace("BiAsFiLeLoc",OutBfABCD).replace("TeStCsV",OutTeABCD).replace("TrAiNiNgDaT",OutTrABCD).replace("eXtRaPaR","")
         myCommandiABCDLQ = myCommandi.replace("TeStCsV",OutTeABCD).replace("oUtFoLdEr",OutFiABCDLQ).replace("TrAiNiNgDaT",OutTrABCD).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfABCD).replace("eXtRaPaR","")
         myCommandiABCDH = myCommandi.replace("TeStCsV",OutTeABCD).replace("oUtFoLdEr",OutFiABCDH).replace("TrAiNiNgDaT",OutTrABCD).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfABCD).replace("eXtRaPaR","")
         myCommandiABCDLQH = myCommandi.replace("TeStCsV",OutTeABCD).replace("oUtFoLdEr",OutFiABCDLQH).replace("TrAiNiNgDaT",OutTrABCD).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfABCD).replace("eXtRaPaR","")
         myCommandiABCDLQHPT = myCommandi.replace("TeStCsV",OutTeABCD).replace("oUtFoLdEr",OutFiABCDLQHPT).replace("TrAiNiNgDaT",OutTrABCD).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfABCD).replace("eXtRaPaR","")
         #ACDE
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Group ACDE and Beta "+Bvalx)
         myCommandiACDEL = myCommandi.replace("TeStCsV",OutTeACDE).replace("oUtFoLdEr",OutFiACDEL).replace("TrAiNiNgDaT",OutTrACDE).replace("FeTuRe2R","-q -h -p nothreshold").replace("BiAsFiLeLoc",OutBfACDE).replace("eXtRaPaR","")
         myCommandiACDELQ = myCommandi.replace("TeStCsV",OutTeACDE).replace("oUtFoLdEr",OutFiACDELQ).replace("TrAiNiNgDaT",OutTrACDE).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfACDE).replace("eXtRaPaR","")
         myCommandiACDEH = myCommandi.replace("TeStCsV",OutTeACDE).replace("oUtFoLdEr",OutFiACDEH).replace("TrAiNiNgDaT",OutTrACDE).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfACDE).replace("eXtRaPaR","")
         myCommandiACDELQH = myCommandi.replace("TeStCsV",OutTeACDE).replace("oUtFoLdEr",OutFiACDELQH).replace("TrAiNiNgDaT",OutTrACDE).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfACDE).replace("eXtRaPaR","")
         myCommandiACDELQHPT = myCommandi.replace("TeStCsV",OutTeACDE).replace("oUtFoLdEr",OutFiACDELQHPT).replace("TrAiNiNgDaT",OutTrACDE).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfACDE).replace("eXtRaPaR","")
         #BCDE
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Group BCDE and Beta "+Bvalx)
         myCommandiBCDEL = myCommandi.replace("TeStCsV",OutTeBCDE).replace("oUtFoLdEr",OutFiBCDEL).replace("TrAiNiNgDaT",OutTrBCDE).replace("FeTuRe2R","-q -h -p nothreshold").replace("BiAsFiLeLoc",OutBfBCDE).replace("eXtRaPaR","")
         myCommandiBCDELQ = myCommandi.replace("TeStCsV",OutTeBCDE).replace("oUtFoLdEr",OutFiBCDELQ).replace("TrAiNiNgDaT",OutTrBCDE).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfBCDE).replace("eXtRaPaR","")
         myCommandiBCDEH = myCommandi.replace("TeStCsV",OutTeBCDE).replace("oUtFoLdEr",OutFiBCDEH).replace("TrAiNiNgDaT",OutTrBCDE).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfBCDE).replace("eXtRaPaR","")
         myCommandiBCDELQH = myCommandi.replace("TeStCsV",OutTeBCDE).replace("oUtFoLdEr",OutFiBCDELQH).replace("TrAiNiNgDaT",OutTrBCDE).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfBCDE).replace("eXtRaPaR","")
         myCommandiBCDELQHPT = myCommandi.replace("TeStCsV",OutTeBCDE).replace("oUtFoLdEr",OutFiBCDELQHPT).replace("TrAiNiNgDaT",OutTrBCDE).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfBCDE).replace("eXtRaPaR","")
         #ABDE
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Group ABDE and Beta "+Bvalx)
         myCommandiABDEL = myCommandi.replace("TeStCsV",OutTeABDE).replace("oUtFoLdEr",OutFiABDEL).replace("TrAiNiNgDaT",OutTrABDE).replace("FeTuRe2R","-q -h -p nothreshold").replace("BiAsFiLeLoc",OutBfABDE).replace("eXtRaPaR","")
         myCommandiABDELQ = myCommandi.replace("TeStCsV",OutTeABDE).replace("oUtFoLdEr",OutFiABDELQ).replace("TrAiNiNgDaT",OutTrABDE).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfABDE).replace("eXtRaPaR","")
         myCommandiABDEH = myCommandi.replace("TeStCsV",OutTeABDE).replace("oUtFoLdEr",OutFiABDEH).replace("TrAiNiNgDaT",OutTrABDE).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfABDE).replace("eXtRaPaR","")
         myCommandiABDELQH = myCommandi.replace("TeStCsV",OutTeABDE).replace("oUtFoLdEr",OutFiABDELQH).replace("TrAiNiNgDaT",OutTrABDE).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfABDE).replace("eXtRaPaR","")
         myCommandiABDELQHPT = myCommandi.replace("TeStCsV",OutTeABDE).replace("oUtFoLdEr",OutFiABDELQHPT).replace("TrAiNiNgDaT",OutTrABDE).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfABDE).replace("eXtRaPaR","")
         #ABCE
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Group ABCE and Beta "+Bvalx)
         myCommandiABCEL = myCommandi.replace("TeStCsV",OutTeABCE).replace("oUtFoLdEr",OutFiABCEL).replace("TrAiNiNgDaT",OutTrABCE).replace("FeTuRe2R","-q -h -p nothreshold").replace("BiAsFiLeLoc",OutBfABCE).replace("eXtRaPaR","")
         myCommandiABCELQ = myCommandi.replace("TeStCsV",OutTeABCE).replace("oUtFoLdEr",OutFiABCELQ).replace("TrAiNiNgDaT",OutTrABCE).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfABCE).replace("eXtRaPaR","")
         myCommandiABCEH = myCommandi.replace("TeStCsV",OutTeABCE).replace("oUtFoLdEr",OutFiABCEH).replace("TrAiNiNgDaT",OutTrABCE).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfABCE).replace("eXtRaPaR","")
         myCommandiABCELQH = myCommandi.replace("TeStCsV",OutTeABCE).replace("oUtFoLdEr",OutFiABCELQH).replace("TrAiNiNgDaT",OutTrABCE).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfABCE).replace("eXtRaPaR","")
         myCommandiABCELQHPT = myCommandi.replace("TeStCsV",OutTeABCE).replace("oUtFoLdEr",OutFiABCELQHPT).replace("TrAiNiNgDaT",OutTrABCE).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfABCE).replace("eXtRaPaR","")
         #ABCDE
         gp.AddMessage("Compiling batch code for "+outFoldsp+": Final Optimized Run")
         myCommandiABCDEL = myCommandiShT.replace("TeStCsV",OutTeABCDE).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABCDE).replace("FeTuRe2R","-q -h -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/")
         myCommandiABCDELQ = myCommandiShT.replace("TeStCsV",OutTeABCDE).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABCDE).replace("FeTuRe2R","-h -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/")
         myCommandiABCDEH = myCommandiShT.replace("TeStCsV",OutTeABCDE).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABCDE).replace("FeTuRe2R","-l -q -p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/")
         myCommandiABCDELQH = myCommandiShT.replace("TeStCsV",OutTeABCDE).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABCDE).replace("FeTuRe2R","-p nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/")
         myCommandiABCDELQHPT = myCommandiShT.replace("TeStCsV",OutTeABCDE).replace("oUtFoLdEr",OutFiFINAL).replace("TrAiNiNgDaT",OutTeABCDE).replace("eTuRe2R","nothreshold").replace("BiAsFiLeLoc",OutBfin).replace("eXtRaPaR",myCommandExtra).replace("\\","/")
         #
         myCommandOLD+=myCommandSp
         myCommandSp=myCommandiABCDL+myCommandiBCDEL+myCommandiACDEL+myCommandiABDEL+myCommandiABCEL+RunPySpt3L+myCommandiABCDLQ+myCommandiBCDELQ+myCommandiACDELQ+myCommandiABDELQ+myCommandiABCELQ+RunPySpt3LQ+myCommandiABCDH+myCommandiBCDEH+myCommandiACDEH+myCommandiABDEH+myCommandiABCEH+RunPySpt3H+myCommandiABCELQH+myCommandiBCDELQH+myCommandiACDELQH+myCommandiABDELQH+myCommandiABCELQH+RunPySpt3LQH+myCommandiABCDLQHPT+myCommandiACDELQHPT+myCommandiBCDELQHPT+myCommandiABDELQHPT+myCommandiABCELQHPT+RunPySpt3LQHPT
         myCommandNew= myCommandOLD+myCommandSp
         gp.AddMessage(myCommandNew)
         ####Python Code 4: full run of best parameters
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==1.0:\n"
         PythAHd4+="      resA='"+myCommandiABCDEL+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==2.0:\n"
         PythAHd4+="      resA='"+myCommandiABCDELQ+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==3.0:\n"
         PythAHd4+="      resA='"+myCommandiABCDEH+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==4.0:\n"
         PythAHd4+="      resA='"+myCommandiABCDELQH+"'"+"\n"+PythAHd4wr
         PythAHd4+="if RegN=="+Bvalx+" and FeatN==5.0:\n"
         PythAHd4+="      resA='"+myCommandiABCDELQHPT+"'"+"\n"+PythAHd4wr
         ########create python code 2
         ### 1. AVERAGE OC and AUC and store as value
         OutFiABCDEHt=OutFiABCDEH.replace("\\","/")
         OutFiABCDELt=OutFiABCDEL.replace("\\","/")
         OutFiABCDELQt=OutFiABCDELQ.replace("\\","/")
         OutFiABCDELQHt=OutFiABCDELQH.replace("\\","/")
         OutFiABCDELQHPTt=OutFiABCDELQHPT.replace("\\","/")
         FeTuReClAsSsHtL="L,1"
         FeTuReClAsSsHtLQ="LQ,2"
         FeTuReClAsSsHtH="H,3" 
         FeTuReClAsSsHtLQH="LQH,4" 
         FeTuReClAsSsHtLQHPT="LQHPF,5" 
         PythScOC="import numpy as np \n"
         PythScOC+="import csv, os \n"
         PythScOC+="csvfile = '"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_ALL.csv' \n"
         PythScOC+="dataRO=np.genfromtxt('"+outFoldGISii+"/tempOC.csv', delimiter=',', usecols=(3),skiprows=1) \n"
         PythScOC+="dataRO = dataRO[~np.isnan(dataRO)] \n"
         PythScOC+="ROtemp=dataRO.mean() \n"
         PythScOC+="ROtempS=str(ROtemp) \n"
         PythScOC+="dataAUC=np.genfromtxt('"+outFoldGISii+"/tempAUC.csv', delimiter=',', usecols=(0),skiprows=0) \n"
         PythScOC+="dataAUC = dataAUC[~np.isnan(dataAUC)] \n"
         PythScOC+="AUCtemp= dataAUC.mean() \n"
         PythScOC+="AUCtempS=str(AUCtemp) \n"
         PythScOC+="resA ='"+outFoldsp+","+Bvalx+",FeTuReClAsSsHt,'+ROtempS+','+AUCtempS \n"
         PythScOC+='file = open(csvfile, "r") \n'
         PythScOC+="filedata = file.read() \n"
         PythScOC+="file.close() \n"
         PythScOC+="newLine = resA+os.linesep+filedata \n"
         PythScOC+='file = open(csvfile, "w") \n'
         PythScOC+="file.write(newLine) \n"
         PythScOC+="file.close() \n"
         PythScOC+="os.remove('"+outFoldGISii+"/tempOC.csv') \n"
         PythScOC+="os.remove('"+outFoldGISii+"/tempAUC.csv') \n"
         myCommandiH_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtH)
         myCommandiL_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtL)
         myCommandiLQ_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtLQ)
         myCommandiLQH_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtLQH)
         myCommandiLQHPT_P=PythScOC.replace("FeTuReClAsSsHt",FeTuReClAsSsHtLQHPT)
         file = open(OutFiABCDEHt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiH_P)
         file.close()
         file = open(OutFiABCDELt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiL_P)
         file.close()
         file = open(OutFiABCDELQt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiLQ_P)
         file.close()
         file = open(OutFiABCDELQHt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiLQH_P)
         file.close()
         file = open(OutFiABCDELQHPTt+"/"+outFoldsp+".py", "w")
         file.write(myCommandiLQHPT_P)
         file.close()
         #gp.AddMessage(myCommandSp)
         gp.AddMessage("Batch Code successfully compiled and output for "+outFoldsp+": Beta "+Bvalx)
         gp.AddMessage("Successfully created GIS layers for: " + outFoldsp)
         gp.AddMessage("************************************************")
         gp.AddMessage("************************************************")
         gp.AddMessage("Generating final python scripts for spatial jackknifing MaxEnt models: " + outFoldsp)
      PythAHd4ft="csvfile = '"+outFoldspFii+"/"+outFoldsp+"_SUMSTATS_RANKED_MODELS.csv' \n"
      PythAHd4ft+='resA = "Reg Multi, Feature N, AUC, weighted RO"\n'
      PythAHd4ft+='file = open(csvfile, "r") \n'
      PythAHd4ft+="filedata = file.read() \n"
      PythAHd4ft+="file.close() \n"
      PythAHd4ft+="newLine = resA+os.linesep+filedata \n"
      PythAHd4ft+='file = open(csvfile, "w") \n'
      PythAHd4ft+="file.write(newLine) \n"
      PythAHd4ft+="file.close() \n"
      PythAHd4Fin=PythAHd4+PythAHd4ft
      file = open(outFoldGIS+"/FinalRank.py", "w")
      file.write(PythAHd4Fin)
      file.close()
      myCommandFinal=myCommandNew+RunPyAHd4+RunPyDel5+RunPySpt2
      file = open(outFoldspF+"/spatial_jackknife.bat", "w")
      file.write(myCommandFinal)
      file.close()
      file = open(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat", "r")
      filedata = file.read()
      file.close()
      newLine =myCommandFinal+filedata
      file = open(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat", "w")
      file.write(newLine)
      file.close()
    #cleanup workspace
    #except:
    #    gp.AddMessage(gp.GetMessages())
  if arcpy.Exists(BiFiT): 
    arcpy.Delete_management(BiFiT) 
  if arcpy.Exists(outfileShp): 
    arcpy.Delete_management(outfileShp) 
  if arcpy.Exists(outFolderTemp):   
    arcpy.Delete_management(outFolderTemp) 
  if arcpy.Exists(outFolderTemp2):   
    arcpy.Delete_management(outFolderTemp2) 
  if arcpy.Exists(outFolderTemp3):   
    arcpy.Delete_management(outFolderTemp3) 
  gp.AddMessage("************************************************")
  gp.AddMessage("************************************************")
  gp.AddMessage("************************************************")
  gp.AddMessage("************************************************")
  gp.AddMessage("***************IMPORTANT************************") 
  gp.AddMessage("Batch code, python scripts, and GIS layers were successfully created for all input species.")
  gp.AddMessage("                                                  ")
  gp.AddMessage("To run batch code, go to the specified output folder and execute the:")
  gp.AddMessage("                                                  ")
  gp.AddMessage("       'Step1_Optimize_MaxEnt_Model_Parameters.bat' batch file")
  gp.AddMessage("              (this script will optimize model parameters)")  
  gp.AddMessage("                                                  ")
  gp.AddMessage("Once the Step 1 batch file is finished, to generate your final SDMs execute:")
  gp.AddMessage("                                                  ")
  gp.AddMessage("       'Step2_Run_Optimized_MaxEnt_Models.bat' batch file")
  gp.AddMessage("                                                  ")
  gp.AddMessage("************************************************")
  gp.AddMessage("************************************************") 
#########################################
#########END Spatial Jackknife###########
#########################################
##*new-start
if nCPU > 1:
    for i in nCPUi:
     fileBATin =  (outFolderPy+"\\Step1_Optimize_MaxEnt_Model_Parameters.bat")
     fileBATout = (outFolderPy+"\\_CPU"+str(int(i))+"_code.bat")
     with open(fileBATin) as infile, open(fileBATout, 'w') as outfile:
       copy = False
       for line in infile:
         if line.strip() == str("##start"+str(vTs[(i-1)])):
             copy = True
         elif line.strip() == str("##end"+str(vTe[(i-1)])):
             copy = False
         elif copy:
             outfile.write(line)
 
if nCPU > 1:
  arcpy.Delete_management(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat")
  file = open(outFolderPy+"/Step1_Optimize_MaxEnt_Model_Parameters.bat", "w")
  for i in nCPUi:
     line = ("start cmd xxiixxc " +outFolderPy+"\_CPU"+str(int(i))+"_code.bat \n").replace("/","\\").replace("xxiixxc","/c")
     line+="timeout 5\n"
     file.write(line)
  file.close()

  
if nCPU > 1:
  file = open(outFolderPy+"/Step3_delete_CPU_climate_folders.bat", "w")
  for i in nCPUi:
     if i < int(nCPU):
          CLIMCOPY = outFolder + "\\_CPU"+str(i+1)+"_climate"
          line = ("echo y|rmdir xxiixxs " + str(CLIMCOPY)+" \n").replace("/","\\").replace("xxiixxs","/s")
          file.write(line)
  file.close()


##*new-end





