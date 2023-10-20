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

    # instrument = "ch instruments"
    instrument = "gamry"

    electrode_area = 0.049 #cm2
    reference_electrode = 'Potential (V) vs. Ag Wire'
    reference_correction = 0
    working_file = r"R:\Spencer Yeager\data\NiOx_Project\2023\10_Oct\03Oct2023_NiOx-Untreated-Iodide\NiOx-Iodide-Echem\Untreatee\ag-wire-calib\Ag-Wire-Fc-Calib-Before.DTA"
    save_fig_filepath= r"R:\Spencer Yeager\data\NiOx_Project\2023\10_Oct\03Oct2023_NiOx-Untreated-Iodide\NiOx-Iodide-Echem\Untreatee\figures"
    save_fig = os.path.join(save_fig_filepath, "fc_calib_before.svg")
    # print(save_fig)

    if instrument == "ch instruments":
        cv = pd.read_csv(working_file, skiprows=rowskip(working_file))
        if len(cv.columns) == 2:
            j = np.array(cv[' Current/A'])
            j = j / electrode_area
            j = j * (10**6)

        if len(cv.columns) == 3:
            j = np.array(cv[' i2/A'])
        V = np.array(cv['Potential/V'])
        plot(V, j, reference_electrode, reference_correction, save_fig)
   
    elif instrument == "gamry":
        cv = pd.read_csv(working_file, skiprows=60, skipfooter=4, sep='\t')
        print(cv.head())
        j = np.array(cv['Im'])
    
        print(j)
        # j = j / electrode_area
        # j = j * (10**6)
        # V = np.array(cv['Vf'])
        # plot(V, j, reference_electrode, reference_correction, save_fig)


    
    else:
        print('this will never happen')


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


def plot(potential, current, reference_electrode, reference_correction, save_fig):
    fontsize = 40
    mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    plt.rc('font', size=12)
    ax.plot(potential - reference_correction, current, color='black', linewidth=7)
    ax.set_xlim(max(potential + 0.1 - reference_correction), min(potential - 0.1 - reference_correction))
    ax.set_xlabel(reference_electrode)
    ax.set_ylabel('Current Density ($\mu$A/cm$^{2}$)')
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
    
    
    plt.savefig(save_fig, tight_layout=True)
    plt.show()

    # print(cv)


if __name__ == '__main__':
    main()
