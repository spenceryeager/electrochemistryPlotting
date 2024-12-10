# this script will let different parameters in outersphere reorganization energy be changed to make nice plots showing reorg vs. parameter changed

import numpy as np
from reorganization_energy import outer_sphere
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
import pandas as pd
import os
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300

def main():
    save_file_dir = r"E:\Electrochemical_Parameters"

    # File that has all of the solvent parameters. I have this on my personal hard drive. Can get these values from literature.
    solvent_parameters_file = r"E:\Electrochemical_Parameters\optical_static_dielectric_constants.csv"
    solvent_parameters_load = pd.read_csv(solvent_parameters_file)

    # outersphere parameters:
    a = 3.66 * 10**-10 # radius of redox probe used, in meters
    ion_radius = 2.69 * 10**-10 # radius of PF6, in meters

    solvent_diameter = (np.cbrt(((solvent_parameters_load['Solvent Volume (cubic nm)'] * (3/4)) / 3.14)) * 2) * 10**-9
    helmholtz_length = (solvent_diameter + ion_radius) * 2
    
    reorg_change = []
    
    val = outer_sphere(a, helmholtz_length, solvent_parameters_load['Static Dielectric'], solvent_parameters_load['Optical Dielectric'])
    reorg_values = pd.DataFrame({'Reorg Energy (eV)':val})
    print(reorg_values)
    saving_dataframe = pd.concat([solvent_parameters_load, reorg_values], axis=1)
    saving_dataframe.to_csv(os.path.join(save_file_dir, "solvent_parameters_with_reorg.csv"))


if __name__ == "__main__":
    main()