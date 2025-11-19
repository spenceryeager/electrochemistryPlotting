import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
import scipy.integrate as integrate
import os

# Author: Spencer Yeager, University of Arizona, Aug 2021
# This program goes hand in hand with the densityOfStates.py program
# This will read the output from that file and turn it into a hole density plot.

def main():
    file_location = r'E:\RDrive_Backup\Spencer Yeager\papers\paper8_UK_Megan_N2200_Paper\worked_up_data\amorphous_N2200_reduction_dos.csv'
    file_load = pd.read_csv(file_location)
    carriers = carrier_density(file_load)


def carrier_density(dos_file):
    print(dos_file.head())
    return 0


if __name__ == "__main__":
    main()

# root = Tk()
# root.withdraw()

# mb.showinfo(title="Select Data", message="Select data folder then file containing energy and DOS data")


# def askdir():
#     workingdir = fd.askdirectory(initialdir="/run/user/1000/gvfs/sftp:host=file.engr.arizona.edu/Research/Ratcliff/Spencer/data/2021/08_Aug/08Aug2021/cv/tfsi")
#     if workingdir == ():
#         quit()
#     return workingdir


# def askfile(workingdir):
#     file = fd.askopenfilename(initialdir=workingdir)
#     if file == ():
#         quit()
#     return file


# workingdir = askdir()
# workingfile = askfile(workingdir)
# interval = sd.askfloat("Data Intervals", 'Enter data intervals')

# # for debugging
# # workingdir = '/home/spenceryeager/Documents/python_bits/holeDensity'
# # workingfile='/home/spenceryeager/Documents/python_bits/holeDensity/test.csv'
# # interval = 0.001

# dos = pd.read_csv(workingfile, usecols=[1, 2])
# hole = np.array(integrate.cumulative_trapezoid(dos['DOS (states/(eV cm^3))'], dos['Energy wrt Vac (eV)'], interval))
# hole = np.abs(hole)
# holelog = np.log10(hole)

# # file saving
# vals = {'Energy wrt Vac (eV)': dos['Energy wrt Vac (eV)'][1:], 'Hole Density (cm^-3)': hole, 'Log(Hole Density (cm^-3))':
#         holelog}
# calc_vals = pd.DataFrame(data=vals)


# def makefile(workingdir, newdir, filename):
#     path = os.path.join(workingdir, newdir)
#     isdir = os.path.isdir(path)
#     if not isdir:
#         os.mkdir(path)
#     filepath = os.path.join(path, filename)
#     return filepath


# calc_vals.to_csv(makefile(workingdir, "calculated_holes", "calculated_holes.csv"))

# # plot
# plt.plot(dos['Energy wrt Vac (eV)'][1:], holelog)
# plt.xlim(max(dos['Energy wrt Vac (eV)'][1:]), min(dos['Energy wrt Vac (eV)'][1:]))
# plt.xlabel("Energy w.r.t Vacuum (eV)")
# plt.ylabel(r"log Hole Density (cm$^{-3}$)")
# plt.show()
