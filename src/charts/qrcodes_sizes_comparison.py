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
from config import MARKER_SIZES, ARUCO_QRCODES_COMPARISON_PATH, COLORS, BG_COLORS

# IMPORT DATA
data = pd.read_csv(ARUCO_QRCODES_COMPARISON_PATH)

realSizes = {}
detectedSizes = {}

for size in MARKER_SIZES:
    mean = data['codeREAL'+ str(size) +'_mean'].dropna().tolist()
    median = data['codeREAL'+ str(size) +'_median'].dropna().tolist()
    std = data['codeREAL'+ str(size) +'_std'].dropna().tolist()
    rangeAcceptance = data['1%stdREAL'+ str(size)].dropna().tolist()
    realSizes[size] = [ [i,j,k,m] for i, j, k, m in zip(mean, median, std, rangeAcceptance)][0]
    
for size in MARKER_SIZES:
    mean = data['code'+ str(size) +'_mean'].dropna().tolist()
    median = data['code'+ str(size) +'_median'].dropna().tolist()
    std = data['code'+ str(size) +'_std'].dropna().tolist()
    detectedSizes[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]  
    suma = [ i for i in mean]  
    if(len(mean) == 1):
        detectedSizes[str(size)+"Average"] = [mean[0], median[0], std[0]]        
    else:
        detectedSizes[str(size)+"Average"] = [np.mean(suma), np.median(suma), np.std(suma)]

# SET CONSTRAINTS
distances_in_mm = get_distances_as_list_from_csv(data)
x = np.array([1,2])
colors = ['blue', 'orange', 'green', 'purple']
i = 0

# GENERATE PLOT
### DISPLAY DATA
fig = plt.figure(figsize=(16,6), dpi=300)
gs = fig.add_gridspec(1, 4, hspace=0, wspace=0.25)
ax1, ax2, ax3, ax4 = gs.subplots(sharex=True, sharey=False)
axes = [ax1, ax2, ax3, ax4]
ax1.set_ylabel('Mean position error [mm]', fontsize=14)
fig.supxlabel('Markers', fontsize=14)

for size, color, axs in zip(MARKER_SIZES, colors, axes):
    axs.add_patch(patches.Rectangle((x[i] - 0.25, realSizes.get(size)[0] - realSizes.get(size)[3]),1.5 , 2*realSizes.get(size)[3], facecolor=color, alpha=0.5))
    axs.errorbar(x[i], realSizes.get(size)[0], yerr = realSizes.get(size)[2], c = 'black',  marker = 's', capsize = 3, ms=10)
    axs.scatter(x[i],realSizes.get(size)[1], c = 'r',  marker = '_', s=600)
    axs.errorbar(x[i+1], detectedSizes.get(str(size)+'Average')[0], yerr = detectedSizes.get(str(size)+'Average')[2], c = 'black',  marker = 's', capsize = 3, ms=10)
    axs.scatter(x[i+1],detectedSizes.get(str(size)+'Average')[1], c = 'r',  marker = '_', s=600)
    i=0
    

### SET X AXIS PROPERTIES
names = ['measured \n using caliper', 'detected \n on Hololens2']
labels = [['Actual marker size \n~ 75 mm',''], ['Actual marker size \n~ 65 mm', ''],['Actual marker size \n~ 37 mm', ''],['Actual marker size \n~ 23 mm', '']]
    
for ax, label in zip(axes, labels):    
    ax.set_xticks([1,2])
    ax.set_xticklabels(names)
    axMarkers = ax.twiny()
    axMarkers.set_xticks([1,2])
    axMarkers.set_xticklabels(label)
    
### ADD LEGEND
blue_patch = mpatches.Patch(color=colors[0], alpha=0.5, label='For marker size ~ 75 mm')
orange_patch = mpatches.Patch(color= colors[1], alpha=0.5, label='For marker size ~ 65 mm')
green_patch = mpatches.Patch(color=colors[2], alpha=0.5,  label='For marker size ~ 37 mm')
red_patch = mpatches.Patch(color=colors[3], alpha=0.5, label='For marker size ~ 23 mm')
fig.legend(handles=[blue_patch, orange_patch, green_patch, red_patch] , loc = 'center', ncol=4, bbox_to_anchor=(0.58,-0.05)).set_title("Max. size error tolerance - according to Microsoft * (at most a 1% error from the actual size)")

circleMEAN = plt.plot([],[], marker="s", ms=10, ls="",  mec=None, color='black', label='Mean with std - QR Code')[0]
crossMEDIAN = plt.plot([],[], marker="_", ms=10, ls="", mec=None, color='red', label='Median')[0]
fig.legend(handles=[circleMEAN, crossMEDIAN] , loc = 'center', bbox_to_anchor=(0.2,-0.05))
plt.figtext(0.58,-0.14, "* \"QR code tracking overview\" Microsoft, 10 Apr. 2022,\n learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/qr-code-tracking-overview. Accessed 25 Apr. 2023", ha="center", fontsize=10)

