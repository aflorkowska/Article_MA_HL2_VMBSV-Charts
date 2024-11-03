import os
import sys
import itertools 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as patches
import matplotlib.patches as mpatches

from utils import preprocess_data_from_csv, get_distances_as_list_from_csv
from config import MARKER_SIZES, ARUCO_CENTERS_VS_CORNERS_COMPARISON_PATH, COLORS, BG_COLORS

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# IMPORT DATA
data = pd.read_csv(ARUCO_CENTERS_VS_CORNERS_COMPARISON_PATH)
aruco = preprocess_data_from_csv(data, MARKER_SIZES, 'aruco')
qrCodes = preprocess_data_from_csv(data, MARKER_SIZES, 'code')

# SET CONSTRAINTS
distances_in_mm = get_distances_as_list_from_csv(data)
all_samples_number = 40 # 8 samples per color (= per distance): 4 for aruco and 4 for qrcodes
dx = all_samples_number / len(distances_in_mm)

labels_xticks  = ['300','500','750','1000', '1250']
centers_for_labels_xticks = [i * (dx / 2) + 0.5 for i in range(1,11,2)]
values_for_brackets = [0.136, 0.318, 0.5, 0.6815, 0.8635]
samples_positions = np.array([i for i in range(1, all_samples_number + 1)])

# GENERATE PLOT
### DISPLAY DATA
fig, ax = plt.subplots(figsize=(16,10), dpi=300)
fig.subplots_adjust(right=0.85)
plt.xlabel("Distance [mm]", fontsize=14)
plt.ylabel("Mean position error [mm]", fontsize=14)

i = 0
j = 0

for color, size in zip(COLORS, MARKER_SIZES):
    for arucoVal, codeVal in itertools.zip_longest(aruco.get(size), qrCodes.get(size)):
        if codeVal != None:
            ax.errorbar(samples_positions[i], codeVal[0], yerr = codeVal[2], c = color,  marker = 's', capsize = 3,  ms=10)
            ax.scatter(samples_positions[i],codeVal[1], c = 'r',  marker = '_', s=600)
        if arucoVal != None:
            ax.errorbar(samples_positions[i+1], arucoVal[0], yerr = arucoVal[2], c = color,  marker = 's', fillstyle='none', capsize = 3,  ms=10)
            ax.scatter(samples_positions[i+1], arucoVal[1], c = 'r',  marker = '_', s=600)
        i+=8
   
    j += 2
    i = j


### SET X AXIS PROPERTIES
ax.set_xticks(centers_for_labels_xticks)
ax.set_xticklabels(labels_xticks)

### ADD BRACKETS TO SEPARATE DATA FROM DIFFERENT DISTANCES
for i in range(0, len(values_for_brackets)):
    ax.axvspan(i * dx + 0.5, (i + 1 ) * dx + 0.5, facecolor = BG_COLORS[i], alpha=0.45)
    ax.annotate('', xy=(values_for_brackets[i], 0.015), xycoords='axes fraction', ha='center', va='bottom', 
                xytext=(values_for_brackets[i], 0),
                bbox=dict(boxstyle='square', fc='white'),
                arrowprops=dict(arrowstyle='-[, widthB=7.4, lengthB=0.5', lw=1.5))
    
### ADD LEGEND
###### MARKER SIZES
blue_patch = mpatches.Patch(color = COLORS[0], label='Marker size ~ 75 mm')
orange_patch = mpatches.Patch(color = COLORS[1], label='Marker size ~ 65 mm')
green_patch = mpatches.Patch(color = COLORS[2], label='Marker size ~ 37 mm')
red_patch = mpatches.Patch(color = COLORS[3], label='Marker size ~ 23 mm')
fig.legend(handles=[blue_patch, orange_patch, green_patch, red_patch] , loc = 'center', bbox_to_anchor=(0.80,0.02)).set_title("Markers")

###### MARKERS THAT DIFFER QRCODES VS ARUCO
circleMEANAruco = plt.plot([],[], marker="s", ms=10, ls="", fillstyle='none', color='black', label='Mean with std - ArUco marker')[0]
circleMEANCode = plt.plot([],[], marker="s", ms=10, ls="",  color='black', label='Mean with std - QR Code')[0]
crossMEDIAN = plt.plot([],[], marker="_", ms=10, ls="", color='red', label='Median')[0]
fig.legend(handles=[circleMEANAruco, circleMEANCode , crossMEDIAN] , loc = 'center', bbox_to_anchor=(0.22,0.02))

###### DISTANCES
D30cm = patches.Rectangle((0,0),1,1,facecolor=BG_COLORS[0],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 300 mm') 
D50cm = patches.Rectangle((0,0),1,1,facecolor=BG_COLORS[1],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 500 mm') 
D75cm = patches.Rectangle((0,0),1,1,facecolor=BG_COLORS[2],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 750 mm')  
D100cm = patches.Rectangle((0,0),1,1,facecolor=BG_COLORS[3],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1000 mm')  
D125cm = patches.Rectangle((0,0),1,1,facecolor=BG_COLORS[4],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1250 mm') 
fig.legend(handles=[D30cm, D50cm, D75cm, D100cm, D125cm] , loc = 'center',bbox_to_anchor=(0.52,0.02),  ncol=2).set_title("The same background color means that the measurments were made from the same distance:")

