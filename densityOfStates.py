import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
import scipy.constants as constant
# a program to plot and calculate the density of states from a cyclic voltammogram file

root = Tk()
root.withdraw()

workingfile = fd.askopenfilename(initialdir="/home/spenceryeager/Documents/python_bits/densityOfStates")

file = open(workingfile, 'r')
count2 = 0
for line in file:
    if line.strip() == "Potential/V, Current/A":
        row = count2
    count2 += 1

cv = pd.read_csv(workingfile, skiprows=row)

potential_list = []
current_list = []

count = 0
while cv['Potential/V'][count] != 0.900:
    potential_list.append(cv['Potential/V'][count])
    current_list.append(cv[' Current/A'][count])
    count +=1

dos_array = np.array(current_list) # all calculations performed on this array
energy_array = np.array(potential_list)

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

plt.plot(dos_array, energy_array, color='red')
plt.xlabel(r'Density of States (states eV$^{-1}$ cm$^{-3}$)')
plt.ylabel(ytit)
plt.show()