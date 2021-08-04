import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
import scipy.constants as constant
import os
# a program to plot and calculate the density of states from a cyclic voltammogram file
# reminder: if working on this a while from now, looking at raw data file will give all parameters asked
# for in the prompts!
root = Tk()
root.withdraw()

workingdir = fd.askdirectory(initialdir="/home/spenceryeager/Documents/python_bits/densityOfStates")
workingfile = fd.askopenfilename(initialdir=workingdir)

highV = sd.askfloat(title='High Potential', prompt="Enter the high potential set")
if highV == None:
    mb.showerror(title="Abort", message="Program aborting")
    quit()

def rowskip(file):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count1
        count1 += 1
    return row


cv = pd.read_csv(workingfile, skiprows=rowskip(workingfile))


def highloc(voltage, highV):
    count = 0
    for i in voltage:
        if i == highV:
            loc = count
            return loc
        count += 1


highPotentialLoc = highloc(cv['Potential/V'], highV)
dos_array = np.array(cv[' Current/A'][0:highPotentialLoc]) # all calculations performed on this array
energy_array = np.array(cv['Potential/V'][0:highPotentialLoc])

default_val = mb.askyesno(title="Default values?", message="Use default values for film thickness (27nm) and working "
                                                           "area (0.71 cm^2)?")
if default_val:
    v = sd.askfloat(title="Scan rate", prompt="Enter the scan rate used in V/s")
    area = 0.71
    d = 27 * (10**-7)

    dos_array = dos_array / area
    dos_array = dos_array / (v * d)
    dos_array = dos_array / (constant.elementary_charge ** 2)
    dos_array = dos_array * constant.physical_constants['electron volt'][0]
    dos_array = np.absolute(dos_array)
    energy_scale = mb.askyesno(title="Energy Scale", message="Use eV energy scale?")

    if energy_scale:
        energy_array = -(energy_array + 4.87)
        ytit = "Energy vs. vacuum (eV)"
    else:
        ytit = "Potential (V)"
else:
    v = sd.askfloat(title="Scan rate", prompt="Enter the scan rate used in V/s")
    area =sd.askfloat(title="Area", prompt="enter the working area on the electrode in cm^2")
    d = sd.askfloat(title="Thickness", prompt="Enter the thickness of the film in nm")
    d = d * (10 ** -7) # conversion to cm
    dos_array = dos_array / area
    dos_array = dos_array / (v * d)
    dos_array = dos_array / (constant.elementary_charge ** 2)
    dos_array = dos_array * constant.physical_constants['electron volt'][0]
    dos_array = np.absolute(dos_array)

# file saving
vals = {"DOS (states/(eV cm^3))": dos_array, "Energy wrt Vac (eV)":energy_array}
calc_vals = pd.DataFrame(data=vals)


def makefile(workingdir, newdir, filename):
    path = os.path.join(workingdir, newdir)
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)
    filepath = os.path.join(path, filename)
    return filepath


calc_vals.to_csv(makefile(workingdir, "calculated_values", "calculated_values.csv"))
# plotting
plt.plot(dos_array, energy_array, color='red')
plt.xlabel(r'Density of States (states eV$^{-1}$ cm$^{-3}$)')
plt.ylabel(ytit)
plt.show()