import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import *
import numpy as np

root = Tk()
root.withdraw()

number = sd.askinteger(title="Enter value", prompt="How many voltammograms are you plotting?")
if number == None:
    quit()
workingdir = fd.askdirectory(initialdir="enter folder here", title="Select data folder")
if workingdir == ():
    quit()



plt.rc('font', size=15)
plt.figure(figsize=(11,8))
plt.xlabel('Potential (V)')
plt.ylabel('Current (A)')

# setting up multi colors based on how many voltammograms are being plotted
colors = plt.cm.viridis(np.linspace(0, 1, number))

count = 0
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
    plt.plot(cv['Potential/V'], cv[' Current/A'], color=colors[count], label=label)
    plt.xlim(max(cv['Potential/V'] + 0.1), min(cv['Potential/V'] - 0.1))
    count += 1
legendChoice = mb.askyesno("Display legend?", "Display legend?")
titleChoice = mb.askyesno("Display title?", "Display title?")
if legendChoice:
    plt.legend(loc='best')

if titleChoice:
    title = sd.askstring("Enter title", "Enter a title for the graph")
    plt.title(title)
plt.show()
# # print(cv)