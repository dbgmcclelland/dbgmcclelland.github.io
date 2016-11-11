import arcpy, os
 
# Set File Locations for culverts feature class and create list of required fields
Culverts_FC = r"W:\ENG\COMMON\Culvert Action Plan\GIS\Drainage Assets.gdb\Culverts_and_Sewers"
fields = ["CVID", "DAID"]

# Creating and populating list of IDs from folder names
CVIDs = []
rootDir = r"L:\ER Geomatics\Geomatics1\Culvert Inventory\4015-E-0008 A1\Assignment 1 Photos Folder 2\Assignment 1 Photos Folder 2"

for item in os.listdir(rootDir):
        CVIDs.append(item)

temp = "temp"
arcpy.MakeFeatureLayer_management(Culverts_FC, temp) # Temporary layer required to use arcpy selctions

# Creates selection from list of IDs in folder
for ID in CVIDs:
        query = "CVID = '" + ID + "'"
        arcpy.SelectLayerByAttribute_management(temp, "ADD_TO_SELECTION", query)

# Search cursor for loop that matches old ID to new ID, and then renames the subfolder
cursor = arcpy.SearchCursor(temp, fields)
for row in cursor:
        CVID = row.getValue("CVID")
        DAID = row.getValue("DAID")
        New_Folder_Location = "L:\\ER Geomatics\\Geomatics1\\Culvert Inventory\\4015-E-0008 A1\\Assignment 1 Photos Folder 2\\Assignment 1 Photos Folder 2\\" + DAID
        Old_Folder_Location = "L:\\ER Geomatics\\Geomatics1\\Culvert Inventory\\4015-E-0008 A1\\Assignment 1 Photos Folder 2\\Assignment 1 Photos Folder 2\\" + CVID
        os.rename(Old_Folder_Location, New_Folder_Location)

print "Done"