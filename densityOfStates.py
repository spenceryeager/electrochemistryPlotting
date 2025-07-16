import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import scipy.constants as constant
import os
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300

# A program to calculate the potential-dependent density of states, DOS(E), of a polymer electrode from a cyclic voltammetry file. 

# This only works for CH Instruments generated files. Can be used as a template for other instrument manufacturers

def main():
    # fill this out
    workingfile = r"file"
    savedir = r"savedir"
    savename = r"savename"

    cv = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    number_of_sweeps = 2 # number of FULL cycles in the polymer
    ox_sweep_first = True # is the oxidation sweep first? True. Reduction sweep first? False
    ox_subset, red_subset = get_voltammograms(cv, number_of_sweeps, ox_sweep_first) # These are used to get the DOS(E) for the anodic and cathodic sweeps.

    # Set parameters below for polymer
    area = 0.71 # in cm^2
    d = 300 * (10**-7) # film thickness. Can get this from profilometry of the polymer film
    v = 0.01 # scan rate of the system, V/s
    ev_conversion_factor = 4.5 # this conversion factor is for converting AgCl potentials to eV

    polymer_dos_oxidation = dos_oxidation(ox_subset, area, d, v, ev_conversion_factor)
    polymer_dos_reduction = dos_reduction(red_subset, area, d, v, ev_conversion_factor)

    if ox_sweep_first:
        polymer_dos_reduction = polymer_dos_reduction.reindex(index = polymer_dos_reduction.index[::-1]).reset_index(drop=True)

    polymer_dos_reduction.to_csv(os.path.join(savedir, savename + "_reduction_dos.csv"))
    polymer_dos_oxidation.to_csv(os.path.join(savedir, savename + "oxidation_DOS.csv"))


def rowskip(workingfile):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count1
        count1 += 1
    return row


def get_voltammograms(cv, number_of_sweeps, ox_sweep_first):
    number_of_points = len(cv)
    length_of_sweep = int(number_of_points / number_of_sweeps)
    # By default, I typically record TWO full cycles at low scan rates. I will go in later and add a better system if there are 1, 3, 4, etc. 
    red_ox_sweep_length = int(length_of_sweep / 2)

    if ox_sweep_first:
        ox_subset = cv[length_of_sweep : length_of_sweep + red_ox_sweep_length]
        red_subset = cv[length_of_sweep + red_ox_sweep_length :]
    else:
        red_subset = cv[length_of_sweep : length_of_sweep + red_ox_sweep_length]
        ox_subset = cv[length_of_sweep + red_ox_sweep_length :]

    return ox_subset, red_subset


# def highloc(voltage, highV):  # phased this section out. Will keep it in case I ever need to use it again.
#     count = 0
#     for i in voltage:
#         if i == highV:
#             loc = count
#             return loc
#         count += 1


def dos_oxidation(analyze_sweep, area, d, v, ev_conversion_factor):
    ev_scale = analyze_sweep['Potential/V']
    ev_scale = -(ev_scale + 4.5)

    dos_array = analyze_sweep[' Current/A']
    dos_array = dos_array / area
    dos_array = dos_array / (v * d)
    dos_array = dos_array / (constant.elementary_charge ** 2)
    dos_array = dos_array * constant.physical_constants['electron volt'][0]
    dos_array = dos_array.clip(upper=0)
    dos_array = np.absolute(dos_array)

    dos_data = {'Energy (eV)' : ev_scale, 'DOS(E) (states / eV cm3)': dos_array}
    dos_df = pd.DataFrame(dos_data).reset_index(drop=True)
    return dos_df


def dos_reduction(analyze_sweep, area, d, v, ev_conversion):
    ev_scale = analyze_sweep['Potential/V']
    ev_scale = -(ev_scale + 4.5)

    dos_array = analyze_sweep[' Current/A']
    dos_array = dos_array / area
    dos_array = dos_array / (v * d)
    dos_array = dos_array / (constant.elementary_charge ** 2)
    dos_array = dos_array * constant.physical_constants['electron volt'][0]
    dos_array = dos_array.clip(lower=0)
    dos_array = np.absolute(dos_array)

    dos_data = {'Energy (eV)' : ev_scale, 'DOS(E) (states / eV cm3)': dos_array}
    dos_df = pd.DataFrame(dos_data).reset_index(drop=True)
    return dos_df


def makefile(workingdir, newdir, filename):
    path = os.path.join(workingdir, newdir)
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)
    filepath = os.path.join(path, filename)
    return filepath


if __name__ == "__main__":
    main()
