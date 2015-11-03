# NationalCropRevisionFacilitation

The main program is called CropRevision.py

This program is built to help AAFC EO (Earth Observation) group for the National Crop Map generation project. 

Each province has a original classification .pix file and a modified classification .pix file. The program will compare both file and export all the raster differences to an existing shapefile.(will eventually contains all the changes apply across the country). For example, if I decided to change a field identified as [corn] in [original.pix], to [Water] in [modified.pix],then a water polygon should be created in the shapefile. After that, the change will be applied to the other provincial file using the national.shp file.

In order to run the program, the arcpy module is required 
