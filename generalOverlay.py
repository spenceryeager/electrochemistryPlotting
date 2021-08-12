import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
from plotFunctions.plotSettings import plotSettings
from fileSelect import select
from tkinter import *


# this program makes a general plotting. It may need to be rewritten to accomodate certain files.
root = Tk()
root.withdraw()


number = sd.askinteger(title="Enter value", prompt="How many datasets are being plotted?")
if number == None:
    quit()

workingdir = fd.askdirectory()

colors = plt.cm.brg(np.linspace(0, 1, number))

header = sd.askstring("Enter header", "enter the header titles where the data begins")

xhead = sd.askstring("Enter x header", "Enter the header of the X values")
yhead = sd.askstring("Enter y header", "Enter the header of the Y values to be used")

count = 0
while count < number:
    workingfile = fd.askopenfilename(initialdir=workingdir)
    label = sd.askstring("Enter label", "Enter a legend label")

    # opening file, and counting how many lines are present until headers


    def rowskip(file):  # cleans up all the extra stuff in the header
        file = open(workingfile, 'r')
        index = 0
        for line in file:
            if line.strip() == header:
                row = index
            index += 1
        return row


    df = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    plt.plot(df[xhead], df[yhead])
    count +=1

width, height, yax, xax, title, fontsize = plotSettings()
plt.figure(figsize=(width, height))
plt.xlabel(xax)
plt.ylabel(yax)
plt.title(title)
plt.rc("font", size=fontsize)

plt.show()
