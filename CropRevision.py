#********************************************************************************************
# This function finished version of the final crop inventory revision facilitation
# Created date:  2015-05-25
# Created by: JiaQi Guo(Max) 
# Last Modified date: 2015-06-16
# Modified by: JiaQi Guo(Max)
# Modification areas: Adding user instructions (line 51 ~ line 90) 
# Future Possible Utilization: using overwrite instead delete intermediate steps.
# Potential Use: This  program is built in a Class called App, can be import to other programs
#*********************************************************************************************


from Tkinter import *
import tkSimpleDialog
import tkFileDialog
import tkMessageBox
import subprocess
import os
import arcpy

class App:
    
    newProvince=""


# Set up the Parent GUI

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
        self.quit = Button(frame, text="QUIT", fg="red", font=("Arial", 12,"bold"),command=frame.quit)
        self.merge_P = Button(frame, text="Province to National",font=("Arial", 12,"bold"), command=self.mergeP)   
        self.new_N = Button(frame, text="Update Province", font=("Arial", 12,"bold"),command=self.updateN)
        self.new_P = Button(frame, text="Update modified provincial pix file",font=("Arial", 12,"bold"), command=self.updateP)
        self.tip = Button(frame, text="**Program Info**", fg="blue",font=("Arial", 12,"bold"), command=self.tips)

        t1 = Label(frame, text = "Adding province to the national.shp",fg ="dark green", font= ("Helvetica 10 bold italic"))
        t2 = Label(frame, text = "Updating the existing province in national.shp",fg ="dark green",font= ("Helvetica 10 bold italic"))
        t3 = Label(frame, text = "Updating provincial pix file using national.shp",fg ="dark green",font= ("Helvetica 10 bold italic"))

        t1.grid(row=2, column=2, padx=2, pady=5, sticky="W")
        t2.grid(row=3, column=2, padx=2, pady=5, sticky="W")
        t3.grid(row=4, column=2, padx=2, pady=5, sticky="W")


        self.merge_P.grid(row=2, column=1, padx=5, pady=5, sticky="W")
        self.new_N.grid(row=3, column=1, padx=5, pady=5, sticky="W")
        self.new_P.grid(row=4, column=1, padx=5, pady=5, sticky="W")
        self.quit.grid(row=8, column=3, sticky="W")
        self.tip.grid(row=8, column=1, sticky="W")
        
# Writting the Program info to help user understand the program

    def tips(self):
        
        newW = Toplevel(root)
        newW.title("Program Info")
        newW.resizable(0,0)
        w1 = Label(newW, text = "Content",
                    font=("Arial", 11, "bold"))
        w1.pack()
        
        w2 = Message(newW,
                    text = " One of the last step to be done before releasing the provincial crop inventory maps every year, is to visually inspect every provincial map and manually make correction if needed.Because there is an overlap between some provincial files, "
                     "modifications done on one file should also be applied on the overlapping one.This program  will automatically applied the correction on other overlapping file(s).",
                    borderwidth = 10,
                    font=("Arial", 11),
                    anchor = "w")
        w2.pack()
        
        w3 = Label(newW,text = "Approach",
                    font=("Arial", 11, "bold"))
        w3.pack()

        w4 = Message(newW,
                    text = "Each province has a original classification .pix file and a modified classification .pix file. The program will compare both files,"
                     "and export all the raster differences to an existing shapefile.(will eventually contains all the changes apply across the country). For example, if I decided to change a field identified as [corn] in [original.pix], to [Water] in [modified.pix],"
                     "then a water polygon should be created in the shapefile. After that, the change will be applied to the other provincial file using the national.shp file.",
                    borderwidth = 12,
                    font=("Arial", 11),
                    anchor = "w")
        w4.pack()

        w5 = Label (newW, text = "                                                  2015-06-16. AAFC",fg="red",font=("Arial", 11, "bold"))

        w5.pack()


                                
                                
        
   

    def mergeP(self):


# Setting up the Sub-GUI for "Province to National"

        newW = Toplevel(root)
        newW.title("Province to National")
        newW.resizable(0,0)

        file_label = Label(newW, text="Input Original pix File:",font=("Arial", 11))
        OFile = Entry(newW, width=50)
        file_browse_button = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,OFile, "Select a pix file", "openOfile", filetypes=[("Raster File","*.pix")]))

        file_label2 = Label(newW, text="Input Original pix File Classification Channel#:",font=("Arial", 11))
        ONum = Entry(newW, width=10)
        
                                 
        file_label3 = Label(newW, text="Input Modified pix File:",font=("Arial", 11))
        MFile = Entry(newW, width=50)
        file_browse_button3 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,MFile, "Select a pix file", "openMfile", filetypes=[("Raster File","*.pix")]))
        
        file_label4 = Label(newW, text="Input Modified pix File Classification Channel#:",font=("Arial", 11))
        MNum = Entry(newW, width=10)
        

        file_label5 = Label(newW, text="Set up the working directory:",font=("Arial", 11))
        strFolder = Entry(newW, width=50)
        file_browse_button5 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,strFolder, "Select a pix file", "setfolder"))

        file_label6 = Label(newW, text="Enter the province name(in abbreviation):",font=("Arial", 11))
        newProvince = Entry(newW, width=10)
        
        run_button = Button(newW, text="RUN",fg="red",font=("Arial", 11, "bold"),command=lambda: run( OFile.get(),
                                                                   ONum.get(),
                                                                   MFile.get(),
                                                                   MNum.get(),
                                                                   strFolder.get(),
                                                                   newProvince.get()))



        file_label.grid(row=2, column=1, padx=5, pady=5, sticky="E")
        OFile.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button.grid(row=2, column=5, padx=5, pady=5)
        
        file_label2.grid(row=3, column=1, padx=5, pady=5, sticky="E")
        ONum.grid(row=3, column=2, columnspan=3, padx=5, pady=5,sticky ="W")
       
        
        file_label3.grid(row=4, column=1, padx=5, pady=5, sticky="E")
        MFile.grid(row=4, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button3.grid(row=4, column=5, padx=5, pady=5)
        
        file_label4.grid(row=5, column=1, padx=5, pady=5, sticky="E")
        MNum.grid(row=5, column=2, columnspan=3, padx=5, pady=5,sticky="W")
        

        file_label5.grid(row=6, column=1, padx=5, pady=5, sticky="E")
        strFolder.grid(row=6, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button5.grid(row=6, column=5, padx=5, pady=5)

        file_label6.grid(row=7, column=1, padx=5, pady=5, sticky="E")
        newProvince.grid(row=7, column=2, columnspan=3, padx=5, pady=5,sticky="W")

        run_button.grid(row=8,column=5, padx=5, pady=5, sticky="E")



        def browse(newW,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):
    
            if(type=="openOfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Original provincial pix file:",filetypes=filetypes)
            elif(type=="openMfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Modified Provincial pix file:",filetypes=filetypes)
            elif(type=="setfolder"):
                case = tkFileDialog.askdirectory(parent=newW,title= "Set up your working Folder:",mustexist=mustexist)
            else:
                raise ValueError(type + " is not a valid browse dialog type.")
                return

            if(len(case)>0):
                dir = os.path.dirname(case)
                textbox.delete(0, END)
                textbox.insert(0, case)
            

        # Merging Provincial file to National file

        def run(OFile,ONum,MFile,MNum,strFolder,newProvince) :

            strEASI_Script = "findOverlap"
            

            print ("Creating a easi script that will generate the overlap areas")

            # Open easi script from the working directory 

            f_EASI = open(os.path.join(strFolder, strEASI_Script + ".eas"), "w")

            #----- Create prm.prm -----

            f_EASI.write("RUN COPPRM\n\n")

            #---------Declare variables------

            f_EASI.write("!----- Declare variables -----\n")
            f_EASI.write("local string strFolder, strPIXO, strPIXM\n") 
            f_EASI.write("local integer intClassif_O, intClassif_M, newChannelM, f_PIXM, f_PIXO\n") 
            f_EASI.write("intClassif_O = "+str(ONum)+"\n")
            f_EASI.write("intClassif_M = "+str(MNum)+"\n")
            f_EASI.write("strPIXO = \""+OFile+"\"\n")
            f_EASI.write("strPIXM = \""+MFile+"\"\n")
            f_EASI.write("strFolder = \""+strFolder+"\"\n")

            #----------PCI mod---------------
            f_EASI.write("!----------PCI mod---------------\n")
            f_EASI.write("FILE = \""+MFile+"\"\n") 
            f_EASI.write("PCIOP = \"ADD\"\n")
            f_EASI.write("PCIVAL = 1\n")
            f_EASI.write("RUN PCIMOD\n")
            f_EASI.write("f_PIXM = DBOpen(\""+MFile+"\", \"w\" )\n")
            f_EASI.write("f_PIXO = DBOpen(\""+OFile+"\", \"r\" )\n")
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
            f_EASI.write("FILI	=	\""+MFile+"\"\n")
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
            f_EASI.write("FILE = \""+MFile+"\"\n")
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


            # Test if national.shp file exist, if exist merge the new province in it, if not create a new national.shp
            
            filename = "national.shp"
            if os.path.exists(filename):

                print ("")
                print ("national.shp exists")
                print ("Merge a new Province to the National.shp file")
            
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

                #-------------------Delete the duplicate areas --------------
                
                from arcpy import env
                env.workspace = strFolder
                eraseinput = "national.shp"
                erasefeature = newProvince +".shp"
                eraseOutput = strFolder + "/" + "national2.shp"
                arcpy.Erase_analysis(eraseinput, erasefeature, eraseOutput)


                #--------------- merge the polygons together ---------------- 

                # feature classes to be merged
                oldPoly = "national2.shp"
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
                out_data5 = "overlap.tif.pox"
                out_data6 = "national2.shp"
                data_type = ""
                arcpy.Delete_management(out_data1, data_type)
                arcpy.Delete_management(out_data2, data_type)
                arcpy.Delete_management(out_data3, data_type)
                arcpy.Delete_management(out_data4, data_type)
                arcpy.Delete_management(out_data5, data_type)
                arcpy.Delete_management(out_data6, data_type)

                #--------------- Rename ----------------
                print (".")
                print ("Rename the new file to national.shp")
                #Set local variables
                in_data =  "new_national.shp"
                out_data = "national.shp"
                data_type = ""

                #Execute Rename
                arcpy.Rename_management(in_data, out_data, data_type)
                print ("The process is done!")
                print ("The province " + newProvince +" has been added to the national.shp file!")
                print ("")
                print ("-----------------------------------------------")
                
            else:
                 #--------------- create the .shp file from the raster .tiff -----------

                print("")
                print("national.shp does not exist...")
                print("Create a new national.shp file...")
                from arcpy import env

                # Set environment settings
                env.workspace = strFolder

                # Set local variables
                inRaster = "overlap.tif"
                outPolygons = strFolder + "/national.shp"
                field = "VALUE"

                # Execute RasterToPolygon
                arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)



                #--------------------add province identifer-------

                from arcpy import env
                # Set environment settings
                env.workspace = strFolder
                 
                # Set local variables
                inFeatures = "national.shp"
                fieldName = "Province"
                fieldAlias = "ProID"
                fieldPrecision = 10


                arcpy.AddField_management(inFeatures, fieldName, "TEXT", fieldPrecision, "", "",
                                          fieldAlias, "NULLABLE")

                rows = arcpy.UpdateCursor(strFolder + "/national.shp") 

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
                layerName = "national.shp"
                fieldname = "GRIDCODE"
                expression = "\"GRIDCODE\" = 0"  
                   
                with arcpy.da.UpdateCursor(layerName, fieldname, expression) as rows:
                  for row in rows:
                    rows.deleteRow()

                #--------------- Delete the intermediate .shp files ----------------
                print (".")
                print ("Delete the intermediate steps")
                #Set local variables
                out_data1 = "overlap.tif"
                out_data2 = "findOverlap.eas"
                out_data3 = "overlap.tif.pox"
                data_type = ""
                arcpy.Delete_management(out_data1, data_type)
                arcpy.Delete_management(out_data2, data_type)
                arcpy.Delete_management(out_data3, data_type)
                print ("The process is done")
                print ("You have created a new national.shp file!")
                print("")
                print("--------------------------------------------------------------------------")

                
                

    def updateN(self):

        # Setting up the Sub-GUI for Update Province.

        newW = Toplevel(root)
        newW.title("Province to existing province from the National.shp")
        newW.resizable(0,0)

        file_label = Label(newW, text="Input Original pix File:",font=("Arial", 11))
        OFile = Entry(newW, width=50)
        file_browse_button = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,OFile, "Select a pix file", "openOfile", filetypes=[("Raster File","*.pix")]))

        file_label2 = Label(newW, text="Input Original pix File Classification Channel#:",font=("Arial", 11))
        ONum = Entry(newW, width=10)
        
                                 
        file_label3 = Label(newW, text="Input Modified pix File:",font=("Arial", 11))
        MFile = Entry(newW, width=50)
        file_browse_button3 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,MFile, "Select a pix file", "openMfile", filetypes=[("Raster File","*.pix")]))
        
        file_label4 = Label(newW, text="Input Modified pix File Classification Channel#:",font=("Arial", 11))
        MNum = Entry(newW, width=10)
        

        file_label5 = Label(newW, text="Set up the working directory:",font=("Arial", 11))
        strFolder = Entry(newW, width=50)
        file_browse_button5 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,strFolder, "Select a pix file", "setfolder"))

        file_label6 = Label(newW, text="Enter the province name(in abbreviation):",font=("Arial", 11))
        updateProvince = Entry(newW, width=10)
        
        run_button = Button(newW, text="RUN",fg="red",font=("Arial", 11, "bold"), command=lambda: run( OFile.get(),
                                                                   ONum.get(),
                                                                   MFile.get(),
                                                                   MNum.get(),
                                                                   strFolder.get(),
                                                                   updateProvince.get()))



        file_label.grid(row=2, column=1, padx=5, pady=5, sticky="E")
        OFile.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button.grid(row=2, column=5, padx=5, pady=5)
        
        file_label2.grid(row=3, column=1, padx=5, pady=5, sticky="E")
        ONum.grid(row=3, column=2, columnspan=3, padx=5, pady=5,sticky ="W")
       
        
        file_label3.grid(row=4, column=1, padx=5, pady=5, sticky="E")
        MFile.grid(row=4, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button3.grid(row=4, column=5, padx=5, pady=5)
        
        file_label4.grid(row=5, column=1, padx=5, pady=5, sticky="E")
        MNum.grid(row=5, column=2, columnspan=3, padx=5, pady=5,sticky="W")
        

        file_label5.grid(row=6, column=1, padx=5, pady=5, sticky="E")
        strFolder.grid(row=6, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button5.grid(row=6, column=5, padx=5, pady=5)

        file_label6.grid(row=7, column=1, padx=5, pady=5, sticky="E")
        updateProvince.grid(row=7, column=2, columnspan=3, padx=5, pady=5,sticky="W")

        run_button.grid(row=8,column=5, padx=5, pady=5, sticky="E")



        def browse(newW,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):
    
            if(type=="openOfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Original provincial pix file:",filetypes=filetypes)
            elif(type=="openMfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Modified Provincial pix file:",filetypes=filetypes)
            elif(type=="setfolder"):
                case = tkFileDialog.askdirectory(parent=newW,title= "Set up your working Folder:",mustexist=mustexist)
            else:
                raise ValueError(type + " is not a valid browse dialog type.")
                return

            if(len(case)>0):
                dir = os.path.dirname(case)
                textbox.delete(0, END)
                textbox.insert(0, case)


       # Updating the existing province in the national.shp with newly modified provincial pix file.
       
        def run(OFile,ONum,MFile,MNum,strFolder,updateProvince) :


            strEASI_Script = "findOverlap"
            print("")
            print ("Update the province data in the existing national.shp")

            # Open easi script from the working directory 

            f_EASI = open(os.path.join(strFolder, strEASI_Script + ".eas"), "w")

            #----- Create prm.prm -----

            f_EASI.write("RUN COPPRM\n\n")

            #---------Declare variables------

            f_EASI.write("!----- Declare variables -----\n")
            f_EASI.write("local string strFolder, strPIXO, strPIXM\n") 
            f_EASI.write("local integer intClassif_O, intClassif_M, newChannelM, f_PIXM, f_PIXO\n") 
            f_EASI.write("intClassif_O = "+str(ONum)+"\n")
            f_EASI.write("intClassif_M = "+str(MNum)+"\n")
            f_EASI.write("strPIXO = \""+OFile+"\"\n")
            f_EASI.write("strPIXM = \""+MFile+"\"\n")
            f_EASI.write("strFolder = \""+strFolder+"\"\n")

            #----------PCI mod---------------
            f_EASI.write("!----------PCI mod---------------\n")
            f_EASI.write("FILE = \""+MFile+"\"\n") 
            f_EASI.write("PCIOP = \"ADD\"\n")
            f_EASI.write("PCIVAL = 1\n")
            f_EASI.write("RUN PCIMOD\n")
            f_EASI.write("f_PIXM = DBOpen(\""+MFile+"\", \"w\" )\n")
            f_EASI.write("f_PIXO = DBOpen(\""+OFile+"\", \"r\" )\n")
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
            f_EASI.write("FILI	=\""+MFile+"\"\n")
            f_EASI.write("FILO    =	strFolder + \"\\\\\" + \"overlap.tif\"\n")
            f_EASI.write("DBIW	=  \n")
            f_EASI.write("DBIC	= newChannelM  \n") 
            f_EASI.write("DBIB	= \n")
            f_EASI.write("DBVS	= \n")
            f_EASI.write("DBLUT	= \n")
            f_EASI.write("DBPCT	= \n")
            f_EASI.write("FTYPE	=	\"TIF\"\n")
            f_EASI.write("FOPTIONS	=	\n")
            f_EASI.write("RUN FEXPORT \n")

            #--------------delete the overlap channel-------------------
            f_EASI.write("!----------delete the old ones--------------\n")
            f_EASI.write("FILE = \""+MFile+"\"\n")
            f_EASI.write("PCIOP = \"DEL\" \n")
            f_EASI.write("PCIVAL = newChannelM \n")
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
            outPolygons = strFolder + "/" + updateProvince + ".shp"
            field = "VALUE"

            # Execute RasterToPolygon
            arcpy.RasterToPolygon_conversion(inRaster, outPolygons, "NO_SIMPLIFY", field)


            print ("mergeing the new provincial file to the national shapefile")

            #--------------------add province identifer-------

            from arcpy import env
            # Set environment settings
            env.workspace = strFolder
             
            # Set local variables
            inFeatures = updateProvince+ ".shp"
            fieldName = "Province"
            fieldAlias = "ProID"
            fieldPrecision = 10

             
            # Execute AddField twice for two new fields
            arcpy.AddField_management(inFeatures, fieldName, "TEXT", fieldPrecision, "", "",
                                      fieldAlias, "NULLABLE")




            # Create update cursor for feature class 
            # 
            rows = arcpy.UpdateCursor(strFolder + "/"+ updateProvince +".shp") 

            # Update the field used in buffer so the distance is based on the road 

            for row in rows:
                row.Province = updateProvince
                rows.updateRow(row) 

            # Delete cursor and row objects to remove locks on the data 
            # 
            del row 
            del rows


            #-----------------------Delete old provincial data from the national.shp---------------


            from arcpy import env
            env.workspace = strFolder
            layerName = "national.shp"
            fieldname = "Province"
            expression = "\"Province\" = \'"+updateProvince+"\'"  
               
            with arcpy.da.UpdateCursor(layerName, fieldname, expression) as rows:
              for row in rows:
                rows.deleteRow()
                

            #----------------------Delete the LandClass----------
            from arcpy import env
            env.workspace = strFolder
            infile = "national.shp"
            arcpy.DeleteField_management(infile, "LandClass")

            #-----------------------Delete class with 0 values ---------------


            from arcpy import env
            env.workspace = strFolder
            layerName = updateProvince+ ".shp"
            fieldname = "GRIDCODE"
            expression = "\"GRIDCODE\" = 0"  
               
            with arcpy.da.UpdateCursor(layerName, fieldname, expression) as rows:
              for row in rows:
                rows.deleteRow()


            #--------------- merge the polygons together ---------------- 

            # feature classes to be merged
            oldPoly = "national.shp"
            newPoly = updateProvince+ ".shp"

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


            #--------------- Delete the intermediate files ----------------
            print (".")
            print ("Delete the intermediate steps")
            #Set local variables
            out_data1 = updateProvince +".shp"
            out_data2 = "national.shp"
            out_data3 = "overlap.tif"
            out_data4 = "findOverlap.eas"
            out_data5 = "overlap.tif.pox"
            data_type = ""
            arcpy.Delete_management(out_data1, data_type)
            arcpy.Delete_management(out_data2, data_type)
            arcpy.Delete_management(out_data3, data_type)
            arcpy.Delete_management(out_data4, data_type)
            arcpy.Delete_management(out_data5, data_type)

            #--------------- Rename ----------------
            print (".")
            print ("Rename the new file to national.shp")
            #Set local variables
            in_data =  "new_national.shp"
            out_data = "national.shp"
            data_type = ""

            #Execute Rename
            arcpy.Rename_management(in_data, out_data, data_type)
            print ("The process is done!")
            print ("The data of " + updateProvince + " province has been updated!")
            print ("")
            print ("---------------------------------------------------------------------------")


                    
    def updateP(self):

        # Creating the SUB-GUI for Update modified pix file using national.shp file

        newW = Toplevel(root)
        newW.title("Update the Provincial pix file")
        newW.resizable(0,0)
                                 
        file_label2 = Label(newW, text="Input Modified pix File:",font=("Arial", 11))
        MFile = Entry(newW, width=50)
        file_browse_button3 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,MFile, "Select a pix file", "openMfile", filetypes=[("Raster File","*.pix")]))
        
        file_label3 = Label(newW, text="Input Modified pix File Classification Channel#:",font=("Arial", 11))
        MNum = Entry(newW, width=10)

        file_label4 = Label(newW, text="Input the National Shapefile:",font=("Arial", 11))
        SFile = Entry(newW, width=50)
        file_browse_button4 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,SFile, "Select a shp file", "openSfile", filetypes=[("Raster File","*.shp")]))
        

        file_label5 = Label(newW, text="Set up the working directory:",font=("Arial", 11))
        strFolder = Entry(newW, width=50)
        file_browse_button5 = Button(newW,text="Browse",font=("Arial", 11, "bold"),command=lambda: browse(newW,strFolder, "Select a pix file", "setfolder"))

        file_label6 = Label(newW, text="Enter the province name(in abbreviation):",font=("Arial", 11))
        updateProvince = Entry(newW, width=10)
        
        run_button = Button(newW, text="RUN",fg="red",font=("Arial", 11, "bold"), command=lambda: run(
                                                                   MFile.get(),
                                                                   MNum.get(),
                                                                   SFile.get(),
                                                                   strFolder.get(),
                                                                   updateProvince.get()))

      
        file_label2.grid(row=2, column=1, padx=5, pady=5, sticky="E")
        MFile.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button3.grid(row=2, column=5, padx=5, pady=5)
        
        file_label3.grid(row=3, column=1, padx=5, pady=5, sticky="E")
        MNum.grid(row=3, column=2, columnspan=3, padx=5, pady=5,sticky="W")

        file_label4.grid(row=4, column=1, padx=5, pady=5, sticky="E")
        SFile.grid(row=4, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button4.grid(row=4, column=5, padx=5, pady=5)

        file_label5.grid(row=5, column=1, padx=5, pady=5, sticky="E")
        strFolder.grid(row=5, column=2, columnspan=3, padx=5, pady=5)
        file_browse_button5.grid(row=5, column=5, padx=5, pady=5)

        file_label6.grid(row=6, column=1, padx=5, pady=5, sticky="E")
        updateProvince.grid(row=6, column=2, columnspan=3, padx=5, pady=5,sticky="W")

        run_button.grid(row=7,column=5, padx=5, pady=5, sticky="E")



        def browse(newW,textbox,dialogtitle, type, mustexist=1, filetypes=[("All","*")]):
    
            if(type=="openMfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Modified provincial pix file:",filetypes=filetypes)
            elif(type=="openSfile"):
                case = tkFileDialog.askopenfilename(parent=newW,title = "Find the national shapefile",filetypes=filetypes)
            elif(type=="setfolder"):
                case = tkFileDialog.askdirectory(parent=newW,title= "Set up your working Folder:",mustexist=mustexist)
            else:
                raise ValueError(type + " is not a valid browse dialog type.")
                return

            if(len(case)>0):
                dir = os.path.dirname(case)
                textbox.delete(0, END)
                textbox.insert(0, case)
                
        def run(MFile,MNum,SFile,strFolder,newProvince) :

                print("")
                print ("Update the value of the overlaped areas from other .pix file") 
                strEASI_Script = "updateP"
                f_EASI = open(os.path.join(strFolder, strEASI_Script + ".eas"), "w")

                # ----------------- Create prm.prm-------------

                f_EASI.write("RUN COPPRM\n\n")

                #---------Declare variables------

                f_EASI.write("!----- Declare variables -----\n")
                f_EASI.write("local string strFolder, strSHP, strPIX,strPIXI,strPIXM,strPIXC \n") 
                f_EASI.write("local integer intClassif_M, f_PIX,newChannel\n") 
                f_EASI.write("intClassif_M = "+str(MNum)+"\n")
                f_EASI.write("strPIXM = \""+MFile+"\"\n")
                f_EASI.write("strPIXC = \"cliped.pix\"\n")
                f_EASI.write("strPIX = \"new.pix\"\n")
                f_EASI.write("strPIXI = \"input.pix\"\n")
                f_EASI.write("strSHP = \""+SFile+"\"\n")
                f_EASI.write("strFolder = \""+strFolder+"\"\n")


                #-------------------------convert the .shp file to a new .pix file --------------
                f_EASI.write("!----------TIFF to raster-------------\n")
                f_EASI.write("FILI = \""+SFile+"\" \n")
                f_EASI.write("FILO =  \""+strFolder+"\" + \"\\\\\" + strPIX \n")
                f_EASI.write("RUN fimport\n")

                #-------------------------create a new raster file--------------------

                f_EASI.write("!----------vector to raster-------------\n")
                f_EASI.write("FILI = \""+strFolder+"\" + \"\\\\\" + strPIX \n")
                f_EASI.write("FILO = \""+strFolder+"\" + \"\\\\\" + strPIXI \n")
                f_EASI.write("FLDNME = \"GRIDCODE\" \n")
                f_EASI.write("DBVS = 2 \n")
                f_EASI.write("PIXRES = 30 \n")
                f_EASI.write("RUN POLY2RAS\n")


                #-------------------------Create cliped file only cover the target area--------------
                f_EASI.write("!----------Clip-------------\n")
                f_EASI.write("FILI = \""+strFolder+"\" + \"\\\\\" + strPIXI \n")
                f_EASI.write("FILO = \""+strFolder+"\" + \"\\\\\" + strPIXC \n")
                f_EASI.write("DBIC = 1 \n")
                f_EASI.write("CLIPFIL = strPIXM \n")
                f_EASI.write("CLIPLAY = 1 \n")
                f_EASI.write("RUN CLIP\n")
                f_EASI.write("\n")

                #-------------------pci mod -------------
                f_EASI.write("!-------------PCI mod add------------\n")
                f_EASI.write("FILE = \""+MFile+"\" \n")
                f_EASI.write("PCIOP = \"ADD\" \n")
                f_EASI.write("PCIVAL = 1 \n")
                f_EASI.write("RUN PCIMOD\n")
                f_EASI.write("\n")
                #-----------------run regpro ---------------------------
                f_EASI.write("!----------regpro-------------\n")
                f_EASI.write("f_PIX = DBOpen(\""+MFile+"\", \"w\" )\n")
                f_EASI.write("newChannel = DBChannels(f_PIX)\n")
                f_EASI.write("FILI = \""+strFolder+"\" + \"\\\\\" + strPIXC \n")
                f_EASI.write("FILO = \""+MFile+"\"\n")
                f_EASI.write("DBIC = 1 \n")
                f_EASI.write("DBOC = newChannel \n")
                f_EASI.write("RUN REGPRO\n")
                f_EASI.write("Call DBClose(f_PIX)\n")
                f_EASI.write("\n")

                #-------------------------create a new bitmap with the overlaped areas in the Modified .pix file --------------

                f_EASI.write("!----------Raster to Bitmap-------------\n")
                f_EASI.write("FILI = \""+MFile+"\" \n")
                f_EASI.write("FILO = \""+MFile+"\" \n")
                f_EASI.write("DBIC = newChannel \n")
                f_EASI.write("RUN RAS2BIT\n")


                #--------------create a new raster channel only contains the overlapped areas-----------------

                f_EASI.write("!----------convert channel--------------\n")
                f_EASI.write("MODEL ON \""+MFile+"\"  \n")
                f_EASI.write("if %%3 = 1 then          \n")
                f_EASI.write("if %{intClassif_M} <> %{newChannel} then \n")
                f_EASI.write("  %{intClassif_M} = %{newChannel} \n")
                f_EASI.write("endif\n")
                f_EASI.write("endif\n")
                f_EASI.write("ENDMODEL \n")

                #--------------delete non-useful channels -----------------

                f_EASI.write("!-------------PCI mod delete------------\n")
                f_EASI.write("FILE = \""+MFile+"\" \n")
                f_EASI.write("PCIOP = \"DEL\" \n")
                f_EASI.write("PCIVAL = newChannel \n")
                f_EASI.write("RUN PCIMOD\n")
                f_EASI.write("\n")

                f_EASI.write("!-------------DAS delete segment------------\n")
                f_EASI.write("FILE = \""+MFile+"\" \n")
                f_EASI.write("PCIOP = \"DEL\" \n")
                f_EASI.write("DBSL = 3 \n")
                f_EASI.write("RUN DAS\n")
                f_EASI.write("\n")
				
                #--------------delete intermediate .pix files -----------------
                
                f_EASI.write("!-------------DBDelete------------\n")
                f_EASI.write("call DBDelete( \"PIX\",\"cliped.pix\" ) \n")
                f_EASI.write("call DBDelete( \"PIX\",\"input.pix\" ) \n")
                f_EASI.write("call DBDelete( \"PIX\",\"new.pix\" ) \n")

                f_EASI.close()

                print (".")
                os.chdir(os.path.join(strFolder))
                subprocess.call("EASI run " + strEASI_Script)
                print ("EASI script has successfully created..")
                
                
                #--------------- Delete the intermediate files -------------------
                
                out_data1 = "updateP.eas"
                data_type = ""
                arcpy.Delete_management(out_data1, data_type)
                
            
                print ("The process is done!")
                print ("The value of overlaped areas have been updated!")
                print ("")
                print ("-----------------------------------------------------------------------")
                
             

        
	
root = Tk()
root.title("Crop Inventory Revision facilitation")
root.resizable(0,0)
app = App(root)
root.mainloop()
root.destroy() 
