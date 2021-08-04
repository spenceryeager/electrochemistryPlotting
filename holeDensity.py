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

root = Tk()
root.withdraw()

# mb.showinfo(title="Select Data", message="Select data folder then file containing energy and DOS data")
# workingdir = fd.askdirectory(initialdir="")
# workingfile = fd.askopenfilename(initialdir=workingdir)
# interval = sd.askfloat("Data Intervals", 'Enter data intervals')
interval = 0.001

workingdir = ''
workingfile=''

dos = pd.read_csv(workingfile, usecols=[1, 2])

# print(dos)

# def DOS(E):
    # return float(dos.loc[dos['Energy wrt Vac (eV)'] == -4.671, 'DOS (states/(eV cm^3))'])

hole = integrate.cumulative_trapezoid(dos['DOS (states/(eV cm^3))'], dos['Energy wrt Vac (eV)'], interval)


