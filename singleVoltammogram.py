import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300
import os
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
from tkinter import *
import numpy as np
root = Tk()
root.withdraw()


def main():
    #only works for a single file
    filepath = sd.askstring(title="Enter directory path", prompt="Enter the path to the directory containing file of interest")
    working_file = fd.askopenfilename(title="Select file for plotting", initialdir=filepath)
    cv = pd.read_csv(working_file, skiprows=rowskip(working_file))
    j = np.array(cv[' Current/A'])
    j = j / 0.71
    V = np.array(cv['Potential/V'])
    plot(V, j)

# opening file, and counting how many lines are present until headers
def rowskip(working_file):
    file = open(working_file, 'r')
    count = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count
        count += 1
    return row


def plot(potential, current):
    plt.rc('font', size=12)
    plt.plot(potential, current, color='red', linewidth=3)
    plt.xlim(max(potential + 0.1), min(potential - 0.1))
    plt.xlabel('Potential (V)')
    plt.ylabel('Current Density (A/cm$^{2}$)')
    plt.show()
    # print(cv)

if __name__ == '__main__':
    main()
