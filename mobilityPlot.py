import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
import scipy.integrate as integrate
import os
from plotLoading.fileSelect import select

# Author: Spencer Yeager, University of Arizona, Aug 2021
# This program goes hand in hand with the holeDensity.py and conductivityPlot.py program
# This will create mobility plots from corresponding conductivity and and hole density plots.
# Additionally it will save the calculated values for plotting in other software.

root = Tk()
root.withdraw()

mb.showinfo(title="Select Data", message="Select data folder then file containing energy and DOS data")

workingdir, workingfile = select()
# interval = sd.askfloat("Data Intervals", 'Enter data intervals')

# for debugging
# workingdir = '/home/spenceryeager/Documents/python_bits/holeDensity'
# workingfile='/home/spenceryeager/Documents/python_bits/holeDensity/test.csv'
# interval = 0.001

# file saving
vals = {'Energy wrt Vac (eV)': dos['Energy wrt Vac (eV)'][1:], 'Hole Density (cm^-3)': hole, 'Log(Hole Density (cm^-3))':
        holelog}
calc_vals = pd.DataFrame(data=vals)


def makefile(workingdir, newdir, filename):
    path = os.path.join(workingdir, newdir)
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)
    filepath = os.path.join(path, filename)
    return filepath


calc_vals.to_csv(makefile(workingdir, "calculated_holes", "calculated_holes.csv"))

# plot
plt.plot(dos['Energy wrt Vac (eV)'][1:], holelog)
plt.xlim(max(dos['Energy wrt Vac (eV)'][1:]), min(dos['Energy wrt Vac (eV)'][1:]))
plt.xlabel("Energy w.r.t Vacuum (eV)")
plt.ylabel(r"log Hole Density (cm$^{-3}$)")
plt.show()
