import os
import sys
import itertools 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as patches
import matplotlib.patches as mpatches

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import preprocess_data_from_csv, get_distances_as_list_from_csv
from config import MARKER_SIZES, ARUCO_CENTERS_ANGLES_COMPARISON_PATH, COLORS, BG_COLORS

# IMPORT DATA
data = pd.read_csv(ARUCO_CENTERS_ANGLES_COMPARISON_PATH)
aruco_centers_const90angle = preprocess_data_from_csv(data, MARKER_SIZES, 'center')
aruco_centers_bigger_angles = preprocess_data_from_csv(data, MARKER_SIZES, 'center', '_mean_DAL', '_median_DAL', '_std_DAL')
aruco_centers_smaller_angles = preprocess_data_from_csv(data, MARKER_SIZES, 'center', '_mean_BLIZ', '_median_BLIZ', '_std_BLIZ')

# SET CONSTRAINTS
distances_in_mm = get_distances_as_list_from_csv(data)
all_samples_number_per_subplot = 20 # 4 samples per bg color (= per distance = 5))
dx = all_samples_number_per_subplot / len(distances_in_mm)

labels_xticks  = [['300 \n φ ~ 90','500 \n φ ~ 90','750 \n φ ~ 90','1000 \n φ ~ 90', '1250 \n φ ~ 90'],  
                  ['300 \n φ ~ 75','500 \n φ ~ 70','750 \n φ ~ 80','1000 \n φ ~ 60', '1250 \n φ ~ 45'], 
                  ['300\n φ ~ 75','500 \n φ ~ 55','750 \n φ ~ 40','1000 \n φ ~ 30', '1250 \n φ ~ 20']]
centers_for_labels_xticks = [i * (dx / 2) + 0.5 for i in range(1,11,2)]
values_for_brackets = [0.136, 0.318, 0.5, 0.6815, 0.8635]
samples_positions = np.array([i for i in range(1, all_samples_number_per_subplot + 1)])

# GENERATE PLOT
### DISPLAY DATA
fig = plt.figure(figsize=(16,8), dpi=300)
gs = fig.add_gridspec(1, 3, hspace=0, wspace=0.05)
ax1, ax2, ax3 = gs.subplots(sharex=False, sharey=True)
axes = [ax1, ax2, ax3]
ax1.set_ylabel('Mean position error [mm]', fontsize=14)
fig.supxlabel('Distance [mm] with the corresponding φ angle [°]', fontsize=14)

i = 0
j = 0

for color, size in zip(COLORS, MARKER_SIZES):
    for const, bigger, smaller in itertools.zip_longest(aruco_centers_const90angle.get(size), aruco_centers_bigger_angles.get(size), aruco_centers_smaller_angles.get(size)):
        if const != None:
            ax1.errorbar(x[i], const[0], yerr = const[2], c = color,  marker = 'o',  capsize = 3, ms=8)
            ax1.scatter(x[i],const[1], c = 'r',  marker = '_', s=600)
        if smaller != None:
            ax2.errorbar(x[i], smaller[0], yerr = smaller[2], c = color,  marker = 'o', capsize = 3, ms=8)
            ax2.scatter(x[i], smaller[1], c = 'r',  marker = '_', s=600)
        if bigger != None:
            ax3.errorbar(x[i], bigger[0], yerr = bigger[2], c = color,  marker = 'o', capsize = 3, ms=8)
            ax3.scatter(x[i], bigger[1], c = 'r',  marker = '_', s=600)
        i+=4
    j+=1
    i=j

### SET X AXIS PROPERTIES
for ax, names in zip(axes, labels_xticks):    
    ax.set_xticks(centers_for_labels_xticks)
    ax.set_xticklabels(names)
    for i in range(0,5):
        ax.axvspan(i*dx + 0.5, (i+1)*dx + 0.5, facecolor = BG_COLORS[i], alpha=0.45)
        ax.annotate('', xy=(values_for_brackets[i], 0.015), xycoords='axes fraction', ha='center', va='bottom', 
                    xytext=(values_for_brackets[i], 0),
                    bbox=dict(boxstyle='square', fc='white'),
                    arrowprops=dict(arrowstyle='-[, widthB=2.5, lengthB=0.5', lw=1.5))

### ADD LEGEND
###### MARKER SIZES
blue_patch = mpatches.Patch(color = COLORS[0], label='Marker size ~ 75 mm')
orange_patch = mpatches.Patch(color = COLORS[1], label='Marker size ~ 65 mm')
green_patch = mpatches.Patch(color = COLORS[2], label='Marker size ~ 37 mm')
red_patch = mpatches.Patch(color = COLORS[3], label='Marker size ~ 23 mm')
fig.legend(handles=[blue_patch, orange_patch, green_patch, red_patch] , loc = 'center', bbox_to_anchor=(0.80,-0.065)).set_title("Markers")

###### MARKERS THAT DIFFER QRCODES VS ARUCO
circleMEANCode = plt.plot([],[], marker="o", ms=10, ls="",  color='black', label='Mean with std - centers of ArUco marker')[0]
crossMEDIAN = plt.plot([],[], marker="_", ms=10, ls="", color='red', label='Median')[0]
fig.legend(handles=[ circleMEANCode , crossMEDIAN] , loc = 'center', bbox_to_anchor=(0.2,-0.065))

###### DISTANCES
D30cm = patches.Rectangle((0,0),1,1,facecolor= BG_COLORS[0],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 300 mm') 
D50cm = patches.Rectangle((0,0),1,1,facecolor= BG_COLORS[1],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 500 mm') 
D75cm = patches.Rectangle((0,0),1,1,facecolor= BG_COLORS[2],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 750 mm')  
D100cm = patches.Rectangle((0,0),1,1,facecolor= BG_COLORS[3],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1000 mm')  
D125cm = patches.Rectangle((0,0),1,1,facecolor= BG_COLORS[4],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1250 mm') 
fig.legend(handles=[D30cm, D50cm, D75cm, D100cm, D125cm] , loc = 'center',bbox_to_anchor=(0.52,-0.065),  ncol=2).set_title("The same background color means that the measurments were made from the same distance:")