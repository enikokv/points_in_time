import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy.da import *
arcpy.env.overwriteoutput=True
import math



inFeatures = arcpy.GetParameterAsText(0) #input: shapefile to calculate origin of the coordinate system
inFeatures1 = arcpy.GetParameterAsText(1) # input: x coordinate to calculate origin of the coordinate system
inFeatures2 = arcpy.GetParameterAsText(2) #input: y coordinate to calculate origin of the coordinate system
inFeatures3 = arcpy.GetParameterAsText(3) # input: Date or time periods, such as occurrence year, month, week, day etc. from inFeatures4
inFeatures4 = arcpy.GetParameterAsText(4) #input: shapefile to be plotted
inFeatures5 = arcpy.GetParameterAsText(5) # input: x coordinate to be plotted
inFeatures6 = arcpy.GetParameterAsText(6) #input: y coordinate to be plotted

field1 = inFeatures1 #coordinate x of the point
field2 = inFeatures2 #coordinate y of the point

x_val = [row[0] for row in arcpy.da.SearchCursor(inFeatures, field1)]
Xmax =  max(x_val)
Xmin = min(x_val)

y_val = [row[0] for row in arcpy.da.SearchCursor(inFeatures, field2)]
Ymax =  max(y_val)
Ymin = min(y_val)


if Xmax<0:
    Xcentr =Xmax-((Xmax-Xmin)/2)
elif Xmin>0:
    Xcentr = Xmin+((Xmax-Xmin)/2)
else:
    Xcentr = 0


if Ymax<0:
    Ycentr = Ymax-((Ymax-Ymin)/2)
elif Ymin>0:
    Ycentr = Ymin+((Ymax-Ymin)/2)
else:
    Ycentr = 0


field3 = "R"
field4 = "Radian"
field5 = "year_ix"
field6 = "Rindex"
field7 = "R1"
field10 = "x"
field11 = "y"
field12 = "Degree"

arcpy.AddField_management(inFeatures4, "R", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(inFeatures4, "Radian", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(inFeatures4, "year_ix", "SHORT", "", "", "4", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(inFeatures4, "R1", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(inFeatures4, "x", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(inFeatures4, "y", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(inFeatures4, "Degree", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")

field13 = inFeatures5 #coordinate x of the point
field14 = inFeatures6 #coordinate y of the point

cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    row.setValue(field10, row.getValue(field13) - Xcentr)
    cursor.updateRow(row)

cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    row.setValue(field11, row.getValue(field14) - Ycentr)
    cursor.updateRow(row)

cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    # field3 will be square root of sum of squared field1, field2
    row.setValue(field3, math.sqrt((row.getValue(field10) * row.getValue(field10))+ (row.getValue(field11) * row.getValue(field11))))
    cursor.updateRow(row)

cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    row.setValue(field4, math.atan2(row.getValue(field11),row.getValue(field10)))
    cursor.updateRow(row)

cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    row.setValue(field12, row.getValue(field4)* 180/ math.pi)
    cursor.updateRow(row)

fld_in = inFeatures3  # Date, time of occurences
fld_out = "year_ix"  #field added; it will be filled with output values

#create a list of values from the field using list comprehensions
lst_values=[r[0] for r in arcpy.da.SearchCursor(inFeatures4, (fld_in))]

#use da module for faster access
#use UpdateCursor to update values
index = 0
year_index = [0]
with arcpy.da.UpdateCursor(inFeatures4,(fld_in, fld_out)) as curs:
    for row in curs:
        name=row[0]
        if index == len(lst_values)-1:
            next_name = None
        else:
            next_name = lst_values[index+1]

        #compare the values
        if name == next_name:
            out_value = year_index[index]
        else:
            out_value = year_index[index] + 1
        year_index.append(out_value)
        #update the values
        curs.updateRow((name, out_value))

        #increment index
        index += 1


# search for maximum value of the Radius
field3 = "R"
r = [row[0] for row in arcpy.da.SearchCursor(inFeatures4, field3)]
Rmax =  max(r)

arcpy.AddField_management(inFeatures4, "Rindex", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    row.setValue(field6, Rmax * row.getValue(field5))
    cursor.updateRow(row)


arcpy.AddField_management(inFeatures4, "R1", "DOUBLE", "", "", "25", "", "NULLABLE", "REQUIRED", "")
field7 = "R1"
cursor = arcpy.UpdateCursor(inFeatures4)
for row in cursor:
    row.setValue(field7, row.getValue(field6) + row.getValue(field3))
    cursor.updateRow(row)

arcpy.AddMessage("Script was run. To see result check the input Feaure Class: Map Locations  updated columns")

