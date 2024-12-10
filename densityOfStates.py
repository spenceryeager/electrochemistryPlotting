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

# reminder: if working on this a while from now, looking at raw data file will give all parameters asked for in the prompts!

def main():
    workingfile = r"select file to use"
    savedir = r"Select a directory to save the output csv"

    # Set parameters below for polymer
    starting_index = 0 # the starting index of sweep to be analyzed
    final_index = 1 # the final index of the sweep to be analyzed
    area = 0.71 # in cm^2
    d = 300 * (10**-7) # film thickness. Can get this from profilometry of the polymer film
    v = 0.01 # scan rate of the system, V/s

    cv = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    analyze_sweep = cv[starting_index:final_index]



def rowskip(file):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count1
        count1 += 1
    return row




# def highloc(voltage, highV):  # phased this section out. Will keep it in case I ever need to use it again.
#     count = 0
#     for i in voltage:
#         if i == highV:
#             loc = count
#             return loc
#         count += 1


highPotentialLoc = highloc(cv['Potential/V'], highV)
dos_array = np.array(cv[' Current/A'][0:highPotentialLoc]) # all calculations performed on this array
energy_array = np.array(cv['Potential/V'][0:highPotentialLoc])
v_array = energy_array

dos_array = dos_array / area
dos_array = dos_array / (v * d)
dos_array = dos_array / (constant.elementary_charge ** 2)
dos_array = dos_array * constant.physical_constants['electron volt'][0]
dos_array = np.absolute(dos_array)

energy_array = -(energy_array + 4.5)
ytit = "Energy vs. vacuum (eV)"


# file saving
vals = {"DOS (states/(eV cm^3))": dos_array, "Energy wrt Vac (eV)":energy_array, "Potential (V)":v_array}
calc_vals = pd.DataFrame(data=vals)


def makefile(workingdir, newdir, filename):
    path = os.path.join(workingdir, newdir)
    isdir = os.path.isdir(path)
    if not isdir:
        os.mkdir(path)
    filepath = os.path.join(path, filename)
    return filepath


calc_vals.to_csv(makefile(workingdir, "calculated_DOS", "calculated_DOS.csv"))

readme = open(makefile(workingdir, "calculated_DOS", "readme.txt"), 'w')
readme.write("Analysis code written by Spencer Yeager, University of Arizona \n")
readme.write("Find the source code here: https://github.com/spenceryeager/electrochemistryPlotting \n")
readme.write("densityOfStates.py \n")
readme.write("Here are the parameters used to generate this data: \n")
readme.write("area (cm^2) = " + str(area) + "\nfilm thickness (nm) = " + str(d) + "\nscan rate (V/s) = " + str(v))
readme.close()

# # plotting
# fontsize = 40
# mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
# fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
# ax.plot(dos_array / 10**20, energy_array, color="black", linewidth=7)
# ax.set_xlabel(r'Density of States (states eV$^{-1}$ cm$^{-3}$) x10$^{20}$')
# ax.set_ylabel(ytit)
# ax.xaxis.labelpad = 5
# ax.yaxis.labelpad = 5
# ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)


# for axis in ['top','bottom','left','right']:
#     ax.spines[axis].set_linewidth(3)

# plt.savefig(os.path.join(savedir, savename))
# plt.show()

if __name__ == "__main__":
    main()

