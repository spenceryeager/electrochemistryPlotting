# Solid state conductivity data processing using the LabVIEW program I wrote for a Keithley 2400

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def main():
    filepath = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\data\13June2025_PBTTT_SSConductivity\Device3\channel2.csv"
    fileload = pd.read_csv(filepath, sep='\t')

    ######################
    ### Fill this out! ###
    ######################
    film_thickness = 27 # nm, will convert later
    channel_width = 30 # mm, from Ossila website, will convert later
    channel_length = 75 # um, from Ossila website, will convert later
    show_fit_plot = True
    ######################

    area, length = unit_conversion(film_thickness, channel_width, channel_length)

    slope, intercept, r_sq = get_slope(fileload['Voltage (V)'], fileload['Current (A)'], plot=show_fit_plot)

    resistivity = slope * (area / length)
    resistivity = resistivity * 100
    print(resistivity)
    conductivity = resistivity ** -1
    print(conductivity, "S cm^-1")


def get_slope(voltage, current, plot):
    vals = stats.linregress(current, voltage)

    if plot:

        fig, ax = plt.subplots()
        ax.plot(current, voltage, color='black')
        linear_line = (vals[0]*current) + vals[1]
        ax.plot(current, linear_line, color='red')
        ax.set_xlabel("Current (A)")
        ax.set_ylabel('Voltage (V)')
        ax.set_title("Check fit")
        plt.show()

    return vals[0], vals[1], vals[2]


def unit_conversion(film_thickness, channel_width, channel_length):
    # converting all to meters because why not
    film_thickness = film_thickness * (10**-9)
    channel_width = channel_width * (10**-3)
    channel_length = channel_length * (10**-6)

    area = channel_width * film_thickness # m^2
    return area, channel_length



if __name__ == "__main__":
    main()
