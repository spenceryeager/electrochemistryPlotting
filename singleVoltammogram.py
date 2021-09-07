import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['figure.dpi'] = 300
rcParams['savefig.dpi'] = 300
import os
import tkinter.filedialog as fd
import numpy as np


def main():
    #only works for a single file
    working_file = fd.askopenfilename(initialdir="enter working directory")
    cv = pd.read_csv(working_file, skiprows=rowskip(workingfile))
    j = np.array(cv[' Current/A'])
    j = j / 0.71
    V = np.array(cv['Potential/V'])
    plot(V, j)

# opening file, and counting how many lines are present until headers
def rowskip(workingfile):
    file = open(working_file, 'r')
    count = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count
        count += 1
    return row


def plot(potential, current):
    plt.rc('font', size=12)
    plt.plot(cv['Potential/V'], j, color='red')
    plt.xlim(max(cv['Potential/V'] + 0.1), min(cv['Potential/V'] - 0.1))
    plt.xlabel('Potential (V)')
    plt.ylabel('Current Density (A/cm$^{2}$)')
    plt.show()
    # print(cv)

if __name__ == '__main__':
    main()
