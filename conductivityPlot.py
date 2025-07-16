import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
# import tkinter.filedialog as fd
# import tkinter.simpledialog as sd
# import tkinter.messagebox as mb
# from tkinter import *
# from plotLoading import fileSelect
import os


# Author: Spencer Yeager, University of Arizona, Aug 2021
# Updated July 2025
# Use this program to generate a conductivity plot from measured current/voltage data from a CH Instruments 
# To understand what is required in this program, refer to the wikipedia page on the relationship between
# current and conductivity:
# https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity


def main():
    #########################
    #### FILL THIS OUT ######
    workingfile = r"D:\10July2025_insitu_conductivity_P3HT_PBTTT\p3ht\run1.csv"
    savedir = r"D:\10July2025_insitu_conductivity_P3HT_PBTTT\p3ht\worked_up"
    savename = r"p3ht_conductivity"
    
    thickness = (27 * (10 **-7)) # cm, film thickness
    width = 3.0 # cm, part of Ossila substrates
    area = thickness * width
    length = 0.005 # cm, 50 um to cm, part of Ossila substrates

    #########################
    #########################

    data = fileloading(workingfile) # loading data
    conductivity_df = conductivity_calculation(data, area, length) # calculating conductivity
    conductivity_df.to_csv(os.path.join(savedir,savename+".csv"))
    fig, ax = plt.subplots()
    ax.plot(conductivity_df['Potential/V'], conductivity_df['Conductivity (S/cm)'])
    plt.show()


def fileloading(workingfile):
    data_load = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    maximum_potential = data_load["Potential/V"].max()
    maximum_potential_loc = data_load["Potential/V"].idxmax()

    minimum_potential = data_load["Potential/V"].min()
    minimum_potential_loc = data_load['Potential/V'].idxmin()


    if minimum_potential_loc == 0:
        # this is a simple way to determine if the sample set is p-type or n-type. Minimum potential location should not be the starting potential
        data_subset = data_load[0:maximum_potential_loc+1]
    else:
        data_subset = data_load[0:minimum_potential_loc+1]


    return data_subset


def rowskip(workingfile):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, i1/A, i2/A":
            row = count1
        count1 += 1
    return row



def conductivity_calculation(data, area, length):
    potentials = [np.nan, np.nan]
    slope = [np.nan, np.nan]
    intercept = [np.nan, np.nan]
    rsq = [np.nan, np.nan]
    final_index = data.index[-1]
    lower_index = 0
    upper_index = 2


    while upper_index <= final_index: # I am taking three values and doing a rolling linear fit to get the slope.
        data_slice = data.loc[lower_index:upper_index]
        fit = get_slope(data_slice)
        slope.append(fit[0])
        intercept.append(fit[1])
        rsq.append(np.square(fit[2]))
        lower_index += 1
        upper_index += 1


    data['Slope'] = slope
    data['Intercept'] = intercept
    data['R Squared'] = rsq

    slope_vals = data['Slope']
    resistivity = (slope_vals * area) / length
    conductivity = np.reciprocal(resistivity)
    data['Resisitivity (ohm cm)'] = resistivity
    data['Conductivity (S/cm)'] = conductivity
    return data


def get_slope(linear_region):
    try:
        fit = stats.linregress(linear_region[' i2/A'], linear_region['Potential/V'])
    except ValueError:
        fit = [np.inf, np.nan, np.nan]
    return fit


if __name__ == "__main__":
    main()
