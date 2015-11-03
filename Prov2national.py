#************************************************************************
# This function will find the overlap area of two polygons and export 
# to a shapefile, add the overlaped area to the existing national.shp
# Created date:  2015-05-25
# Created by: JiaQi Guo(Max) 
# Last Modified date: 
# Modified by:
#*************************************************************************



import subprocess
import os
import arcpy


newProvince = "NB"
strEASI_Script = "findOverlap"
strFolder = "E:\\IMPORTANT\\overlapping_conversion"

print ("Creating a easi script that will generate the overlap areas")

# Open easi script from the working directory 

f_EASI = open(os.path.join(strFolder, strEASI_Script + ".eas"), "w")

#----- Create prm.prm -----

f_EASI.write("RUN COPPRM\n\n")

#---------Declare variables------

f_EASI.write("!----- Declare variables -----\n")
f_EASI.write("local string strFolder, strPIXO, strPIXM\n") 
f_EASI.write("local integer intClassif_O, intClassif_M, newChannelM, f_PIXM, f_PIXO\n") 
f_EASI.write("intClassif_O = 3\n")
f_EASI.write("intClassif_M = 3\n")
f_EASI.write("strPIXO = \"O.pix\"\n")
f_EASI.write("strPIXM = \"M.pix\"\n")
f_EASI.write("strFolder = \"E:\\IMPORTANT\\overlapping_conversion\"\n")

#----------PCI mod---------------
f_EASI.write("!----------PCI mod---------------\n")
f_EASI.write("FILE = strFolder + \"\\\\\" + strPIXM\n") 
f_EASI.write("PCIOP = \"ADD\"\n")
f_EASI.write("PCIVAL = 1\n")
f_EASI.write("RUN PCIMOD\n")
f_EASI.write("f_PIXM = DBOpen(strFolder + \"\\\\\" + strPIXM, \"w\" )\n")
f_EASI.write("f_PIXO = DBOpen(strFolder + \"\\\\\" + strPIXO, \"r\" )\n")
f_EASI.write("newChannelM = DBChannels(f_PIXM)\n")

#--------------create a new raster channel only contains the overlapped areas-----------------
f_EASI.write("!----------create a new raster channel only contains the overlapped areas--------------\n")
f_EASI.write("if %{f_PIXM ,intClassif_M } <> %{f_PIXO, intClassif_O}  then\n")
f_EASI.write("	%{ f_PIXM, newChannelM } = %{f_PIXM ,intClassif_M}\n")
f_EASI.write("endif\n")
f_EASI.write("Call DBClose(f_PIXM)\n")
f_EASI.write("Call DBClose(f_PIXO)\n")

#------------------ Export a shapefile --------------
f_EASI.write("!----------Export a shapefile --------------\n")
f_EASI.write("FILI	=	strFolder + \"\\\\\" + strPIXM\n")
f_EASI.write("FILO    =	strFolder + \"\\\\\" + \"overlap.tif\"\n")
f_EASI.write("DBIW	=  \n")
f_EASI.write("DBIC	= newChannelM \n") 
f_EASI.write("DBIB	= \n")
f_EASI.write("DBVS	= \n")
f_EASI.write("DBLUT	= \n")
f_EASI.write("DBPCT	= \n")
f_EASI.write("FTYPE	=	\"TIF\"\n")
f_EASI.write("FOPTIONS	=	\n")
f_EASI.write("RUN FEXPORT \n")


#--------------delete the overlap channel-------------------
f_EASI.write("!----------delete the old ones--------------\n")
f_EASI.write("FILE = strFolder + \"\\\\\" + strPIXM\n")
f_EASI.write("PCIOP = \"DEL\" \n")
f_EASI.write("PCIVAL = newChannelM\n")
f_EASI.write("RUN PCIMOD\n")


f_EASI.close()

print ("EASI script has successfully created..")
print (".")
print (".")
print ("Creating .tiff raster file from EASI script...")
os.chdir(os.path.join(strFolder))
subprocess.call("EASI run " + strEASI_Script)
print (".tiff file that contains the overlap areas has successfully created..")

print (".")
print (".")
print ("Converting raster to polygon through arcpy tool...")

#--------------- create the .shp file from the raster .tiff -----------

from arcpy import env

# Set environment settings
env.workspace = strFolder

# Set local variables
inRaster = "overlap.tif"
outPolygons = strFolder + "/" + newProvince + ".shp"
field = "VALUE"

# Execute RasterToPolygon
arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)


print ("mergeing the new provincial file to the national shapefile")

#--------------------add province identifer-------

from arcpy import env
# Set environment settings
env.workspace = strFolder
# Set local variables
inFeatures = newProvince +".shp"
fieldName = "Province"
fieldAlias = "ProID"
fieldPrecision = 10

 
# Execute AddField twice for two new fields
arcpy.AddField_management(inFeatures, fieldName, "TEXT", fieldPrecision, "", "",
                          fieldAlias, "NULLABLE")




# Create update cursor for feature class 
# 
rows = arcpy.UpdateCursor(strFolder + "/" +newProvince + ".shp") 

for row in rows:
    
    row.Province = newProvince
    rows.updateRow(row) 

# Delete cursor and row objects to remove locks on the data 
# 
del row 
del rows

#-----------------------Delete class with 0 values ---------------


from arcpy import env
env.workspace = strFolder
layerName = newProvince +".shp"
fieldname = "GRIDCODE"
expression = "\"GRIDCODE\" = 0"  
   
with arcpy.da.UpdateCursor(layerName, fieldname, expression) as rows:
  for row in rows:
    rows.deleteRow()



#----------------------Delete the LandClass----------
from arcpy import env
env.workspace = strFolder
infile = "national.shp"
arcpy.DeleteField_management(infile, "LandClass")

#--------------- merge the polygons together ---------------- 

# feature classes to be merged
oldPoly = "national.shp"
newPoly = newProvince +".shp"

# Create FieldMappings object to manage merge output fields
fieldMappings = arcpy.FieldMappings()

# Add all fields from both oldpolygon and polygon
fieldMappings.addTable(oldPoly)
fieldMappings.addTable(newPoly)

# Add input fields "GRIDCODE" into new output field
fldMap_lclass = arcpy.FieldMap()
fldMap_lclass.addInputField(oldPoly,"GRIDCODE")
fldMap_lclass.addInputField(newPoly,"GRIDCODE")
# Set name of new output field "Land_Class"
lclass = fldMap_lclass.outputField
lclass.name = "LandClass"
fldMap_lclass.outputField = lclass
# Add output field to field mappings object
fieldMappings.addFieldMap(fldMap_lclass)


uptodatePoly = strFolder + "/new_national"
arcpy.Merge_management([oldPoly, newPoly], uptodatePoly,fieldMappings)


print ("The new national file is now created")



#--------------- Delete the intermediate .shp files ----------------
print (".")
print ("Delete the intermediate steps")
#Set local variables
out_data1 = newProvince + ".shp"
out_data2 = "national.shp"
out_data3 = "overlap.tif"
out_data4 = "findOverlap.eas"
data_type = ""
arcpy.Delete_management(out_data1, data_type)
arcpy.Delete_management(out_data2, data_type)
arcpy.Delete_management(out_data3, data_type)
arcpy.Delete_management(out_data4, data_type)

#--------------- Rename ----------------
print (".")
print ("Rename the new file to national.shp")
#Set local variables
in_data =  "new_national.shp"
out_data = "national.shp"
data_type = ""

#Execute Rename
arcpy.Rename_management(in_data, out_data, data_type)










