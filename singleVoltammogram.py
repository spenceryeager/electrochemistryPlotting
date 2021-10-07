import numpy as np
from tkinter import *
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300
root = Tk()
root.withdraw()


def main():
    # only works for a single file
    filepath = sd.askstring(title="Enter directory path",
                            prompt="Enter the path to the directory containing file of interest")
    working_file = fd.askopenfilename(
        title="Select file for plotting", initialdir=filepath)
    cv = pd.read_csv(working_file, skiprows=rowskip(working_file))
    if len(cv.columns) == 2:
        j = np.array(cv[' Current/A'])
        j = j / 0.71

    if len(cv.columns) == 3:
        j = np.array(cv[' i2/A'])
    V = np.array(cv['Potential/V'])
    plot(V, j)


# def column_comp(comp_val, col_list):
#     boolean_list = []
#     for i in col_list:
#         boolean_list.append(i == comp_val)
#     print(boolean_list)


def rowskip(working_file):
    file = open(working_file, 'r')
    count = 0
    for line in file:
        if (line.strip() == "Potential/V, i1/A, i2/A") or (line.strip() == 'Potential/V, Current/A'):
            row = count
        count += 1
    return row


def plot(potential, current):
    plt.rc('font', size=12)
    plt.figure(figsize=(10,6))
    plt.plot(potential, current, color='red', linewidth=1)
    plt.xlim(max(potential + 0.1), min(potential - 0.1))
    plt.xlabel('Potential (V)')
    plt.ylabel('Current Density (A/cm$^{2}$)')
    plt.show()
    # print(cv)


if __name__ == '__main__':
    main()
