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
import tkinter.messagebox as mb
from tkinter import *
import numpy as np

root = Tk()
root.withdraw()


def main():
    electrode_area = 0.049 #cm2
    ref_electrode = "Potential vs. Ag Wire"

    number = sd.askinteger(title="Enter value", prompt="How many voltammograms are you plotting?")
    if number == None:
        quit()
    workingdir = r"R:\Spencer Yeager\data\NiOx_Project\2023\08_Aug\17Aug2023_Ag-Wire-Ref-Test"
    if workingdir == ():
        quit()



    # plt.rc('font', size=30)
    # plt.figure(figsize=(11,8))
    # plt.xlabel('Potential (V)')
    # plt.ylabel(r'Current Density (A cm$^{-2}$)')

    # setting up multi colors based on how many voltammograms are being plotted
    colors = plt.cm.jet(np.linspace(0, 1, number))

    count = 0
    while count < number:
        workingfile = fd.askopenfilename(initialdir=workingdir)
        label = sd.askstring("Enter label", "Enter a legend label")

        # opening file, and counting how many lines are present until headers


        def rowskip(file):  # cleans up all the extra stuff in the header
            file = open(workingfile, 'r')
            index = 0
            for line in file:
                if line.strip() == "Potential/V, Current/A":
                    row = index
                index += 1
            return row


        cv = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
        current_array = np.array(cv[' Current/A'])
        current_array = current_array / electrode_area

        fontsize = 40
        mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
        fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)

        ax.plot(cv['Potential/V'], current_array, color=colors[count], label=label)
        ax.set_xlim(max(cv['Potential/V'] + 0.1), min(cv['Potential/V'] - 0.1))
        count += 1
    
    # plot formatting
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)

    ax.set_xlabel(ref_electrode)
    ax.set_ylabel("Current Density ($\mu$A cm$^{-2}$)")

    legendChoice = mb.askyesno("Display legend?", "Display legend?")
    titleChoice = mb.askyesno("Display title?", "Display title?")
    if legendChoice:
        plt.legend(loc='best')

    if titleChoice:
        title = sd.askstring("Enter title", "Enter a title for the graph")
        plt.title(title)
    plt.show()
    # # print(cv)

    if __name__ == "__main__":
        main()
