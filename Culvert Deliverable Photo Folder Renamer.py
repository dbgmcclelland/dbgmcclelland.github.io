import arcpy, shutil, os
 
#Set File Locations for culverts feature class
Culverts_FC = r"W:\ENG\COMMON\Culvert Action Plan\GIS\Drainage Assets.gdb\Culverts_and_Sewers"
#Culverts_FC = "W:\\ENG\\Geomatics\\GIS\\Map & Data Requests\\Contracts\\Maintenance\\Culverts\\Data\\2016\\Carillion\\Deliverable\\Carillion 2016 Culvert Inspection Deliverables.gdb\\Culverts_and_Sewers"
fields = ["CVID", "DAID"]

#For loop to cycle through features
CVIDs = []
rootDir = r"L:\ER Geomatics\Geomatics1\Culvert Inventory\4015-E-0008 A1\Assignment 1 Photos Folder 2\Assignment 1 Photos Folder 2"
for item in os.listdir(rootDir):
        CVIDs.append(item)

temp = "temp"
arcpy.MakeFeatureLayer_management(Culverts_FC, temp)

for ID in CVIDs:
        query = "CVID = '" + ID + "'"
        arcpy.SelectLayerByAttribute_management(temp, "ADD_TO_SELECTION", query)

cursor = arcpy.SearchCursor(temp, fields)
for row in cursor:
        CVID = row.getValue("CVID")
        DAID = row.getValue("DAID")
        New_Folder_Location = "L:\\ER Geomatics\\Geomatics1\\Culvert Inventory\\4015-E-0008 A1\\Assignment 1 Photos Folder 2\\Assignment 1 Photos Folder 2\\" + DAID
        Old_Folder_Location = "L:\\ER Geomatics\\Geomatics1\\Culvert Inventory\\4015-E-0008 A1\\Assignment 1 Photos Folder 2\\Assignment 1 Photos Folder 2\\" + CVID
        os.rename(Old_Folder_Location, New_Folder_Location)

print "Done"
