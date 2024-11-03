# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:41:12 2023

@author: AgnieszkaFlorkowska
"""

import os
import pandas as pd
import numpy as np
import itertools 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as patches
import matplotlib.patches as mpatches

CSVPath  = r'D:\Kamery_[WYNIKI]\PracaMagisterska_[AGH]\Charts\qrcodesVSaruco.csv'
data = pd.read_csv(CSVPath)

distancesMM = data['distance'].tolist()
markersSizes = [75,65,37,23]

qrCodes = {}
aruco = {}

for size in markersSizes:
    mean = data['code'+ str(size) +'_mean'].dropna().tolist()
    median = data['code'+ str(size) +'_median'].dropna().tolist()
    std = data['code'+ str(size) +'_std'].dropna().tolist()
    qrCodes[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]

   
for size in markersSizes:
    mean = data['aruco'+ str(size) +'_mean'].dropna().tolist()
    median = data['aruco'+ str(size) +'_median'].dropna().tolist()
    std = data['aruco'+ str(size) +'_std'].dropna().tolist()
    aruco[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]



fig, ax = plt.subplots(figsize=(16,10), dpi=300)
plt.xlabel("Distance [mm]", fontsize=14)
plt.ylabel("Mean position error [mm]", fontsize=14)

x = np.array([i for i in range(1,41)])
colors = ['blue', 'orange', 'green', 'purple']
bgcolors = ['white', 'lightgray', 'silver', 'darkgray', 'gray']

i = 0
j = 0

'''
### Wersja połaczone linie        
qrCodeMean = []
qrCodeStd = []

arucoMean = []
arucoStd = []

for color, size in zip(colors,markersSizes):
    for arucoVal, codeVal in itertools.zip_longest(aruco.get(size), qrCodes.get(size)):
        xCode = [j + 8*x +1 for x in range(5)]
        xAruco = [j + 8*x + 2 for x in range(5)]
        if codeVal != None:
            qrCodeMean.append(codeVal[0])
            qrCodeStd.append(codeVal[2])
            #ax.errorbar(x[i], codeVal[0], yerr = codeVal[2], c = color,  fmt='-o', capsize = 3)
            ax.scatter(x[i],codeVal[1], c = 'r',  marker = '_', s=400)
        if arucoVal != None:
            arucoMean.append(arucoVal[0])
            arucoStd.append(arucoVal[2])
            #ax.errorbar(x[i+1], arucoVal[0], yerr = arucoVal[2], c = color,  marker = 's', fillstyle='none', capsize = 3)
            ax.scatter(x[i+1], arucoVal[1], c = 'r',  marker = '_', s=400)
        i+=8
    xCode = xCode[0: len(qrCodeMean)]
    ax.errorbar(xCode, qrCodeMean, yerr = qrCodeStd, c = color,  fmt='-s', capsize = 3)
    xAruco = xAruco[0: len(arucoMean)]
    ax.errorbar(xAruco, arucoMean, yerr = arucoStd, c = color,  fmt = '--s', fillstyle='none', capsize = 3)
    qrCodeMean.clear()
    qrCodeStd.clear()
    arucoMean.clear()
    arucoStd.clear()
    j+=2
    i=j
'''

### Wersja same znaczniki

for color, size in zip(colors,markersSizes):
    for arucoVal, codeVal in itertools.zip_longest(aruco.get(size), qrCodes.get(size)):
        if codeVal != None:
            ax.errorbar(x[i], codeVal[0], yerr = codeVal[2], c = color,  marker = 's', capsize = 3,  ms=10)
            ax.scatter(x[i],codeVal[1], c = 'r',  marker = '_', s=600)
        if arucoVal != None:
            ax.errorbar(x[i+1], arucoVal[0], yerr = arucoVal[2], c = color,  marker = 's', fillstyle='none', capsize = 3,  ms=10)
            ax.scatter(x[i+1], arucoVal[1], c = 'r',  marker = '_', s=600)
        i+=8
   
    j+=2
    i=j


NumAllSamples = 40
SamplesPerColor = 8
dx = NumAllSamples / len(distancesMM)
names  = ['300','500','750','1000', '1250']
valuesForBrackets = [0.136, 0.318, 0.5, 0.6815, 0.8635]
centers = [i*(dx/2) + 0.5 for i in range(1,11,2)]
ax.set_xticks(centers)
ax.set_xticklabels(names)
for i in range(0,5):
    ax.axvspan(i*dx + 0.5, (i+1)*dx + 0.5, facecolor=bgcolors[i], alpha=0.45)
    ax.annotate('', xy=(valuesForBrackets[i], 0.015), xycoords='axes fraction', ha='center', va='bottom', 
               xytext=(valuesForBrackets[i], 0),
                bbox=dict(boxstyle='square', fc='white'),
                arrowprops=dict(arrowstyle='-[, widthB=7.8, lengthB=0.5', lw=1.5))

    
blue_patch = mpatches.Patch(color=colors[0], label='Marker size ~ 75 mm')
orange_patch = mpatches.Patch(color=colors[1], label='Marker size ~ 65 mm')
green_patch = mpatches.Patch(color=colors[2], label='Marker size ~ 37 mm')
red_patch = mpatches.Patch(color=colors[3], label='Marker size ~ 23 mm')
fig.legend(handles=[blue_patch, orange_patch, green_patch, red_patch] , loc = 'center', bbox_to_anchor=(0.80,0.02)).set_title("Markers")

circleMEANAruco = plt.plot([],[], marker="s", ms=10, ls="", fillstyle='none', color='black', label='Mean with std - ArUco marker')[0]
circleMEANCode = plt.plot([],[], marker="s", ms=10, ls="",  color='black', label='Mean with std - QR Code')[0]
crossMEDIAN = plt.plot([],[], marker="_", ms=10, ls="", color='red', label='Median')[0]
fig.legend(handles=[circleMEANAruco, circleMEANCode , crossMEDIAN] , loc = 'center', bbox_to_anchor=(0.22,0.02))

D30cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[0],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 300 mm') 
D50cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[1],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 500 mm') 
D75cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[2],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 750 mm')  
D100cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[3],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1000 mm')  
D125cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[4],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1250 mm') 
fig.legend(handles=[D30cm, D50cm, D75cm, D100cm, D125cm] , loc = 'center',bbox_to_anchor=(0.52,0.02),  ncol=2).set_title("The same background color means that the measurments were made from the same distance:")

