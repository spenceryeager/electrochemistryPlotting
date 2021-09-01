import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
import scipy.constants as constant
import os
from plotLoading.fileSelect import *

# Author: Spencer Yeager, University of Arizona, Aug 2021
# This program goes hand in hand with the holeDensity.py and conductivityPlot.py program
# This will create mobility plots from corresponding conductivity and and hole density plots.
# Additionally it will save the calculated values for plotting in other software.

#01-Sep-2021, this program is a bit sloppy. I hope to have time in the future to make it look a little better.

root = Tk()
root.withdraw()

mb.showinfo(title="Select Data", message="Select data folder then file containing energy and hole data")
workingdir, workingfile = select()
# #debugging:
# workingfile = "/home/spenceryeager/Documents/calculations/mobility/calculated_holes.csv"
hole = pd.read_csv(workingfile, usecols=[1, 2])

mb.showinfo(title="Select Data", message="Select data file containing conductivity data")
workingfile = singleFileSelect(workingdir)
#debugging:
# workingfile = '/home/spenceryeager/Documents/calculations/mobility/clo4_calculated_conductivity.csv'
cond = pd.read_csv(workingfile, usecols=[5, 6])


# eventually remove this - but need to convert energy in conductivity to negative.
cond_ev = np.array(cond['Energy wrt Vac (eV)'])
cond_ev = cond_ev * -1
cond_values = np.array(cond['Conductivity (S/cm)'])
hole_ev = np.array(hole['Energy wrt Vac (eV)'])
hole_number = np.array(hole['Hole Density (cm^-3)'])

print(len(cond_ev), len(hole_ev))

count = 0
for i in cond_ev:
    if i == hole_ev[0]:
        position = count
    count +=1

cond_ev = cond_ev[position:]
cond_values = cond_values[position:]

mobility = cond_values / (hole_number * constant.elementary_charge)

print(mobility)

# file saving
vals = {'Energy wrt Vac (eV)': hole_ev, 'Mobility (cm^2 V^-1 s^-1)': mobility}
calc_vals = pd.DataFrame(data=vals)


def makefile(workingdir, newdir, filename):
    path = os.path.join(workingdir, newdir)
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)
    filepath = os.path.join(path, filename)
    return filepath


calc_vals.to_csv(makefile(workingdir, "calculated_mobility", "calculated_mobility.csv"))

# plot
plt.plot(hole_ev, mobility)
plt.xlim(max(hole_ev), min(hole_ev))
plt.xlabel("Energy w.r.t Vacuum (eV)")
plt.ylabel(r"Mobility (cm$^{2}$ V$^{-1}$ s$^{-1}$)")
plt.show()
