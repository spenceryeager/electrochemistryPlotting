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

# a program to plot and calculate the density of states from a cyclic voltammogram file
# reminder: if working on this a while from now, looking at raw data file will give all parameters asked
# for in the prompts!
# root = Tk()
# root.withdraw()

# workingdir = fd.askdirectory(initialdir="enter file path")
# workingfile = fd.askopenfilename(initialdir=workingdir)

# highV = sd.askfloat(title='High Potential', prompt="Enter the high potential set")
# if highV == None:
#     mb.showerror(title="Abort", message="Program aborting")
#     quit()

workingfile = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\data\SPECS-Project\2023\06Aug2023_StingelinPBTTTMacroscale\CV\10mVs_no_sec.csv"
savedir = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\data\SPECS-Project\2023\06Aug2023_StingelinPBTTTMacroscale\figures"
savename = "pbttt_dos.svg"
# below is for saving extra info
workingdir = r"\\engr-drive.bluecat.arizona.edu\Research\Ratcliff\Spencer Yeager\data\SPECS-Project\2023\06Aug2023_StingelinPBTTTMacroscale\CV"
highV = 1.2 # V
area = 0.71
d = 300 * (10**-7)
v = 0.01 # Scan rate, V/s

def rowskip(file):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count1
        count1 += 1
    return row


cv = pd.read_csv(workingfile, skiprows=rowskip(workingfile))


def highloc(voltage, highV):
    count = 0
    for i in voltage:
        if i == highV:
            loc = count
            return loc
        count += 1


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

# plotting
fontsize = 40
mpl.rcParams.update({'font.size': fontsize, 'figure.autolayout': True})
fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
ax.plot(dos_array / 10**20, energy_array, color="black", linewidth=7)
ax.set_xlabel(r'Density of States (states eV$^{-1}$ cm$^{-3}$) x10$^{20}$')
ax.set_ylabel(ytit)
ax.xaxis.labelpad = 5
ax.yaxis.labelpad = 5
ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)


for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(3)

plt.savefig(os.path.join(savedir, savename))
plt.show()

