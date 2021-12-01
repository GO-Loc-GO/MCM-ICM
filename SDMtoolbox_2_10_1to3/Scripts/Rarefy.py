# Description:Rarefy
# Requirements: Spatial Analyst
# Author: Jason Brown
# 4/03/2014 v2
# Import system modules
import arcpy, sys, string, os, csv, glob, arcgisscripting 
gp = arcgisscripting.create()
arcpy.env.overwriteOutput = True

def str2bool(pstr):
    """Convert ESRI boolean string to Python boolean type"""
    return pstr == 'true'
#set workspace NOTE: all files must be in this directory
infile = sys.argv[1]
speciesField=sys.argv[2]
latitudeField=sys.argv[3]
longitudField=sys.argv[4]
outFolder = sys.argv[5]
outName=sys.argv[6]
resolution=sys.argv[7]
inProject = sys.argv[8]
inputBoolean = str2bool(sys.argv[9])
inHetero = sys.argv[10]
nClasses = sys.argv[11]
ClassType= sys.argv[12]
maxDist=sys.argv[13]
minDist=sys.argv[14]

arcpy.CreateFolder_management(outFolder,"TEMP_ilUli")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUlii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUliii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUliiii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUliiiii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUlvi")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUlvii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUlviii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUlviiii")
arcpy.CreateFolder_management(outFolder,"TEMP_ilUlxx")

outFolderTemp= outFolder + "/TEMP_ilUli"
outFolderTemp2= outFolder + "/TEMP_ilUlii"
outFolderTemp3= outFolder + "/TEMP_ilUliii"
outFolderTemp4= outFolder + "/TEMP_ilUliiii"
outFolderTemp5= outFolder + "/TEMP_ilUliiiii"
outFolderTemp6 = outFolder + "/TEMP_ilUlvi"
outFolderTemp7 = outFolder + "/TEMP_ilUlvii"
outFolderTemp8 = outFolder + "/TEMP_ilUlviii"
outFolderTemp9 = outFolder + "/TEMP_ilUlviiii"
outFolderTemp10 = outFolder + "/TEMP_ilUlxx"

TempShp1 = outFolderTemp + "/temp1.shp"
TempShp2 = outFolderTemp + "/temp2.shp"

#infile = sys.argv[1]
inSHP = str(infile).replace("\\","/")
SHPName1 = os.path.split(inSHP)[1]
SHPName = str(SHPName1)[:-4]
transformationOut ='#'


project1="PROJCS['Africa_Equidistant_Conic',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',25.0],PARAMETER['Standard_Parallel_1',20.0],PARAMETER['Standard_Parallel_2',-23.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
project2="PROJCS['Asia_North_Equidistant_Conic',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',95.0],PARAMETER['Standard_Parallel_1',15.0],PARAMETER['Standard_Parallel_2',65.0],PARAMETER['Latitude_Of_Origin',30.0],UNIT['Meter',1.0]]"
project3="PROJCS['Asia_South_Equidistant_Conic',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',125.0],PARAMETER['Standard_Parallel_1',7.0],PARAMETER['Standard_Parallel_2',-32.0],PARAMETER['Latitude_Of_Origin',-15.0],UNIT['Meter',1.0]]"
project4="PROJCS['Europe_Equidistant_Conic',GEOGCS['GCS_European_1950',DATUM['D_European_1950',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',10.0],PARAMETER['Standard_Parallel_1',43.0],PARAMETER['Standard_Parallel_2',62.0],PARAMETER['Latitude_Of_Origin',30.0],UNIT['Meter',1.0]]"
transformation4="ED_1950_To_WGS_1984_NTv2_Catalonia"
project5="PROJCS['North_America_Equidistant_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',20.0],PARAMETER['Standard_Parallel_2',60.0],PARAMETER['Latitude_Of_Origin',40.0],UNIT['Meter',1.0]]"
transformation5="WGS_1984_(ITRF00)_To_NAD_1983"
project6="PROJCS['USA_Contiguous_Equidistant_Conic',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-96.0],PARAMETER['Standard_Parallel_1',33.0],PARAMETER['Standard_Parallel_2',45.0],PARAMETER['Latitude_Of_Origin',39.0],UNIT['Meter',1.0]]"
transformation6="WGS_1984_(ITRF00)_To_NAD_1983"
project7="PROJCS['South_America_Equidistant_Conic',GEOGCS['GCS_South_American_1969',DATUM['D_South_American_1969',SPHEROID['GRS_1967_Truncated',6378160.0,298.25]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-60.0],PARAMETER['Standard_Parallel_1',-5.0],PARAMETER['Standard_Parallel_2',-42.0],PARAMETER['Latitude_Of_Origin',-32.0],UNIT['Meter',1.0]]"
transformation7="SAD_1969_To_WGS_1984_15"
project8="PROJCS['World_Azimuthal_Equidistant',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Azimuthal_Equidistant'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
project9="PROJCS['World_Equidistant_Conic',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Equidistant_Conic'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',60.0],PARAMETER['Standard_Parallel_2',60.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
project10="PROJCS['World_Plate_Carree',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Plate_Carree'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]"
  
if inProject == "World: Azimuthal Equidistant":
    ProjectOut=project8
if inProject == "World: Equidistant Conic":
    ProjectOut=project9
if inProject == "World: Plate Carree":
    ProjectOut=project10
if inProject == "Continent: Africa Equidistant Conic":
    ProjectOut=project1
if inProject == "Continent: Asia North Equidistant Conic":
    ProjectOut=project2
if inProject == "Continent: Asia South Equidistant Conic":
    ProjectOut=project3
if inProject == "Continent: Europe Equidistant Conic":
    ProjectOut=project4
    transformationOut = transformation4
if inProject == "Continent: North America Equidistant Conic":
    ProjectOut=project5
    transformationOut = transformation5
if inProject == "Continent: USA Contiguous Equidistant Conic":
    ProjectOut=project6
    transformationOut = transformation6
if inProject == "Continent: South America Equidistant Conic":
    ProjectOut=project7
    transformationOut = transformation7

#step1 copy in file, then project to equidistant projection
outPoints=outFolder+"/"+outName+"_temp.shp"
outPoints2=outFolder+"/"+outName+"_temp2.shp"
outPointsF=outFolder+"/"+outName+"_spatially_rarified_locs.shp"
gp.AddMessage(" ")
gp.AddMessage("***Projecting "+infile+" to Equal Distant Projection")
gp.AddMessage(" ")

#arcpy.CopyFeatures_management(infile,outPoints)
arcpy.Project_management(infile,outPoints,ProjectOut,transformationOut,"#")
latitudeField=sys.argv[3]
longitudField=sys.argv[4]

#step2 delete spatial duplications
#count all points in input
totPnts1= arcpy.GetCount_management(outPoints)
totPntsN1= int(str(totPnts1))
gp.addmessage(str(totPntsN1)+ " points input")
gp.AddMessage(" ")

#setting up inputs
speciesField1=str(speciesField)
latitudeField1=str(latitudeField)
longitudField1=str(longitudField)
groupSLL=str(speciesField1)+";"+str(latitudeField1)+";"+str(longitudField1)
gp.AddMessage("***Step 1:Remove spatially redundant occurrence localities for each species")
gp.AddMessage(" ")
arcpy.DeleteIdentical_management(outPoints,groupSLL,"#","0")

#count number of duplicate points 
totPnts2= arcpy.GetCount_management(outPoints)
totPntsN2= int(str(totPnts2))
diffnumVal2=  int(totPntsN1-totPntsN2)
gp.addmessage(str(diffnumVal2) + " duplicates removed (of "+ str(totPntsN1)+" points)")
gp.AddMessage(" ")
gp.addmessage(str(totPntsN2) + " points remain")
gp.AddMessage(" ")
nClassesIN=(int(nClasses))
if nClassesIN > 5:
      gp.AddMessage("Too many classes, reduce to between 2-5")
      del gp
#step3 spatial rarefy---SINGLE CLASS
if inputBoolean== False:
   groupSP="Shape;"+str(speciesField)
   resolutionS=str(resolution)
   gp.AddMessage("***Step 2: Spatially rarefying occurrence data at "+resolutionS)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(outPoints,groupSP,resolutionS,"0")
   #count number of duplicate points 
   totPnts3= arcpy.GetCount_management(outPoints)
   totPntsN3= int(str(totPnts3))
   diffnumVal3=  int(totPntsN2-totPntsN3)
   gp.addmessage(str(diffnumVal3) + " spatially autocorrelated points removed (of "+ str(totPntsN2)+" points)")
   gp.AddMessage(" ")
   gp.addmessage("Final dataset includes "+str(totPntsN3)+" unique occurrence points")
   gp.AddMessage(" ")
   ##project back into WGS1980
   gp.AddMessage("Projecting shapefile back to original WGS 1984 geographic projection")
   gp.AddMessage(" ")
   arcpy.Project_management(outPoints,outPointsF,"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","#")
   arcpy.Delete_management(outPoints)
   gp.AddMessage("FINISHED SUCCESFULLY")

#step3 spatial rarefy---GRADUATED CLASSES:5CLASSES
if inputBoolean== True and nClassesIN == 5:
   emptyShape=outFolderTemp+"/empty.shp"
   arcpy.Copy_management(outPoints,emptyShape)
   arcpy.DeleteRows_management(emptyShape)
   arcpy.gp.Slice_sa(inHetero,outFolder+"/spatial_groups.tif",nClassesIN,ClassType,"1")
   arcpy.gp.ExtractValuesToPoints_sa(outPoints,outFolder+"/spatial_groups.tif",outFolderTemp+"/OutPtsEall.shp","NONE","VALUE_ONLY")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP", "[RASTERVALU]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","RASTERVALU")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU", "[TEMP]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","TEMP")
   ###CALCULATE_RAREFY_DISTANCES
   arcpy.MakeFeatureLayer_management(outFolderTemp+"/OutPtsEall.shp", "OutPtsEall_View")
   arcpy.SelectLayerByAttribute_management("OutPtsEall_View","NEW_SELECTION", '"RASTERVALU" =-9999')
   arcpy.CalculateField_management("OutPtsEall_View", field="RASTERVALU", expression="1", expression_type="VB", code_block="")
   def get_num(x):
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
   def get_text(x):
    return str(''.join(ele for ele in x if ele.isalpha() or ele == ' '))
   inMax = get_num(maxDist)
   inMin = get_num(minDist)
   inUnits = get_text(minDist)
   inMaxV = float(inMax)
   inMinV = float(inMin)
   interVal=(inMaxV-inMinV)/(nClassesIN-1)
   Dcm1=inMinV+interVal
   Dcm2=Dcm1+interVal
   Dcm3=Dcm2+interVal
   Dcm1T=str(Dcm1)+inUnits
   Dcm2T=str(Dcm2)+inUnits
   Dcm3T=str(Dcm3)+inUnits
   ####TEXTOUT
   groupSP="Shape;"+str(speciesField)
   resolutionS=str(resolution)
   gp.AddMessage("***Step 2. Phase 1: Spatially rarefying all occurrence data at "+minDist)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(outFolderTemp+"/OutPtsEall.shp",groupSP,minDist,"0")
   #count number of duplicate points 
   totPnts3= arcpy.GetCount_management(outFolderTemp+"/OutPtsEall.shp")
   totPntsN3= int(str(totPnts3))
   diffnumVal3=  int(totPntsN2-totPntsN3)
   gp.addmessage(str(diffnumVal3) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE1
   from Scripts import Rarefy1####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD2
   E0A= outFolderTemp2+"/0.shp"
   E1A= outFolderTemp2+"/1.shp"
   E2A= outFolderTemp2+"/2.shp"
   E3A= outFolderTemp2+"/3.shp"
   E4A= outFolderTemp2+"/4.shp"
   E5A= outFolderTemp2+"/5.shp"
   IN_EA=str(E1A+";"+E2A+";"+E3A+";"+E4A)
   EM1_4= outFolderTemp2+"/Merge1.shp"
   #count number of duplicate points 
   if arcpy.Exists(E0A):
       MISdataPN=arcpy.GetCount_management(E0A)
       MISdataPA=str(MISdataPN)
       MISdataP=int(MISdataPA)
   else:
       MISdataP=0
       arcpy.Copy_management(emptyShape,E0A)
   if arcpy.Exists(E1A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1A)
   if arcpy.Exists(E2A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E2A)
   if arcpy.Exists(E3A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E3A)
   if arcpy.Exists(E4A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E4A)
   if arcpy.Exists(E5A):
       group5Pnts=arcpy.GetCount_management(E5A)
       group5PntsNA=str(group5Pnts)
       group5PntsN=int(group5PntsNA)
   else:
       group5PntsN=0
       arcpy.Copy_management(emptyShape,E5A)
   arcpy.Merge_management(IN_EA,EM1_4,"#")
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 2: Spatially rarefying occurrence data in groups 1-4 at "+Dcm1T)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(EM1_4,groupSP,Dcm1T,"0")
   totPnts4= arcpy.GetCount_management(EM1_4)
   totPntsN4= int(str(totPnts4))
   diffnumVal4=  int(totPntsN3-totPntsN4-group5PntsN-MISdataP)
   gp.addmessage(str(diffnumVal4) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE2
   from Scripts import Rarefy2
   E1B= outFolderTemp3+"/1.shp"
   E2B= outFolderTemp3+"/2.shp"
   E3B= outFolderTemp3+"/3.shp"
   E4B= outFolderTemp3+"/4.shp"
   EM1_3= outFolderTemp3+"/Merge2.shp"
   IN_EB=str(E1B+";"+E2B+";"+E3B)   
   #count number of duplicate points 
   if arcpy.Exists(E1B):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1B)
   if arcpy.Exists(E2B):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E2B)
   if arcpy.Exists(E3B):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E3B)
   if arcpy.Exists(E4B):
      group4Pnts=arcpy.GetCount_management(E4B)
      group4PntsNA=str(group4Pnts)
      group4PntsN=int(group4PntsNA)
   else:
       group4PntsN=0
       arcpy.Copy_management(emptyShape,E4B)
   arcpy.Merge_management(IN_EB,EM1_3,"#")
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 3: Spatially rarefying occurrence data in groups 1-3 at "+Dcm2T)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(EM1_3,groupSP,Dcm2T,"0")
   totPnts5= arcpy.GetCount_management(EM1_3)
   totPntsN5= int(str(totPnts5))
   diffnumVal5=  int(totPntsN4-totPntsN5-group4PntsN)
   gp.addmessage(str(diffnumVal5) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE4
   from Scripts import Rarefy3####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD4
   E1C= outFolderTemp4+"/1.shp"
   E2C= outFolderTemp4+"/2.shp"
   E3C= outFolderTemp4+"/3.shp"
   EM1_2= outFolderTemp4+"/Merge3.shp"
   IN_EC=str(E1C+";"+E2C)
   #count number of duplicate points 
   if arcpy.Exists(E1C):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1C)
   if arcpy.Exists(E2C):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E2C)
   if arcpy.Exists(E3C):
      group5Pnts=arcpy.GetCount_management(E3C)
      group5PntsNA=str(group5Pnts)
      group5PntsN=int(group5PntsNA)
   else:
       group5PntsN=0
       arcpy.Copy_management(emptyShape,E3C)
   arcpy.Merge_management(IN_EC,EM1_2,"#")
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 4: Spatially rarefying occurrence data in groups 1-2 at "+Dcm3T)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(EM1_2,groupSP,Dcm3T,"0")
   totPnts6= arcpy.GetCount_management(EM1_2)
   totPntsN6= int(str(totPnts6))
   diffnumVal6=  int(totPntsN5-totPntsN6-group5PntsN)
   gp.addmessage(str(diffnumVal6) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE5
   from Scripts import Rarefy4####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD5
   E1D= outFolderTemp5+"/1.shp"
   E2D= outFolderTemp5+"/2.shp"
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 5: Spatially rarefying occurrence data in group 1 at "+maxDist)
   gp.AddMessage(" ")
   if arcpy.Exists(E1D):
      totPnts7a=arcpy.GetCount_management(E1D)
      totPntsN7aT=str(totPnts7a)
      totPntsN7a=int(totPntsN7aT)
   else:
       totPntsN7a=0
       arcpy.Copy_management(emptyShape,E1D)
   if arcpy.Exists(E2D):
       v=1
   else:
       arcpy.Copy_management(emptyShape,E2D)
   arcpy.DeleteIdentical_management(E1D,groupSP,maxDist,"0")
   #count number of duplicate points 
   totPntsN7b=0
   if arcpy.Exists(E1D):
      totPnts7b=arcpy.GetCount_management(E1D)
      totPntsN7bT=str(totPnts7b)
      totPntsN7b=int(totPntsN7bT)
   diffnumVal7=  int(totPntsN7a-totPntsN7b)
   gp.addmessage(str(diffnumVal7) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")   
   ###MERGE_ALL_DATSETS
   IN_ED=str(E5A+";"+E4B+";"+E3C+";"+E2D+";"+E1D)
   arcpy.Merge_management(IN_ED,outPoints2,"#")
   totPnts8= arcpy.GetCount_management(outPoints2)
   totPntsN8= int(str(totPnts8))
   ##project back into WGS1984
   gp.AddMessage("Projecting shapefile back to original WGS 1984 geographic projection")
   gp.AddMessage(" ")
   arcpy.Project_management(outPoints2,outPointsF,"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","#")
   arcpy.Delete_management(outPoints)
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   gp.AddMessage("FINISHED SUCCESFULLY")
   gp.addmessage("Starting number of localities: "+str(totPntsN1))   
   gp.addmessage("Spatially redundant occurrence localities removed: "+str(diffnumVal2))
   gp.addmessage("The following spatially autocorrelated localities")
   gp.addmessage("were hierarchically removed, as follows:")
   gp.addmessage("Phase 1: "+str(diffnumVal3) + " points removed from groups 1-5 at "+ minDist)
   gp.addmessage("Phase 2: "+str(diffnumVal4) + " points removed from groups 1-4 at "+ Dcm1T)
   gp.addmessage("Phase 3: "+str(diffnumVal5) + " points removed from groups 1-3 at "+ Dcm2T)
   gp.addmessage("Phase 4: "+str(diffnumVal6) + " points removed from groups 1-2 at "+ Dcm3T)
   gp.addmessage("Phase 5: "+str(diffnumVal7) + " points removed from group 1 at "+ maxDist)
   gp.AddMessage(" ")
   gp.addmessage("Final dataset includes "+str(totPntsN8)+" unique occurrence points")
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   if MISdataP != 0:
     #output csv
     gp.AddMessage("WARNING!: "+str(MISdataPN)+" localities fell outside of "+str(inHetero)+ " and were not included in spatial rarefying")
     gp.AddMessage("****************************************")
     gp.AddMessage("See file:"+str(outFolder) + "/" + str(outName) + "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv for localities")
     CSVFile = outFolder + "/" + outName+ "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv" 
     fieldnames = [f.name for f in arcpy.ListFields(E0A) if f.type <> 'Geometry']
     for i,f in enumerate(fieldnames):
         if f == 'Shape' or f == 'FID' or f == 'OBJECTID':
             del fieldnames[i]
     with open(CSVFile, 'w') as f:
         f.write(','.join(fieldnames)+'\n') #csv headers
         with arcpy.da.SearchCursor(E0A, fieldnames) as cursor:
             for row in cursor:
                  f.write(','.join([str(r) for r in row])+'\n')

#step3 spatial rarefy---GRADUATED CLASSES:4CLASSES
if inputBoolean== True and nClassesIN == 4:
   emptyShape=outFolderTemp+"/empty.shp"
   arcpy.Copy_management(outPoints,emptyShape)
   arcpy.DeleteRows_management(emptyShape)
   arcpy.gp.Slice_sa(inHetero,outFolder+"/spatial_groups.tif",nClassesIN,ClassType,"1")
   arcpy.gp.ExtractValuesToPoints_sa(outPoints,outFolder+"/spatial_groups.tif",outFolderTemp+"/OutPtsEall.shp","NONE","VALUE_ONLY")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP", "[RASTERVALU]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","RASTERVALU")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU", "[TEMP]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","TEMP")
   arcpy.MakeFeatureLayer_management(outFolderTemp+"/OutPtsEall.shp", "OutPtsEall_View")
   arcpy.SelectLayerByAttribute_management("OutPtsEall_View","NEW_SELECTION", '"RASTERVALU" =-9999')
   arcpy.CalculateField_management("OutPtsEall_View", field="RASTERVALU", expression="1", expression_type="VB", code_block="")
   ###CALCULATE_RAREFY_DISTANCES
   def get_num(x):
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
   def get_text(x):
    return str(''.join(ele for ele in x if ele.isalpha() or ele == ' '))
   inMax = get_num(maxDist)
   inMin = get_num(minDist)
   inUnits = get_text(minDist)
   inMaxV = float(inMax)
   inMinV = float(inMin)
   interVal=(inMaxV-inMinV)/(nClassesIN-1)
   Dcm1=inMinV+interVal
   Dcm2=Dcm1+interVal
   Dcm1T=str(Dcm1)+inUnits
   Dcm2T=str(Dcm2)+inUnits
   ####TEXTOUT
   groupSP="Shape;"+str(speciesField)
   resolutionS=str(resolution)
   gp.AddMessage("***Step 2. Phase 1: Spatially rarefying all occurrence data at "+minDist)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(outFolderTemp+"/OutPtsEall.shp",groupSP,minDist,"0")
   #count number of duplicate points 
   totPnts3= arcpy.GetCount_management(outFolderTemp+"/OutPtsEall.shp")
   totPntsN3= int(str(totPnts3))
   diffnumVal3=  int(totPntsN2-totPntsN3)
   gp.addmessage(str(diffnumVal3) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE1
   from Scripts import Rarefy1####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD2
   E0A= outFolderTemp2+"/0.shp"
   E1A= outFolderTemp2+"/1.shp"
   E2A= outFolderTemp2+"/2.shp"
   E3A= outFolderTemp2+"/3.shp"
   E4A= outFolderTemp2+"/4.shp"
   IN_EA=str(E1A+";"+E2A+";"+E3A)
   EM1_3= outFolderTemp2+"/Merge1.shp"
   #count number of duplicate points 
   if arcpy.Exists(E0A):
       MISdataPN=arcpy.GetCount_management(E0A)
       MISdataPA=str(MISdataPN)
       MISdataP=int(MISdataPA)
   else:
       MISdataP=0
       arcpy.Copy_management(emptyShape,E0A)
   if arcpy.Exists(E1A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1A)
   if arcpy.Exists(E2A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E2A)
   if arcpy.Exists(E3A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E3A)
   if arcpy.Exists(E4A):
       group5Pnts=arcpy.GetCount_management(E4A)
       group5PntsNA=str(group5Pnts)
       group5PntsN=int(group5PntsNA)
   else:
       group5PntsN=0
       arcpy.Copy_management(emptyShape,E4A)
   arcpy.Merge_management(IN_EA,EM1_3,"#")
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 2: Spatially rarefying occurrence data in groups 1-3 at "+Dcm1T)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(EM1_3,groupSP,Dcm1T,"0")
   totPnts4= arcpy.GetCount_management(EM1_3)
   totPntsN4= int(str(totPnts4))
   diffnumVal4=  int(totPntsN3-totPntsN4-group5PntsN-MISdataP)
   gp.addmessage(str(diffnumVal4) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")   
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE2
   from Scripts import Rarefy2
   E1B= outFolderTemp3+"/1.shp"
   E2B= outFolderTemp3+"/2.shp"
   E3B= outFolderTemp3+"/3.shp"
   EM1_2= outFolderTemp3+"/Merge2.shp"
   IN_EB=str(E1B+";"+E2B)   
   #count number of duplicate points 
   if arcpy.Exists(E1B):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1B)
   if arcpy.Exists(E2B):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E2B)
   if arcpy.Exists(E3B):
      group4Pnts=arcpy.GetCount_management(E3B)
      group4PntsNA=str(group4Pnts)
      group4PntsN=int(group4PntsNA)
   else:
       group4PntsN=0
       arcpy.Copy_management(emptyShape,E3B)
   arcpy.Merge_management(IN_EB,EM1_2,"#")
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 3: Spatially rarefying occurrence data in groups 1-2 at "+Dcm2T)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(EM1_2,groupSP,Dcm2T,"0")
   totPnts5= arcpy.GetCount_management(EM1_2)
   totPntsN5= int(str(totPnts5))
   diffnumVal5=  int(totPntsN4-totPntsN5-group4PntsN)
   gp.addmessage(str(diffnumVal5) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE4
   from Scripts import Rarefy3####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD4
   E1C= outFolderTemp4+"/1.shp"
   E2C= outFolderTemp4+"/2.shp"
   #count number of duplicate points 
   if arcpy.Exists(E1C):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1C)
   if arcpy.Exists(E2C):
      group5Pnts=arcpy.GetCount_management(E2C)
      group5PntsNA=str(group5Pnts)
      group5PntsN=int(group5PntsNA)
   else:
       group5PntsN=0
       arcpy.Copy_management(emptyShape,E2C)
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 4: Spatially rarefying occurrence data in group 1 at "+str(maxDist))
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(E1C,groupSP,maxDist,"0")
   totPnts6= arcpy.GetCount_management(E1C)
   totPntsN6= int(str(totPnts6))
   diffnumVal6=  int(totPntsN5-totPntsN6-group5PntsN)
   gp.addmessage(str(diffnumVal6) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   ###MERGE_ALL_DATSETS
   IN_ED=str(E4A+";"+E3B+";"+E2C+";"+E1C)
   arcpy.Merge_management(IN_ED,outPoints2,"#")
   totPnts8= arcpy.GetCount_management(outPoints2)
   totPntsN8= int(str(totPnts8))
   ##project back into WGS1984
   gp.AddMessage("Projecting shapefile back to original WGS 1984 geographic projection")
   gp.AddMessage(" ")
   arcpy.Project_management(outPoints2,outPointsF,"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","#")
   arcpy.Delete_management(outPoints)
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   gp.AddMessage("FINISHED SUCCESFULLY")
   gp.addmessage("Starting number of localities: "+str(totPntsN1))   
   gp.addmessage("Spatially redundant occurrence localities removed: "+str(diffnumVal2))
   gp.addmessage("The following spatially autocorrelated localities")
   gp.addmessage("were hierarchically removed, as follows:")
   gp.addmessage("Phase 1: "+str(diffnumVal3) + " points removed from groups 1-4 at "+ minDist)
   gp.addmessage("Phase 2: "+str(diffnumVal4) + " points removed from groups 1-3 at "+ Dcm1T)
   gp.addmessage("Phase 3: "+str(diffnumVal5) + " points removed from groups 1-2 at "+ Dcm2T)
   gp.addmessage("Phase 4: "+str(diffnumVal6) + " points removed from group 1 at "+ str(maxDist))
   gp.AddMessage(" ")
   gp.addmessage("Final dataset includes "+str(totPntsN8)+" unique occurrence points")
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   if MISdataP != 0:
     #output csv
     gp.AddMessage("WARNING!: "+str(MISdataPN)+" localities fell outside of "+str(inHetero)+ " and were not included in spatial rarefying")
     gp.AddMessage("****************************************")
     gp.AddMessage("See file:"+str(outFolder) + "/" + str(outName) + "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv for localities")
     CSVFile = outFolder + "/" + outName+ "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv" 
     fieldnames = [f.name for f in arcpy.ListFields(E0A) if f.type <> 'Geometry']
     for i,f in enumerate(fieldnames):
         if f == 'Shape' or f == 'FID' or f == 'OBJECTID':
             del fieldnames[i]
     with open(CSVFile, 'w') as f:
         f.write(','.join(fieldnames)+'\n') #csv headers
         with arcpy.da.SearchCursor(E0A, fieldnames) as cursor:
             for row in cursor:
                  f.write(','.join([str(r) for r in row])+'\n')
#################################################
#step3 spatial rarefy---GRADUATED CLASSES:3CLASSES
if inputBoolean== True and nClassesIN == 3:
   emptyShape=outFolderTemp+"/empty.shp"
   arcpy.Copy_management(outPoints,emptyShape)
   arcpy.DeleteRows_management(emptyShape)
   arcpy.gp.Slice_sa(inHetero,outFolder+"/spatial_groups.tif",nClassesIN,ClassType,"1")
   arcpy.gp.ExtractValuesToPoints_sa(outPoints,outFolder+"/spatial_groups.tif",outFolderTemp+"/OutPtsEall.shp","NONE","VALUE_ONLY")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP", "[RASTERVALU]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","RASTERVALU")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU", "[TEMP]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","TEMP")
   arcpy.MakeFeatureLayer_management(outFolderTemp+"/OutPtsEall.shp", "OutPtsEall_View")
   arcpy.SelectLayerByAttribute_management("OutPtsEall_View","NEW_SELECTION", '"RASTERVALU" =-9999')
   arcpy.CalculateField_management("OutPtsEall_View", field="RASTERVALU", expression="1", expression_type="VB", code_block="")
   ###CALCULATE_RAREFY_DISTANCES
   def get_num(x):
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
   def get_text(x):
    return str(''.join(ele for ele in x if ele.isalpha() or ele == ' '))
   inMax = get_num(maxDist)
   inMin = get_num(minDist)
   inUnits = get_text(minDist)
   inMaxV = float(inMax)
   inMinV = float(inMin)
   interVal=(inMaxV-inMinV)/(nClassesIN-1)
   Dcm1=inMinV+interVal
   Dcm1T=str(Dcm1)+inUnits
   ####TEXTOUT
   groupSP="Shape;"+str(speciesField)
   resolutionS=str(resolution)
   gp.AddMessage("***Step 2. Phase 1: Spatially rarefying all occurrence data at "+minDist)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(outFolderTemp+"/OutPtsEall.shp",groupSP,minDist,"0")
   #count number of duplicate points 
   totPnts3= arcpy.GetCount_management(outFolderTemp+"/OutPtsEall.shp")
   totPntsN3= int(str(totPnts3))
   diffnumVal3=  int(totPntsN2-totPntsN3)
   gp.addmessage(str(diffnumVal3) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE1
   from Scripts import Rarefy1####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD2
   E0A= outFolderTemp2+"/0.shp"
   E1A= outFolderTemp2+"/1.shp"
   E2A= outFolderTemp2+"/2.shp"
   E3A= outFolderTemp2+"/3.shp"
   IN_EA=str(E1A+";"+E2A)
   EM1_2= outFolderTemp2+"/Merge1.shp"
   #count number of duplicate points 
   if arcpy.Exists(E0A):
       MISdataPN=arcpy.GetCount_management(E0A)
       MISdataPA=str(MISdataPN)
       MISdataP=int(MISdataPA)
   else:
       MISdataP=0
       arcpy.Copy_management(emptyShape,E0A)
   if arcpy.Exists(E1A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1A)
   if arcpy.Exists(E2A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E2A)
   if arcpy.Exists(E3A):
       group5Pnts=arcpy.GetCount_management(E3A)
       group5PntsNA=str(group5Pnts)
       group5PntsN=int(group5PntsNA)
   else:
       group5PntsN=0
       arcpy.Copy_management(emptyShape,E3A)
   arcpy.Merge_management(IN_EA,EM1_2,"#")
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 2: Spatially rarefying occurrence data in groups 1-2 at "+Dcm1T)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(EM1_2,groupSP,Dcm1T,"0")
   totPnts4= arcpy.GetCount_management(EM1_2)
   totPntsN4= int(str(totPnts4))
   diffnumVal4=  int(totPntsN3-totPntsN4-group5PntsN-MISdataP)
   gp.addmessage(str(diffnumVal4) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE2
   from Scripts import Rarefy2
   E1B= outFolderTemp3+"/1.shp"
   E2B= outFolderTemp3+"/2.shp"
   EM1_2= outFolderTemp3+"/Merge2.shp" 
   #count number of duplicate points 
   if arcpy.Exists(E1B):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1B)
   if arcpy.Exists(E2B):
      group4Pnts=arcpy.GetCount_management(E2B)
      group4PntsNA=str(group4Pnts)
      group4PntsN=int(group4PntsNA)
   else:
       group4PntsN=0
       arcpy.Copy_management(emptyShape,E2B)
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 3: Spatially rarefying occurrence data in group 1 at "+str(maxDist))
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(E1B,groupSP,maxDist,"0")
   totPnts5= arcpy.GetCount_management(E1B)
   totPntsN5= int(str(totPnts5))
   diffnumVal5=  int(totPntsN4-totPntsN5-group4PntsN)
   gp.addmessage(str(diffnumVal5) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   
   ###MERGE_ALL_DATSETS
   IN_ED=str(E3A+";"+E2B+";"+E1B)
   arcpy.Merge_management(IN_ED,outPoints2,"#")
   totPnts8= arcpy.GetCount_management(outPoints2)
   totPntsN8= int(str(totPnts8))
   ##project back into WGS1984
   gp.AddMessage("Projecting shapefile back to original WGS 1984 geographic projection")
   gp.AddMessage(" ")
   arcpy.Project_management(outPoints2,outPointsF,"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","#")
   arcpy.Delete_management(outPoints)
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   gp.AddMessage("FINISHED SUCCESFULLY")
   gp.addmessage("Starting number of localities: "+str(totPntsN1))   
   gp.addmessage("Spatially redundant occurrence localities removed: "+str(diffnumVal2))
   gp.addmessage("The following spatially autocorrelated localities")
   gp.addmessage("were hierarchically removed, as follows:")
   gp.addmessage("Phase 1: "+str(diffnumVal3) + " points removed from groups 1-3 at "+ minDist)
   gp.addmessage("Phase 2: "+str(diffnumVal4) + " points removed from groups 1-2 at "+ Dcm1T)
   gp.addmessage("Phase 3: "+str(diffnumVal5) + " points removed from group 1 at "+ str(maxDist))
   gp.AddMessage(" ")
   gp.addmessage("Final dataset includes "+str(totPntsN8)+" unique occurrence points")
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   if MISdataP != 0:
     #output csv
     gp.AddMessage("WARNING!: "+str(MISdataPN)+" localities fell outside of "+str(inHetero)+ " and were not included in spatial rarefying")
     gp.AddMessage("****************************************")
     gp.AddMessage("See file:"+str(outFolder) + "/" + str(outName) + "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv for localities")
     CSVFile = outFolder + "/" + outName+ "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv" 
     fieldnames = [f.name for f in arcpy.ListFields(E0A) if f.type <> 'Geometry']
     for i,f in enumerate(fieldnames):
         if f == 'Shape' or f == 'FID' or f == 'OBJECTID':
             del fieldnames[i]
     with open(CSVFile, 'w') as f:
         f.write(','.join(fieldnames)+'\n') #csv headers
         with arcpy.da.SearchCursor(E0A, fieldnames) as cursor:
             for row in cursor:
                  f.write(','.join([str(r) for r in row])+'\n')
##############################################
#step3 spatial rarefy---GRADUATED CLASSES:2CLASSES
if inputBoolean== True and nClassesIN == 2:
   emptyShape=outFolderTemp+"/empty.shp"
   arcpy.Copy_management(outPoints,emptyShape)
   arcpy.DeleteRows_management(emptyShape)
   arcpy.gp.Slice_sa(inHetero,outFolder+"/spatial_groups.tif",nClassesIN,ClassType,"1")
   arcpy.gp.ExtractValuesToPoints_sa(outPoints,outFolder+"/spatial_groups.tif",outFolderTemp+"/OutPtsEall.shp","NONE","VALUE_ONLY")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp", "TEMP", "[RASTERVALU]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","RASTERVALU")
   arcpy.AddField_management(outFolderTemp+"/OutPtsEall.shp", "RASTERVALU","SHORT","1","","","","")
   arcpy.CalculateField_management(outFolderTemp+"/OutPtsEall.shp","RASTERVALU", "[TEMP]", "VB","#")
   arcpy.DeleteField_management(outFolderTemp+"/OutPtsEall.shp","TEMP")
   arcpy.MakeFeatureLayer_management(outFolderTemp+"/OutPtsEall.shp", "OutPtsEall_View")
   arcpy.SelectLayerByAttribute_management("OutPtsEall_View","NEW_SELECTION", '"RASTERVALU" =-9999')
   arcpy.CalculateField_management("OutPtsEall_View", field="RASTERVALU", expression="1", expression_type="VB", code_block="")
   def get_num(x):
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.'))
   def get_text(x):
    return str(''.join(ele for ele in x if ele.isalpha() or ele == ' '))
   inMax = get_num(maxDist)
   inMin = get_num(minDist)
   inUnits = get_text(minDist)
   inMaxV = float(inMax)
   inMinV = float(inMin)
   ####TEXTOUT
   groupSP="Shape;"+str(speciesField)
   resolutionS=str(resolution)
   gp.AddMessage("***Step 2. Phase 1: Spatially rarefying all occurrence data at "+minDist)
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(outFolderTemp+"/OutPtsEall.shp",groupSP,minDist,"0")
   #count number of duplicate points 
   totPnts3= arcpy.GetCount_management(outFolderTemp+"/OutPtsEall.shp")
   totPntsN3= int(str(totPnts3))
   diffnumVal3=  int(totPntsN2-totPntsN3)
   gp.addmessage(str(diffnumVal3) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
   #SPLIT_BY_CLASS_THE_RAREFY_CLASSES_HIERARCHICALLY_PHASE1
   from Scripts import Rarefy1####VERSION1--SPLIT BASED ON RASTER VALUE!!! EXPORT TO TEMPFOLD2
   E0A= outFolderTemp2+"/0.shp"
   E1A= outFolderTemp2+"/1.shp"
   E2A= outFolderTemp2+"/2.shp"
   EM1_2= outFolderTemp2+"/Merge1.shp"
   #count number of duplicate points 
   if arcpy.Exists(E0A):
       MISdataPN=arcpy.GetCount_management(E0A)
       MISdataPA=str(MISdataPN)
       MISdataP=int(MISdataPA)
   else:
       MISdataP=0
       arcpy.Copy_management(emptyShape,E0A)
   if arcpy.Exists(E1A):
       V=1
   else:
       arcpy.Copy_management(emptyShape,E1A)
   if arcpy.Exists(E2A):
       group5Pnts=arcpy.GetCount_management(E2A)
       group5PntsNA=str(group5Pnts)
       group5PntsN=int(group5PntsNA)
   else:
       group5PntsN=0
       arcpy.Copy_management(emptyShape,E2A)
   ####TEXTOUT_PHASE2
   gp.AddMessage("***Step 2. Phase 2: Spatially rarefying occurrence data in group 1 at "+str(maxDist))
   gp.AddMessage(" ")
   arcpy.DeleteIdentical_management(E1A,groupSP,maxDist,"0")
   totPnts4= arcpy.GetCount_management(E1A)
   totPntsN4= int(str(totPnts4))
   diffnumVal4=  int(totPntsN3-totPntsN4-group5PntsN-MISdataP)
   gp.addmessage(str(diffnumVal4) + " spatially autocorrelated points removed")
   gp.AddMessage(" ")
      
   ###MERGE_ALL_DATSETS
   IN_ED=str(E2A+";"+E1A)
   arcpy.Merge_management(IN_ED,outPoints2,"#")
   totPnts8= arcpy.GetCount_management(outPoints2)
   totPntsN8= int(str(totPnts8))
   ##project back into WGS1984
   gp.AddMessage("Projecting shapefile back to original WGS 1984 geographic projection")
   gp.AddMessage(" ")
   arcpy.Project_management(outPoints2,outPointsF,"GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]","#","#")
   arcpy.Delete_management(outPoints)
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   gp.AddMessage("FINISHED SUCCESFULLY")
   gp.addmessage("Starting number of localities: "+str(totPntsN1))   
   gp.addmessage("Spatially redundant occurrence localities removed: "+str(diffnumVal2))
   gp.addmessage("The following spatially autocorrelated localities")
   gp.addmessage("were hierarchically removed, as follows:")
   gp.addmessage("Phase 1: "+str(diffnumVal3) + " points removed from groups 1-2 at "+ minDist)
   gp.addmessage("Phase 2: "+str(diffnumVal4) + " points removed from group 1 at "+str(maxDist))
   gp.AddMessage(" ")
   gp.addmessage("Final dataset includes "+str(totPntsN8)+" unique occurrence points")
   gp.AddMessage("****************************************")
   gp.AddMessage("****************************************") 
   if MISdataP != 0:
     #output csv
     gp.AddMessage("WARNING!: "+str(MISdataPN)+" localities fell outside of "+str(inHetero)+ " and were not included in spatial rarefying")
     gp.AddMessage("****************************************")
     gp.AddMessage("See file:"+str(outFolder) + "/" + str(outName) + "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv for localities")
     CSVFile = outFolder + "/" + outName+ "_EXCLUDED_PTS_OUTSIDE_OF_HETEROGENEITY_RASTER.csv" 
     fieldnames = [f.name for f in arcpy.ListFields(E0A) if f.type <> 'Geometry']
     for i,f in enumerate(fieldnames):
         if f == 'Shape' or f == 'FID' or f == 'OBJECTID':
             del fieldnames[i]
     with open(CSVFile, 'w') as f:
         f.write(','.join(fieldnames)+'\n') #csv headers
         with arcpy.da.SearchCursor(E0A, fieldnames) as cursor:
             for row in cursor:
                  f.write(','.join([str(r) for r in row])+'\n')

   ###Add new points to map
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
addLayer = arcpy.mapping.Layer(outPointsF)
arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")

#output csv
CSVFile = outFolder + "/" + outName+ "_rarefied_points.csv" 
fieldnames = [f.name for f in arcpy.ListFields(outPointsF) if f.type <> 'Geometry']
for i,f in enumerate(fieldnames):
    if f == 'Shape' or f == 'FID' or f == 'OBJECTID':
        del fieldnames[i]
with open(CSVFile, 'w') as f:
    f.write(','.join(fieldnames)+'\n') #csv headers
    with arcpy.da.SearchCursor(outPointsF, fieldnames) as cursor:
        for row in cursor:
            f.write(','.join([str(r) for r in row])+'\n')


import datetime
#create table of inputs into SDMtoolbox
#change outFolder if needed, out file if needed, and inputs names
#NOTE: If script contains a "glob" n- write the first occured of the glob as: + str(inFolder+"/*.asc")+ "\n" + 
newLine = ""
file = open(outFolder+"/"+outName+".SDMtoolboxInputs", "w")
file.write(newLine)
file.close()
addlineH=str(datetime.datetime.now())+ "\n" + "Input Parameters \n" + "Input Folder: " + str(infile) + "\n" + "Species Field:" +str(speciesField)+ " \n" + "Long: "+ str(longitudField)+ " \n" + "Lat: "+ str(latitudeField)+ "Output Folder: " + str(outFolder) + "\n" + "Output Name" +str(outName)+ " \n" + "resolution: "+ str(resolution)+ " \n" + "Projection: "+ str(inProject)+ "Boolean: " + str(inputBoolean) + "\n" + "inHetero" +str(inHetero)+ " \n" + "Classes: "+ str(nClasses)+ " \n" + "Class Types: "+ str(ClassType)+ " \n" + "Max Distance: "+ str(maxDist)+ " \n" + "Min Distance: "+ str(minDist)
filedataZ=""
###special for 'GRID' function
#Rasters=gp.listrasters("", "ALL")
#raster= Rasters.next
#while raster:
#    print raster
#    newLineR =str(raster)+ ", "+filedataZ
#    filedataZ=newLineR
#    raster = Rasters.next()
#END of special for 'GRID' function
file = open(outFolder+"/"+outName+".SDMtoolboxInputs", "r")
filedata = file.read()
file.close()
#DELETE +"\nRasters input: "
newLine =addlineH+"\nRasters input: "+filedataZ+filedata
file = open(outFolder+"/"+outName+".SDMtoolboxInputs", "w")
file.write(newLine)
file.close()
gp.AddMessage("*******************************************")
gp.AddMessage("Table of inputs were output: "+outFolder+"/"+outName+".SDMtoolboxInputs")
#####step1_change_output_name_appropriately. For example: outFolder+"/ExtractByMask.SDMtoolboxInputs". If fixed name leave within ""; if calling user input: "/"+outName+".SDMtoolboxInputs" (CHANGING gridName to name input)
###change 'outFolder' to match outfolder sytax in focal script 
####step3_change inputs to match script Line:9 (from top of python script
###step4 paste at bottom before file deletes

gp.AddMessage("Cleaning up workspace")
if arcpy.Exists(outFolderTemp+"/OutPtsEall.shp"):
   arcpy.Delete_management(outFolderTemp+"/OutPtsEall.shp")
if arcpy.Exists(outFolderTemp+"/empty.shp"):
   arcpy.Delete_management(outFolderTemp+"/empty.shp")
if arcpy.Exists(outFolderTemp2+"/1.shp"):
   arcpy.Delete_management(outFolderTemp2+"/1.shp")
if arcpy.Exists(outFolderTemp2+"/2.shp"):
   arcpy.Delete_management(outFolderTemp2+"/2.shp")
if arcpy.Exists(outFolderTemp2+"/3.shp"):
   arcpy.Delete_management(outFolderTemp2+"/3.shp")
if arcpy.Exists(outFolderTemp2+"/4.shp"):
   arcpy.Delete_management(outFolderTemp2+"/4.shp")
if arcpy.Exists(outFolderTemp2+"/5.shp"):
   arcpy.Delete_management(outFolderTemp2+"/5.shp")
if arcpy.Exists(outFolderTemp2+"/0.shp"):
   arcpy.Delete_management(outFolderTemp2+"/0.shp")
if arcpy.Exists(outFolderTemp2+"/Merge1.shp"):
   arcpy.Delete_management(outFolderTemp2+"/Merge1.shp")
if arcpy.Exists(outFolderTemp3+"/1.shp"):
   arcpy.Delete_management(outFolderTemp3+"/1.shp")
if arcpy.Exists(outFolderTemp3+"/2.shp"):
   arcpy.Delete_management(outFolderTemp3+"/2.shp")
if arcpy.Exists(outFolderTemp3+"/3.shp"):
   arcpy.Delete_management(outFolderTemp3+"/3.shp")
if arcpy.Exists(outFolderTemp3+"/4.shp"):
   arcpy.Delete_management(outFolderTemp3+"/4.shp")
if arcpy.Exists(outFolderTemp3+"/Merge2.shp"):
   arcpy.Delete_management(outFolderTemp3+"/Merge2.shp")  
if arcpy.Exists(outFolderTemp4+"/Merge3.shp"):
   arcpy.Delete_management(outFolderTemp4+"/Merge3.shp") 
if arcpy.Exists(outFolderTemp4+"/1.shp"):
   arcpy.Delete_management(outFolderTemp4+"/1.shp")   
if arcpy.Exists(outFolderTemp4+"/2.shp"):
   arcpy.Delete_management(outFolderTemp4+"/2.shp")   
if arcpy.Exists(outFolderTemp4+"/3.shp"):
   arcpy.Delete_management(outFolderTemp4+"/3.shp")      
if arcpy.Exists(outPoints2):
   arcpy.Delete_management(outPoints2)    
arcpy.Delete_management(outFolderTemp)
arcpy.Delete_management(outFolderTemp2)
arcpy.Delete_management(outFolderTemp3)
arcpy.Delete_management(outFolderTemp4)
arcpy.Delete_management(outFolderTemp5)
arcpy.Delete_management(outFolderTemp6)
arcpy.Delete_management(outFolderTemp7)
arcpy.Delete_management(outFolderTemp8)
arcpy.Delete_management(outFolderTemp9)
arcpy.Delete_management(outFolderTemp10)

gp.AddMessage("Finished successfully")
#del gp



