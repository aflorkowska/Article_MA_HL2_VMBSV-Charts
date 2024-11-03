import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as patches
import matplotlib.patches as mpatches

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from config import MARKER_SIZES, QRCODES_MARKER_SIZES_COMPARISON_PATH

data = pd.read_csv(QRCODES_MARKER_SIZES_COMPARISON_PATH)

distancesMM = data['distance'].tolist()

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



fig, ax = plt.subplots(figsize=(16,8), dpi=300)
plt.xlabel("Markers", fontsize=14)

x = np.array([1,2,3,4,5,6,7,8])
twin1 = ax.twinx()
twin2 = ax.twinx()
twin3 = ax.twinx()
twin2.spines.right.set_position(("axes", 1.15))
twin3.spines.right.set_position(("axes", 1.3))

colors = ['blue', 'orange', 'green', 'purple']
axes = [ax, twin1, twin2, twin3]

i = 0
for size, color, axs in zip(MARKER_SIZES, colors, axes):
    axs.add_patch(patches.Rectangle((x[i] - 0.25, realSizes.get(size)[0] - realSizes.get(size)[3]),1.5 , 2*realSizes.get(size)[3], facecolor=color, alpha=0.5))
    axs.errorbar(x[i], realSizes.get(size)[0], yerr = realSizes.get(size)[2], c = 'black',  marker = 's', capsize = 3, ms=10)
    axs.scatter(x[i],realSizes.get(size)[1], c = 'r',  marker = '_', s=600)
    axs.errorbar(x[i+1], detectedSizes.get(str(size)+'Average')[0], yerr = detectedSizes.get(str(size)+'Average')[2], c = 'black',  marker = 's', capsize = 3, ms=10)
    axs.scatter(x[i+1],detectedSizes.get(str(size)+'Average')[1], c = 'r',  marker = '_', s=600)
    i+=2


plt.xticks(x,['measured \n using caliper', 'detected \n on Hololens2', 'measured \n using caliper', 'detected \n on Hololens2','measured \n using caliper', 'detected \n on Hololens2','measured \n using caliper', 'detected \n on Hololens2'], fontsize=12)
axMarkers = ax.twiny()
axMarkers.set_xticks(x,['Actual marker size \n~ 75 mm', '', 'Actual marker size \n~ 65 mm', '' , 'Actual marker size \n~ 37 mm', '', 'Actual marker size \n~ 23 mm', ''], fontsize=12)

ax.set_ylabel("Mean size [mm]", fontsize=14)
ax.yaxis.label.set_color(colors[0])
twin1.set_ylabel("Mean size [mm]", fontsize=14)
twin1.yaxis.label.set_color(colors[1])
twin2.set_ylabel("Mean size [mm]", fontsize=14)
twin2.yaxis.label.set_color(colors[2])
twin3.set_ylabel("Mean size [mm]", fontsize=14)
twin3.yaxis.label.set_color(colors[3])


tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=colors[0], **tkw)
twin1.tick_params(axis='y', colors=colors[1], **tkw)
twin2.tick_params(axis='y', colors=colors[2], **tkw)
twin3.tick_params(axis='y', colors=colors[3], **tkw)
ax.tick_params(axis='x', **tkw)

blue_patch = mpatches.Patch(color=colors[0], alpha=0.5, label='For marker size ~ 75 mm')
orange_patch = mpatches.Patch(color= colors[1], alpha=0.5, label='For marker size ~ 65 mm')
green_patch = mpatches.Patch(color=colors[2], alpha=0.5,  label='For marker size ~ 37 mm')
red_patch = mpatches.Patch(color=colors[3], alpha=0.5, label='For marker size ~ 23 mm')
fig.legend(handles=[blue_patch, orange_patch, green_patch, red_patch] , loc = 'center', ncol=2, bbox_to_anchor=(0.45,-0.03)).set_title("Max. size error tolerance - according to Microsoft (1) \n (at most a 1% error from the actual size)")

circleMEAN = plt.plot([],[], marker="s", ms=10, ls="",  mec=None, color='black', label='Mean with std - QR Code')[0]
crossMEDIAN = plt.plot([],[], marker="_", ms=10, ls="", mec=None, color='red', label='Median')[0]
fig.legend(handles=[circleMEAN, crossMEDIAN] , loc = 'center', bbox_to_anchor=(0.22,-0.03))
plt.figtext(0.90,-0.05, "(1) - https://learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/qr-code-tracking-overview ", ha="center", fontsize=10)
