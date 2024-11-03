# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:52:29 2023

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

CSVPath  = r'D:\Kamery_[WYNIKI]\PracaMagisterska_[AGH]\Charts\arucoCenters_MIXKATOW.csv'
data = pd.read_csv(CSVPath)

distancesMM = data['distance'].tolist()
markersSizes = [75,65,37,23]

centersWPROST = {}
centersDAL = {}
centersBLIZ = {}

for size in markersSizes:
    mean = data['center'+ str(size) +'_mean'].dropna().tolist()
    median = data['center'+ str(size) +'_median'].dropna().tolist()
    std = data['center'+ str(size) +'_std'].dropna().tolist()
    centersWPROST[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]

for size in markersSizes:
    mean = data['center'+ str(size) +'_mean_DAL'].dropna().tolist()
    median = data['center'+ str(size) +'_median_DAL'].dropna().tolist()
    std = data['center'+ str(size) +'_std_DAL'].dropna().tolist()
    centersDAL[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]

for size in markersSizes:
    mean = data['center'+ str(size) +'_mean_BLIZ'].dropna().tolist()
    median = data['center'+ str(size) +'_median_BLIZ'].dropna().tolist()
    std = data['center'+ str(size) +'_std_BLIZ'].dropna().tolist()
    centersBLIZ[size] = [ [i,j,k] for i, j, k in zip(mean, median, std)]
    

fig = plt.figure(figsize=(16,8), dpi=300)
gs = fig.add_gridspec(1, 3, hspace=0, wspace=0.05)
ax1, ax2, ax3 = gs.subplots(sharex=False, sharey=True)
axes = [ax1, ax2, ax3]
ax1.set_ylabel('Mean position error [mm]', fontsize=14)
fig.supxlabel('Distance [mm] with the corresponding φ angle [°]', fontsize=14)


x = np.array([i for i in range(1,61)])
colors = ['blue', 'orange', 'green', 'purple']
bgcolors = ['white', 'lightgray', 'silver', 'darkgray', 'gray']
i = 0
j = 0


'''
### Wersja połaczone linie,        
qrCodeMean = []
qrCodeStd = []

arucoMean = []
arucoStd = []

for color, size in zip(colors,markersSizes):
    for arucoVal, codeVal in itertools.zip_longest(corners.get(size), centers.get(size)):
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
    ax.errorbar(xCode, qrCodeMean, yerr = qrCodeStd, c = color,  fmt='-o', capsize = 3)
    xAruco = xAruco[0: len(arucoMean)]
    ax.errorbar(xAruco, arucoMean, yerr = arucoStd, c = color,  fmt = '--s', fillstyle='none', capsize = 3)
    qrCodeMean.clear()
    qrCodeStd.clear()
    arucoMean.clear()
    arucoStd.clear()
    j+=2
    i=j
    
    
'''

'''
### Na jednym wykresie wszystko
for color, size in zip(colors,markersSizes):
    for wprost, dal, bliz in itertools.zip_longest(centersWPROST.get(size), centersDAL.get(size), centersBLIZ.get(size)):
        if wprost != None:
            ax.errorbar(x[i], wprost[0], yerr = wprost[2], c = color,  marker = 'o',  capsize = 3)
            ax.scatter(x[i],wprost[1], c = 'r',  marker = '_', s=400)
        if dal != None:
            ax.errorbar(x[i+1], dal[0], yerr = dal[2], c = color,  marker = 's', capsize = 3)
            ax.scatter(x[i+1], dal[1], c = 'r',  marker = '_', s=400)
        if bliz != None:
            ax.errorbar(x[i+2], bliz[0], yerr = bliz[2], c = color,  marker = 'o', fillstyle='none', capsize = 3)
            ax.scatter(x[i+2], bliz[1], c = 'r',  marker = '_', s=400)
        i+=12
   
    j+=3
    i=j

'''
### 3 osobne wykresy, niepołączone znaczniki

Nmax = 21
dx = (Nmax-1) / 5
x = np.array([i for i in range(1,Nmax)])
for color, size in zip(colors,markersSizes):
    for wprost, dal, bliz in itertools.zip_longest(centersWPROST.get(size), centersDAL.get(size), centersBLIZ.get(size)):
        if wprost != None:
            ax1.errorbar(x[i], wprost[0], yerr = wprost[2], c = color,  marker = 'o',  capsize = 3, ms=8)
            ax1.scatter(x[i],wprost[1], c = 'r',  marker = '_', s=600)
        if bliz != None:
            ax2.errorbar(x[i], bliz[0], yerr = bliz[2], c = color,  marker = 'o', capsize = 3, ms=8)
            ax2.scatter(x[i], bliz[1], c = 'r',  marker = '_', s=600)
        if dal != None:
            ax3.errorbar(x[i], dal[0], yerr = dal[2], c = color,  marker = 'o', capsize = 3, ms=8)
            ax3.scatter(x[i], dal[1], c = 'r',  marker = '_', s=600)
        i+=4
    j+=1
    i=j

centers = [i*(dx/2) + 0.5 for i in range(1,11,2)]
valuesForBrackets = [0.135, 0.318, 0.5, 0.683, 0.865]
firstValue = 0.135 
xticksaxes = [['300 \n φ ~ 90','500 \n φ ~ 90','750 \n φ ~ 90','1000 \n φ ~ 90', '1250 \n φ ~ 90'],  ['300 \n φ ~ 75','500 \n φ ~ 70','750 \n φ ~ 80','1000 \n φ ~ 60', '1250 \n φ ~ 45'], ['300\n φ ~ 75','500 \n φ ~ 55','750 \n φ ~ 40','1000 \n φ ~ 30', '1250 \n φ ~ 20']]
for ax, names in zip(axes, xticksaxes):    
    ax.set_xticks(centers)
    ax.set_xticklabels(names)
    for i in range(0,5):
        ax.axvspan(i*dx + 0.5, (i+1)*dx + 0.5, facecolor=bgcolors[i], alpha=0.45)
        ax.annotate('', xy=(valuesForBrackets[i], 0.015), xycoords='axes fraction', ha='center', va='bottom', 
                   xytext=(valuesForBrackets[i], 0),
                    bbox=dict(boxstyle='square', fc='white'),
                    arrowprops=dict(arrowstyle='-[, widthB=2.5, lengthB=0.5', lw=1.5))



blue_patch = mpatches.Patch(color=colors[0], label='Marker size ~ 75 mm')
orange_patch = mpatches.Patch(color=colors[1], label='Marker size ~ 65 mm')
green_patch = mpatches.Patch(color=colors[2], label='Marker size ~ 37 mm')
red_patch = mpatches.Patch(color=colors[3], label='Marker size ~ 23 mm')
fig.legend(handles=[blue_patch, orange_patch, green_patch, red_patch] , loc = 'center', bbox_to_anchor=(0.80,-0.065)).set_title("Markers")

circleMEANCode = plt.plot([],[], marker="o", ms=10, ls="",  color='black', label='Mean with std - centers of ArUco marker')[0]
crossMEDIAN = plt.plot([],[], marker="_", ms=10, ls="", color='red', label='Median')[0]
fig.legend(handles=[ circleMEANCode , crossMEDIAN] , loc = 'center', bbox_to_anchor=(0.2,-0.065))

D30cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[0],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 300 mm') 
D50cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[1],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 500 mm') 
D75cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[2],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 750 mm')  
D100cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[3],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1000 mm')  
D125cm = patches.Rectangle((0,0),1,1,facecolor=bgcolors[4],alpha=0.45, edgecolor='black', linewidth=1.0, label='Distance = 1250 mm') 
fig.legend(handles=[D30cm, D50cm, D75cm, D100cm, D125cm] , loc = 'center',bbox_to_anchor=(0.52,-0.065),  ncol=2).set_title("The same background color means that the measurments were made from the same distance:")


