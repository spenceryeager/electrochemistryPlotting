# this script will let different parameters in outersphere reorganization energy be changed to make nice plots showing reorg vs. parameter changed

import numpy as np
from reorganization_energy import outer_sphere
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
import pandas as pd
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300

def main():
    # File that has all of the solvent parameters. I have this on my personal hard drive. Can get these values from literature.
    solvent_parameters_file = r"E:\Electrochemical_Parameters\optical_static_dielectric_constants.csv"
    solvent_parameters_load = pd.read_csv(solvent_parameters_file)

    # outersphere parameters:
    a = 1.66 * 10**-10 # radius of redox probe used, in meters
    ion_radius = 2.69 * 10**-10 # radius of PF6, in meters

    solvent_diameter = (np.cbrt(((solvent_parameters_load['Solvent Volume (cubic nm)'] * (3/4)) / 3.14)) * 2) * 10**-9
    helmholtz_length = solvent_diameter + ion_radius
    print(helmholtz_length)
    # re = (2 * a) # twice the distance from the image charge at the interface to the redox probe. I am assuming this to be twice the distance of the radius (not accounting for solvent shell)
    
    reorg_change = []
    
    val = outer_sphere(a, helmholtz_length, solvent_parameters_load['Static Dielectric'], solvent_parameters_load['Optical Dielectric'])

    print(val)
    # for row in solvent_parameters_load:
    #     print(row)
    #     print('next!')
        # val = outer_sphere(a, re, i, frequency_dielectric)
        # reorg_change.append(val)
    

    # fontsize = 40
    # mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
    # fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    # ax.scatter(static_dielectric, reorg_change, s=200, color='#49006a')
    # ax.set_xlabel("Static Dielectric Constant")
    # ax.set_ylabel("Reorganization Energy (eV)")
    
    # ax.xaxis.labelpad = 5
    # ax.yaxis.labelpad = 5
    # ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    
    
    # for axis in ['top','bottom','left','right']:
    #     ax.spines[axis].set_linewidth(3)

    
    # plt.show()

if __name__ == "__main__":
    main()