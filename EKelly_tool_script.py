# by Eniko Kelly-Voicu, 2018


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




# this script works with following column titles: "centroid_x" for x coordinates of the point, "centroid_y" for the y coordinates.
# YEAR_ is the title of the column of the time periods used in calculation Year, month, decade etc.)
# FOR TIME SUBSET THE FIRST AND LAST YEAR OF THE PERIOD is defined in row 70. Output PATH and Title of the results (image and excel file) at the end of the script.
# Central point (origin of the coordinate system) is calculated based on the entries from row 17. Row 53: data subset to be plotted will be entered.
# If the dataset does not have records for some of the years, the user can add rows for the missing years and blank rings will be drawn. In the new rows the year_ has to be filled out and x, y coordinates equaling zero.

mydf = pd.read_excel('LA_1900_2017_table.xls', sheet_name='Sheet1') # THE CENTRAL POINT OF THE PLOT WILL BE CALCULATED BASED ON THIS FILE.
# IF THIS FILE IS THE SAME FROM ROW 50, THE RELATIVE CENTER WILL BE CALCULATED FOR THE DATA SUBSET.

#assign a new polar coordinate system based on the exsiting x,y cartesian coordinate values
Xmax = mydf['centroid_x'].max()
Xmin = mydf['centroid_x'].min()
Ymax = mydf['centroid_y'].max()
Ymin = mydf['centroid_y'].min()

# calculate the central point of the plot
if Xmax<0:
    Xcentr =Xmax-((Xmax-Xmin)/2)
elif Xmin>0:
    Xcentr = Xmin+((Xmax-Xmin)/2)
else:
    Xcentr = 0


if Ymax<0:
    Ycentr = Ymax - ((Ymax-Ymin)/2)
elif Ymin>0:
    Ycentr = Ymin + ((Ymax-Ymin)/2)
else:
    Ycentr = 0

print "Study Area Central Point Coordinates X, Y:"
print Xcentr
print Ycentr
print Xmax
print Xmin
print Ymax
print Ymin



#choose data subset to be plotted
mydf = pd.read_excel('LA_1900_2017_table.xls', sheet_name='Sheet1')
mydf.sort_values("YEAR_", inplace=True)

rows_no=mydf.shape[0]  # number of rows only    - mydf:
cols_no=mydf.shape[1]    # number of columns only - mydf:

#inserts new columns for the new coordinates which will be calculated and added to the dataframe.
mydf.insert(int(cols_no), "x", value = int)
mydf.insert(int(cols_no+1), "y", value = int)
mydf.insert(int(cols_no+2), "R", value = int)
mydf.insert(int(cols_no+3), "Angle_rad", value = float)
mydf.insert(int(cols_no+4), "R1", value = int)


mydf['x'] = mydf['centroid_x']-Xcentr
mydf['y'] = mydf['centroid_y']-Ycentr
# THE FIRST AND LAST YEAR OF THE PERIOD CAN BE SELECTED:
mydf = mydf[mydf['YEAR_'].between(1900, 2017, inclusive=True)]  #Select the time period to be plotted
YEAR_list = mydf['YEAR_'].tolist()


#creates list of unique year numbers. Assigns the first value which is -1. The index value will change only if the calendar year changes.
#Each new (different) calendar year will get a unique index, staring with zero: 0,1,2,..etc.
year_ix = [-1]

for i in range(len(YEAR_list)-1):
    if YEAR_list[i] == YEAR_list[i-1]:
        year_ix[i] = year_ix[i-1]
    else:
        year_ix[i]= year_ix[i-1]+1
    year_ix.append(year_ix[i])


mydf['year_ix'] = year_ix

#calculates the new polar coordinates and adds them to the dataframe
mydf["R"] = np.sqrt(np.power(mydf["x"],2 ) + np.power(mydf["y"],2 )).astype(np.float32)  #calculates distance from the central point with coordinates (0,0)
Rmax = mydf["R"].max()
print Rmax

mydf["Angle_rad"] = np.arctan2(mydf["y"], mydf["x"]).astype(np.float32) #calculates angle in radian
mydf["R1"] = mydf['R'] + (Rmax * mydf['year_ix'])



theta = mydf['Angle_rad'].tolist() #angle in radian
r = mydf['R1'].tolist()   #this is the transformed radius containing the time info and radius as polar coordinate

R1max = mydf["R1"].max()

#draws polar scatterplot
year_set = set(year_ix)
my_index = list(year_set)

area = 2  #this value defines the area of the points in the scatterplot
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8, 0.8],polar=True)
ax.set_ylim(0, R1max)   #maximum value of R1
ax.set_yticks(np.arange(Rmax, R1max, Rmax))  # if the rings representing the years are drawn every 10th year: ax.set_yticks(np.arange(0, R1max,10*Rmax). Otherwise (np.arange(0, R1max, Rmax))
ax.set_yticklabels(my_index, fontsize=4) #fontsize can be modified
ax.scatter(theta,r,c = 'b', s=area)
#ax.set_rmin(-R1max/3) # set offset. The value can be changed by the user as needed.
plt.show()
fig.savefig('C:/MY_FOLDER/FINAL/LA_1900_2017_3_rel.jpg') # save figure to your work folder

#The results of the above calculations can be written to an excel file.
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('C:/MY_FOLDER/FINAL/LA_1900_2017_3_rel.xlsx', engine='xlsxwriter') # save figure to your work folder

# Convert the dataframe to an XlsxWriter Excel object.
mydf.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
