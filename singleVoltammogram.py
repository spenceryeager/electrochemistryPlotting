import numpy as np
from tkinter import *
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
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
    # filepath = sd.askstring(title="Enter directory path",
    #                         prompt="Enter the path to the directory containing file of interest")
    # working_file = fd.askopenfilename(
    #     title="Select file for plotting", initialdir=filepath)
    electrode_area = 0.049 #cm2
    working_file = r"R:\Spencer Yeager\data\NiOx_Project\2023\08_Aug\17Aug2023_Ag-Wire-Ref-Test\ag-wire-fc-after-run1.csv"
    save_fig_filepath= r"R:\Spencer Yeager\group_meetings\general_group_meetings\2023\16Aug2023"
    save_fig = os.path.join(save_fig_filepath, "AgWire-Fc-After.svg")
    # print(save_fig)
    cv = pd.read_csv(working_file, skiprows=rowskip(working_file))
    if len(cv.columns) == 2:
        j = np.array(cv[' Current/A'])
        j = j / electrode_area
        j = j * (10**6)

    if len(cv.columns) == 3:
        j = np.array(cv[' i2/A'])
    V = np.array(cv['Potential/V'])
    plot(V, j, save_fig)


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


def plot(potential, current, save_fig):
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    plt.rc('font', size=12)
    ax.plot(potential, current, color='red', linewidth=7)
    ax.set_xlim(max(potential + 0.1), min(potential - 0.1))
    ax.set_xlabel('Potential (V) vs. Ag/AgCl')
    ax.set_ylabel('Current Density ($\mu$A/cm$^{2}$)')
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    
    
    plt.savefig(save_fig)
    plt.show()

    # print(cv)


if __name__ == '__main__':
    main()
