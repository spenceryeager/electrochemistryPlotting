# I've seemingly lost my past spectra map program. It might've been made before I knew how to use git. Nevertheless, here is a new version.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def main():
    # fill all this out
    spec_file = r"G:\RDrive_Backup\Spencer Yeager\papers\paper2_GATech_Collab_P3HT-PBTTT\electrochemistry_data\DOS_Films_Comparisons\15Aug2025_StaticDynamic_PBTTT_P3HT_IBTDT\Spectroscopy\IDTBT\IDTBT_Static_Dynamic_SEC_10mV_Run1.TXT"
    initial_voltage = -0.4
    final_voltage = 1.5
    
   
    spec_file_load = pd.read_csv(spec_file, sep='\t', skiprows=5)

    # I want to get the very last spectrum. This is going to get my minimum and maximum abs values over the set range!
    final_col = spec_file_load.iloc[:,-1:].columns[0]
    abs_subset = spec_file_load[final_col].loc[(spec_file_load['WL-Time'] > 400)]
    min_val = abs_subset.min()
    max_val = abs_subset.max()

    # cleaning up df for plotting
    wavelengths = spec_file_load['WL-Time']
    spec_file_load.drop('WL-Time', axis='columns', inplace=True)
    col_no = len(spec_file_load.columns)
    spec_file_load = spec_file_load.T
    potential_vals = np.linspace(initial_voltage, final_voltage, col_no)


    # my x and y will be x = wavelength, y = potential
    xlamb, ypot = np.meshgrid(wavelengths, potential_vals)


    fig, ax = plt.subplots()
    ax.contourf(xlamb, ypot, spec_file_load, levels=200, vmin=min_val, vmax=max_val)
    ax.set_xlim(400,1100)
    plt.show()
# # def make_map

if __name__ == '__main__':
    main()