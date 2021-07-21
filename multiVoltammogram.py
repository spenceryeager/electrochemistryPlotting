import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import *

root = Tk()
root.withdraw()

number = sd.askinteger(title="Enter value", prompt="How many voltammograms are you plotting?")
if number == None:
    quit()
workingdir = fd.askdirectory(initialdir="/home/spenceryeager/Documents/python_bits/voltammetry", title="Select data folder")
if workingdir == ():
    quit()


count = 0
plt.rc('font', size=15)
plt.figure(figsize=(11,8))
plt.xlabel('Potential (V)')
plt.ylabel('Current (A)')

while count < number:
    workingfile = fd.askopenfilename(initialdir=workingdir)
    label = sd.askstring("Enter label", "Enter a legend label")

    # opening file, and counting how many lines are present until headers
    file = open(workingfile, 'r')
    count2 = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count2
        count2 += 1

    cv = pd.read_csv(workingfile, skiprows=row)
    plt.plot(cv['Potential/V'], cv[' Current/A'], color='red', label=label)
    plt.xlim(max(cv['Potential/V'] + 0.1), min(cv['Potential/V'] - 0.1))
    count += 1
legendChoice = mb.askyesno("Display legend?", "Display legend?")
if legendChoice:
    plt.legend(loc='best')
plt.show()
# # print(cv)