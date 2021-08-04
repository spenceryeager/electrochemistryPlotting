import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import *
import os

# Author: Spencer Yeager, University of Arizona, Aug 2021
# Use this program to generate a conductivity plot from measured current/voltage data.
# To understand what is required in this program, refer to the wikipedia page on the relationship between
# current and conductivity:
# https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity

root = Tk()
root.withdraw()

workingdir = fd.askdirectory(initialdir='/home/spenceryeager/Documents/python_bits/conductivityPlot/conductivity')
workingfile = fd.askopenfilename(initialdir=workingdir)
if workingfile == ():
    quit()
highV = sd.askfloat(title='High Potential', prompt="Enter the high potential set")
if highV == None:
    mb.showerror(title="Abort", message="Program aborting")
    quit()
potential_diff = sd.askfloat(title='Potential difference', prompt='Enter the potential difference across channel in V')
if potential_diff == None:
    mb.showerror(title="Abort", message="Program aborting")
    quit()


def rowskip(file):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, i1/A, i2/A":
            row = count1
        count1 += 1
    return row


rawdata = pd.read_csv(workingfile, skiprows=rowskip(workingfile))


def highloc(voltage, highV):
    count = 0
    for i in voltage:
        if i == highV:
            loc = count
        count += 1
    return loc + 1


highPotentialLoc = highloc(rawdata['Potential/V'], highV)
# These following two arrays are where most of the arithmetic will be performed
potential_array = np.array(rawdata['Potential/V'][0:highPotentialLoc])
current_array = np.array(rawdata[' i2/A'][0:highPotentialLoc])

# area is defined as the film thickness * channel width. Film thickness is approximated to be 27 nm
# and length is the total combined width of all channels, which is about 3cm.
# substrate parameters found here: https://www.ossila.com/products/interdigitated-ito-ofet-substrates
# we use 50 um channel length substrates

# spelling these calculations out to really see how it is derived.
thickness = (27 * (10 **-7)) # cm
width = 3.0 # cm
area = thickness * width
length = 0.005 # cm, 50 um to cm.

resistance_array = potential_diff / current_array
resistivity_array = (resistance_array * area) / length
conductivity_array = resistivity_array ** -1
ev_array = potential_array + 4.87

# saving new arrays
# making dictionary of all parameters
allparams = {"Potential (V)": potential_array, "Current (A)": current_array, "Resistance (ohm)": resistance_array,
             "Resistivity (ohm cm)": resistivity_array, "Conductivity (S/cm)": conductivity_array,
             "Energy wrt Vac (eV)": ev_array}
calc_vals = pd.DataFrame(data=allparams)

def makefile(workingdir, newdir, filename):
    path = os.path.join(workingdir, newdir)
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)
    filepath = os.path.join(path, filename)
    return filepath

calc_vals.to_csv(makefile(workingdir, "calculated_values", "calculated_values.csv"))

# plotting
plt.plot(ev_array, conductivity_array, color='red')

titlechoice = mb.askyesno(title="Enter title?", message="Add title?")
title = ''
if titlechoice:
    title = sd.askstring(title='Enter title', prompt="Enter graph title")
plt.title(title)

plt.xlabel("Energy vs. Vacuum")
plt.ylabel("Conductivity (S/cm)")
plt.show()
