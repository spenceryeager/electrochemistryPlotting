import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
import scipy.integrate as integrate
import os

# Author: Spencer Yeager, University of Arizona, Aug 2021
# This program goes hand in hand with the densityOfStates.py program
# This will read the output from that file and turn it into a hole density plot.

def main():
    ####################
    ###FILL THIS OUT!###
    ####################
    file_location = r'E:\RDrive_Backup\Spencer Yeager\papers\paper8_UK_Megan_N2200_Paper\worked_up_data\amorphous_N2200_reduction_dos.csv'
    file_save_location = r'E:\RDrive_Backup\Spencer Yeager\papers\paper8_UK_Megan_N2200_Paper\worked_up_data'
    file_name = r'n2200_more_amorphous_carrier_density_calc' # no need for file extension
    ####################

    file_load = pd.read_csv(file_location)
    carriers = carrier_density(file_load)
    filesave(carriers, file_save_location, file_name)


def carrier_density(dos_file):
    carrier_amount = integrate.cumulative_trapezoid(dos_file['DOS(E) (states / eV cm3)'], dos_file['Energy (eV)'])
    carrier_amount = np.insert(carrier_amount, obj=0, values=np.array(0)) # adding a zero at the beginning to compensate for the dropped value in integration. Could make this NaN, but ultimately I think it's fine
    log_carrier = np.log10(carrier_amount)
    dos_file.insert(4, 'log10 Carriers (carriers / cm)', log_carrier)
    dos_file.insert(4, 'Carriers (carriers / cm)', carrier_amount)
    return dos_file    


def filesave(data, file_save_location, filename):
    data.to_csv(os.path.join(file_save_location, filename + ".csv"), index=False)


if __name__ == "__main__":
    main()
