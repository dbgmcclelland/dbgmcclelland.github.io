
# Import arcpy module
import arcpy
from arcpy import env
import os, datetime, glob

# This script creates a culverts shapefile for export to MapGuide, with the latest inspections from the inspection table joined to each record.

print "Beginning export ......... "

# Local variables:
Local_GDB = "W:\\ENG\\COMMON\\Culvert Action Plan\\GIS\\Drainage Assets.gdb"
env.workspace = Local_GDB
arcpy.env.qualifiedFieldNames = False
Culverts_and_Sewers_Inspection_Table = "W:\\ENG\\COMMON\\Culvert Action Plan\\GIS\\Drainage Assets.gdb\\Culverts_and_Sewers_Inspection_Table"
CulvertsSewers = "W:\\ENG\\COMMON\\Culvert Action Plan\\GIS\\Drainage Assets.gdb\\Culverts_and_Sewers"
MapGuide_Folder = r"E:\OSGeo\MapGuide\Server\Repositories\Library\DataFiles\0271f36c-7728-11e5-8000-f0921ce59b65\"

# Convert FC to feature layer for join
arcpy.MakeFeatureLayer_management(CulvertsSewers, "Culverts_and_Sewers_temp")
CulvertsSewersLyr = "Culverts_and_Sewers_temp"

# Process: Add Join
print "Running initial join ........ "
arcpy.AddJoin_management(CulvertsSewersLyr, "DAID", Culverts_and_Sewers_Inspection_Table, "DAID", "KEEP_ALL")
print "Join complete, selecting unique DAIDs ........ "

# Creates feature class from joined layer

arcpy.CopyFeatures_management(CulvertsSewersLyr, "CulvertsSewersNew")
fc = "CulvertsSewersNew"
fields = ["DAID", "INS_DATE"]

# Loop to populate list of unique DAIDs

DAID = []

with arcpy.da.SearchCursor(fc, fields) as cursor:
    for row in cursor:
        if row[0] not in DAID and row[0] is not None:
            DAID.append(row[0])

arcpy.MakeFeatureLayer_management(fc, "CulvertsSewersNewTemp")
fl = "CulvertsSewersNewTemp"

print "Extracting dates ........ "

# Loop to build dictionary, key values are DAIDs and assigned the most recent inspection date as a value. If there are no inspection dates, a null value is assigned

dateDict = {}

for ID in DAID:
    exp = "DAID = '" + ID + "'"
    dates = []
    arcpy.SelectLayerByAttribute_management(fl, 'NEW_SELECTION', exp)
    with arcpy.da.SearchCursor(fl, fields) as cursor:
        for row in cursor:
            if row[1] is not None:
                dates.append(row[1])
    if len(dates) > 0: # Null dates will cause an error and should be fixed in the table. This check prevents an error if the only dates are null.
        maxdate = max(dates)
        dateDict[ID] = maxdate
    else:
        dateDict[ID] = None
    if len(dateDict) % 250 == 0:
        print "Date count: {0}".format(len(dateDict))

arcpy.SelectLayerByAttribute_management(fl, 'CLEAR_SELECTION')

# Final loop selects latest inspection based on date associated with DAID in dictionary. If all dates are null, each record associated with the DAID is selected. Causes a few duplicates, ideally records should be fixed.

print "Selecting latest inspections ......... "

for k in dateDict:
    ID = k
    date = dateDict[k]
    if date is not None:
        exp = "DAID = '" + ID + "' AND INS_DATE = date'" + date.strftime('%Y-%m-%d %H:%M:%S') + "'"
        arcpy.SelectLayerByAttribute_management(fl, 'ADD_TO_SELECTION', exp)
    else:
        exp = "DAID = '" + ID + "'"
        arcpy.SelectLayerByAttribute_management(fl, 'ADD_TO_SELECTION', exp)
            
print "Exporting feature class to shapefile and MapGuide ....... "


#Export to MapGuide
errorLog = r'W:\ENG\Geomatics\GIS\MapGuide_Data_Updates\log.txt'
filePath = errorLog
try:
######################     Step 1 - Test to see if file exists on MapGuide Server (if so, delete)   ######################
    test = MapGuide_Folder
    r = glob.glob(test)
    for i in r:
        os.remove(i)

######################     Step 2 - Export shapefile to MapGuide Server                             ######################
    arcpy.env.overwriteOutput = True
    arcpy.FeatureClassToShapefile_conversion (fl, MapGuide_Folder2)

######################     Step 3 - Log errors                                                      ######################
except:
    arcpy.AddMessage(arcpy.GetMessages(2))
    try:
        with open(errorLog,'a') as text_file:
            text_file.write("Update failed for" + Local_filename + "\n")
            text_file.write(str(datetime.datetime.today()))
            text_file.write("\n\n-------------------------------------------------------------------------------------------------------- \n\n")
            with open(errorLog,'a') as errorMsg:
                errorMsg.write("%s,%s\n" % (errorLog,arcpy.GetMessages(2)))
    except RuntimeError:
        arcpy.AddMessage("Unable to log")
        arcpy.AddMessage(RuntimeError.message)

# Delete copied feature class
arcpy.Delete_management(fc)

print "Done."
