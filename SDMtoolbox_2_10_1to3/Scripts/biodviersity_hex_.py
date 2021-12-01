###points
import arcpy, csv, sys, string, os, glob, numpy, arcgisscripting

arcpy.env.overwriteOutput = True
gp = arcgisscripting.create()


def str2bool(pstr):
    """Convert ESRI boolean string to Python boolean type"""
    return pstr == 'true'


scriptPath = sys.path[0]
inFolder = sys.argv[1]
#gridTypeIN=sys.argv[2]
inputBoolean = str2bool(sys.argv[2])
gridName = sys.argv [3]
outFolder = sys.argv[4]
gridType = sys.argv[5]
inHex = sys.argv[6]
inPtsObsShp = sys.argv[7]
inPtsObsField = sys.argv[8]
inPtsObsDist = sys.argv[9]
inPtsObsDistN= float(inPtsObsDist)

if outFolder == inFolder:
    gp.AddMessage("input folder cannot be the same as output folder!")
    del arcpy

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


if gridType == "#":
  gridTypeO = ".tif"
  gridTypeO1="NO"
if gridType == "TIFF (.tif)":
    gridTypeO=".tif"
    gridTypeO1="NO"
if gridType == "ASCII (.asc)":
    gridTypeO=".tif"
    gridTypeO1="YES"
if gridType == "Erdas Imagine (.img)":
    gridTypeO=".img"
    gridTypeO1="NO"



#Create centriod pts (nice for sampling values of coasts)
arcpy.FeatureToPoint_management(inHex,outFolderTemp + "/temp1.shp","INSIDE")

gp.AddMessage("...setting up environment")

#if gridTypeIN=="YES":
if inputBoolean== True:
   #get a list of the grids in directory
   gp.workspace = inFolder
   Grids = gp.listrasters("", "ALL")
   grid = Grids.next()
   while grid:
     try:#get a list of the grids in directory
       arcpy.gp.Slice_sa(grid,outFolderTemp + "/" + "consTemp","1","EQUAL_INTERVAL","0")
       ConstRas1= outFolderTemp + "/" + "consTemp"
       outTempRas1 = ConstRas1
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231F.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231B.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231C.tif","","","","","","#")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231D.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231E.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231G.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231H.tif","","","","","","32_BIT_FLOAT")
       outTempRas1 = outFolderTemp +"/TEMP231F.tif"
       outTempRas2 = outFolderTemp +"/TEMP231B.tif"
       outTempRas3 = outFolderTemp + "/TEMP231D.tif"
       outTempRas4 = outFolderTemp + "/TEMP231E.tif"
       outTempRas5 = outFolderTemp + "/TEMP231G.tif"
       outTempRas6 = outFolderTemp + "/TEMP231G.tif"
       TempShp1 = outFolderTemp + "/temp1.shp"
       TempShp2 = outFolderTemp + "/temp2.shp"
       TempShp3 = outFolderTemp + "/temp3.shp"
       outMASK = outFolderTemp + "/TEMP231C.tif"
       print grid, "spatial environment established"
       gp.AddMessage("spatial environment established")
       grid = ()
     except:
       print grid, "...NOT SUMMED"
       gp.AddMessage(grid + " ...NOT SUMMED- will try another" + gp.GetMessages())
       grid = Grids.next()
#----------BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB----------  
##create a blank grid at resolution and extent of summing
#if gridTypeIN=="NO":
if inputBoolean== False:
   #get a list of the grids in directory
   gp.workspace = inFolder
   Grids = gp.listrasters("", "ALL")
   grid = Grids.next()
   while grid:
     try:#get a list of the grids in directory
       arcpy.gp.Slice_sa(grid,outFolderTemp + "/" + "consTemp","1","EQUAL_INTERVAL","0")
       ConstRas1= outFolderTemp + "/" + "consTemp"
       outTempRas1 = ConstRas1
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231F.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231B.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231C.tif","","","","","","#")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231D.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231E.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231G.tif","","","","","","32_BIT_FLOAT")
       arcpy.CopyRaster_management(outTempRas1,outFolderTemp +"/TEMP231H.tif","","","","","","32_BIT_FLOAT")
       outTempRas1 = outFolderTemp +"/TEMP231F.tif"
       outTempRas2 = outFolderTemp +"/TEMP231B.tif"
       outTempRas3 = outFolderTemp + "/TEMP231D.tif"
       outTempRas4 = outFolderTemp + "/TEMP231E.tif"
       outTempRas5 = outFolderTemp + "/TEMP231G.tif"
       outTempRas6 = outFolderTemp + "/TEMP231G.tif"
       TempShp1 = outFolderTemp + "/temp1.shp"
       TempShp2 = outFolderTemp + "/temp2.shp"
       TempShp3 = outFolderTemp + "/temp3.shp"
       outMASK = outFolderTemp + "/TEMP231C.tif"
       print grid, "spatial environment established"
       gp.AddMessage("spatial environment established")
       grid = ()
     except:
       print ""
       gp.AddMessage("")
       grid = Grids.next()

arcpy.env.extent = outMASK
arcpy.env.cellSize = outMASK
   


#######CONVERT POINTS TO BUFFER THEN INSERT INTO ALL OTHER ANALYSIS

if inPtsObsShp != "#":
    from Scripts import Biodiversity_raster2_sl_nm
    gp.AddMessage("separating points to separate files")
if inPtsObsShp != "#":
    theFilesAA = glob.glob(outFolderTemp6+"/*.shp")
    for i in theFilesAA:
      inSHP = str(i).replace("\\","/")
      outName = os.path.split(inSHP)[1] 
      outSHP = (outFolderTemp7 + "/" + str(outName)[:-4]+ ".shp").replace("\\","/")
      gp.AddMessage("Converting: " + inSHP)
      try: 
        arcpy.Buffer_analysis(inSHP,outSHP,inPtsObsDistN,"FULL","ROUND","ALL","#")
      except: 
        gp.AddMessage(gp.GetMessages())
##Convert ShapeFile to raster
if inPtsObsShp != "#":		
    theFilesBB = glob.glob(outFolderTemp7+"/*.shp")
    for i in theFilesBB:
      inSHP = str(i).replace("\\","/")
      outName = os.path.split(inSHP)[1] 
      outTIF = (outFolderTemp7 + "/" + str(outName)[:-4]+ ".TIF").replace("\\","/")
      gp.AddMessage("Converting: " + inSHP)
      try: 
        arcpy.PolygonToRaster_conversion(inSHP,"FID",outTIF,"CELL_CENTER","NONE","#")
      except: 
        gp.AddMessage(gp.GetMessages())
##Convert NoData Values to 0 pre-summation
if inPtsObsShp != "#":
    theFilesCC = glob.glob(outFolderTemp7+"/*.TIF")
    for i in theFilesCC:
      inTIF = str(i).replace("\\","/")
      outName = os.path.split(inTIF)[1] 
      outTIF = (outFolderTemp8 + "/" + str(outName)[:-4]+ ".TIF").replace("\\","/")
      gp.AddMessage("Changing NoData to Zero: " + inTIF)
      try: 
        arcpy.gp.Reclassify_sa(inTIF,"Value","0 1;NODATA 0",outTIF,"DATA") 
      except: 
        gp.AddMessage(gp.GetMessages())
###
if inPtsObsShp != "#":
    theFilesCC = glob.glob(outFolderTemp8+"/*.TIF")
    for i in theFilesCC:
      inTIF = str(i).replace("\\","/")
      outName = os.path.split(inTIF)[1] 
      outTIF = (outFolderTemp9  + "/" + str(outName)[:-4] + ".TIF").replace("\\","/")   
      outTIF2 = (outFolderTemp3  + "/" + str(outName)[:-4] + ".TIF").replace("\\","/")
      gp.AddMessage("Clipping: " + inTIF)
      gp.AddMessage("Producing: " + outTIF)
      try: 
         gp.CopyRaster_management(outFolderTemp + "/" + "consTemp",outFolderTemp + "/" + "consTemp2","#","#","#","NONE","NONE","#")
         gp.CopyRaster_management(outFolderTemp + "/" + "consTemp",outFolderTemp + "/" + "consTemp3","#","#","#","NONE","NONE","#")
         ConstRas2= (outFolderTemp + "/" + "consTemp2").replace("\\","/")
         arcpy.Mosaic_management(inTIF,ConstRas2,"MAXIMUM","FIRST","#","#","NONE","0","NONE")
         gp.CopyRaster_management(ConstRas2,outTIF,"#","#","#","NONE","NONE","#")
         arcpy.gp.Plus_sa(outTIF,outFolderTemp + "/" + "consTemp3",outTIF2)
      except: 
         gp.AddMessage(gp.GetMessages())

###******************************************************
##Convert NoData Values to 0 pre-summation
###ConvertPointsToRaster
gp.workspace = inFolder
arcpy.workspace = inFolder
theFilesA1 = arcpy.ListRasters("", "ALL")
for i in theFilesA1:
   inTIF = str(i).replace("\\","/")
   outName = os.path.split(inTIF)[1] 
   outTIF = (outFolderTemp2 + "/" + str(outName)[:-4]+ ".TIF").replace("\\","/")
   gp.AddMessage("Converting raster to float: " + outName)
   try: 
       arcpy.gp.Reclassify_sa(inTIF,"Value","1 1;NODATA 0",outTIF,"DATA")
   except: 
       gp.AddMessage(gp.GetMessages())

###******************************************************
##Convert NoData Values to 0 pre-summation
###ConvertPointsToRaster
theFilesA = glob.glob(outFolderTemp2+"/*TIF")
for i in theFilesA:
  inTIF = str(i).replace("\\","/")
  outName = os.path.split(inTIF)[1] 
  outTIF = (outFolderTemp3 + "/" + str(outName)[:-4]+ ".TIF").replace("\\","/")
  gp.AddMessage("Changing NoData to Zero: " + outName)
  try: 
    arcpy.gp.Float_sa(inTIF,outTIF)
  except: 
    gp.AddMessage(gp.GetMessages())

##*******************************************************
###CREATE WE and RICH RASTERS FOR HEX
theFilesC = glob.glob(outFolderTemp3 + "/*.TIF")
for i in theFilesC:
  inTIF = str(i).replace("\\","/")
  outName = os.path.split(inTIF)[1] 
  outTIF = (outFolderTemp4 + "/" + str(outName)[:-4]+ "_DIV.TIF").replace("\\","/")
  WErasOUT = (outFolderTemp5 + "/" + str(outName)[:-4]+ "_WE.TIF").replace("\\","/")
  PARAMS='"""RASTERVALU "RASTERVALU" true true false 8 Double 0 0 ,First,#,'+TempShp2+',RASTERVALU,-1,-1"""'
  gp.AddMessage("Generating weighted layers: " + outName)
  
  try: 
    TempShp2 = outFolderTemp + "/temp2.shp"
    arcpy.gp.ZonalStatistics_sa(inHex,"FID",inTIF,outTIF,"MAXIMUM","DATA")
    arcpy.gp.ExtractValuesToPoints_sa(TempShp1,outTIF,TempShp2,"NONE","VALUE_ONLY")
    naZ = arcpy.da.TableToNumPyArray(TempShp2,"RASTERVALU")
    val2= numpy.count_nonzero(naZ["RASTERVALU"])
    arcpy.gp.Divide_sa(outTIF,val2,WErasOUT)
    arcpy.Delete_management(TempShp2)
  except: 
    gp.AddMessage(gp.GetMessages())

###Summing all WE rasters to create WE 
theFilesE = glob.glob(outFolderTemp5+"/*.TIF")
for i in theFilesE:
  inTIF = str(i).replace("\\","/")
  outName = os.path.split(inTIF)[1] 
  gp.AddMessage("Calculating weighted endemism: processing " + outName)
  try: 
    arcpy.gp.Plus_sa(inTIF,outTempRas1,outTempRas2)
    arcpy.CopyRaster_management(outTempRas2,outTempRas1,"","","","","","")
  except: 
    gp.AddMessage(gp.GetMessages())

###Summing of all occur rasters to create richness 
theFilesZ = glob.glob(outFolderTemp4+"/*.TIF")
for i in theFilesZ:
  inTIF = str(i).replace("\\","/")
  outName = os.path.split(inTIF)[1] 
  gp.AddMessage("Calculating richness: processing " + outName)
  try: 
    arcpy.gp.Plus_sa(inTIF,outTempRas3,outTempRas4)
    arcpy.CopyRaster_management(outTempRas4,outTempRas3,"","","","","","")
  except: 
    gp.AddMessage(gp.GetMessages())

#Save final WE GRID
if gridTypeO1=="YES":
     arcpy.Mosaic_management(outTempRas2,outTempRas5,"LAST","#","#","#","NONE","0","NONE")
     arcpy.RasterToASCII_conversion(outTempRas5,outFolder + "/" + gridName + "_WE.asc")
if gridTypeO1=="NO":
     arcpy.Mosaic_management(outTempRas2,outTempRas5,"LAST","#","#","#","NONE","0","NONE")
     arcpy.CopyRaster_management(outTempRas5,outFolder + "/" + gridName + "_WE"+ gridTypeO,"","","","","","")

#Save final Richness GRID
if gridTypeO1=="YES":
     arcpy.RasterToASCII_conversion(outTempRas3,outFolder + "/" + gridName + "_Spp_Rich.asc")
if gridTypeO1=="NO":
     arcpy.CopyRaster_management(outTempRas3,outFolder + "/" + gridName + "_Spp_Rich"+ gridTypeO,"","","","","","")

#ID final layers
InFinRich= outFolder + "/" + gridName + "_Spp_Rich"+ gridTypeO
InFinWE=outFolder + "/" + gridName + "_WE"+ gridTypeO
InFinCWE=outFolderTemp + "/" + gridName + "_CWE_M"+ gridTypeO

###Create CWE layer
arcpy.gp.Divide_sa(InFinWE,InFinRich,InFinCWE)
arcpy.Mosaic_management(InFinCWE,outTempRas6,"LAST","#","#","#","NONE","0","NONE")
arcpy.CopyRaster_management(outTempRas6,outFolder + "/" + gridName + "_CWE"+ gridTypeO,"","","","","","")
if gridTypeO1=="YES":
     arcpy.RasterToASCII_conversion(InFinCWE,outFolder + "/" + gridName + "_CWE.asc")


#extract Rich, CWE, and We to points
arcpy.Copy_management(TempShp1,outFolderTemp + "/outMASK2_CP_PTS.shp","ShapeFile")
arcpy.Copy_management(TempShp1,outFolderTemp + "/outMASK2_CP_PTS2.shp","ShapeFile")
arcpy.Copy_management(TempShp1,outFolderTemp + "/outMASK2_CP_PTS3.shp","ShapeFile")
arcpy.Copy_management(TempShp1,outFolderTemp + "/outMASK2_CP_PTS4.shp","ShapeFile")
arcpy.Copy_management(inHex,outFolderTemp + "/outMASK2_CP.shp","ShapeFile")
FFmask=outFolderTemp + "/outMASK2_CP_PTS.shp"
FFmask2=outFolderTemp + "/outMASK2_CP_PTS2.shp"
FFmask3=outFolderTemp + "/outMASK2_CP_PTS3.shp"
FFmask4=outFolderTemp + "/outMASK2_CP_PTS4.shp"
FFmaskShp=outFolderTemp + "/outMASK2_CP.shp"
  
arcpy.gp.ExtractValuesToPoints_sa(FFmask,InFinRich,FFmask2,"NONE","VALUE_ONLY")
arcpy.AddField_management(FFmask2, "Richness", "DOUBLE", "#","","","","")
arcpy.CalculateField_management(FFmask2, "Richness", "[RASTERVALU]", "VB","#")
arcpy.DeleteField_management(FFmask2,["RASTERVALU","Id","ORIG_FID"])
arcpy.gp.ExtractValuesToPoints_sa(FFmask2,InFinWE,FFmask3,"NONE","VALUE_ONLY")
arcpy.AddField_management(FFmask3, "WE", "DOUBLE", "#","","","","")
arcpy.CalculateField_management(FFmask3, "WE", "[RASTERVALU]", "VB","#")
arcpy.DeleteField_management(FFmask3,["RASTERVALU","Id","ORIG_FID"])
arcpy.gp.ExtractValuesToPoints_sa(FFmask3,InFinCWE,FFmask4,"NONE","VALUE_ONLY")
arcpy.AddField_management(FFmask4, "CWE", "DOUBLE", "#","","","","")
arcpy.CalculateField_management(FFmask4, "CWE", "[RASTERVALU]", "VB","#")
arcpy.DeleteField_management(FFmask4,["RASTERVALU","Id","ORIG_FID"])


#join points with clipped grid
outLast16=outFolder+"/"+gridName+".shp"
arcpy.SpatialJoin_analysis(FFmaskShp,FFmask4,outLast16,"JOIN_ONE_TO_MANY","KEEP_ALL","","INTERSECT","","")
arcpy.DeleteField_management(outLast16,["TARGET_FID","JOIN_FID","Id","Join_Count","Input_FID","OBJECTID_1","Input_FI_1","Shape_le_1","Shape_Ar_1",])
rows = arcpy.UpdateCursor(outLast16) 


desc = arcpy.Describe(outLast16)
fields = desc.fields
rows = arcpy.UpdateCursor(outLast16)

for row in rows:
    if row.Richness == "-9999":
        row.Richness = "0"
    else:
        row.Richness = row.Richness
    rows.updateRow(row)

del rows
	
# Delete cursor and row objects to remove locks on the data 
# 
del row 
del rows  

rows = arcpy.UpdateCursor(outLast16) 
for row in rows:
    # Fields from the table can be dynamically accessed from the row object.
    #   Here, the field is named targetField as I don't know your field name
    targetRow = row.WE #Assigns value of targetField to string
    row.WE = targetRow.replace('0', '-9999') #Removes the dashes
    rows.updateRow(row) 

# Delete cursor and row objects to remove locks on the data 
# 
del row 
del rows  

rows = arcpy.UpdateCursor(outLast16) 
for row in rows:
    # Fields from the table can be dynamically accessed from the row object.
    #   Here, the field is named targetField as I don't know your field name
    targetRow = row.CWE #Assigns value of targetField to string
    row.CWE = targetRow.replace('0', '-9999') #Removes the dashes
    rows.updateRow(row) 

# Delete cursor and row objects to remove locks on the data 
# 
del row 
del rows  

###Adds new files to open map
gp.AddMessage("Adding results to ArcMap")
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

if gridTypeO1=="YES":
      addLayer4 = arcpy.mapping.Layer(outFolder + "/" + gridName + ".shp")
      arcpy.mapping.AddLayer(df, addLayer4, "AUTO_ARRANGE")

if gridTypeO1=="NO":  
      addLayer4 = arcpy.mapping.Layer(outFolder + "/" + gridName + ".shp")
      arcpy.mapping.AddLayer(df, addLayer4, "AUTO_ARRANGE")



gp.AddMessage("Cleaning up workspace")
arcpy.Delete_management(outFolderTemp + "/outMASK2_CP_PTS2.shp")
arcpy.Delete_management(outFolderTemp + "/outMASK2_CP_PTS3.shp")
arcpy.Delete_management(outFolderTemp + "/outMASK2_CP_PTS4.shp")
#arcpy.Delete_management(OutShape1)
#arcpy.Delete_management(OutShape2)
arcpy.Delete_management(outFolderTemp)
arcpy.Delete_management(outFolderTemp2)
arcpy.Delete_management(outFolderTemp3)
arcpy.Delete_management(outFolderTemp4)
arcpy.Delete_management(outFolderTemp5)
gp.AddMessage("Finished successfully")
#del gp

