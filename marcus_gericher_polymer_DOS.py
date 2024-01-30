import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.integrate as integrate

# Note: This approximation is coming from this Nature Comms paper:
# https://www.nature.com/articles/s41467-017-01264-2
# Equation 5 specifically. 

def main():
    # Lots of parameters to change here
    data_path = r"C:\Users\spenceryeager\Documents\example_dos\p3ht_calculated_DOS.csv"
    dos_data = pd.read_csv(data_path)
    lower_bound = -4.6
    upper_bound = -5.8
    lb_index = dos_data.index[dos_data['Energy wrt Vac (eV)'] == lower_bound][0]
    up_index = dos_data.index[dos_data['Energy wrt Vac (eV)'] == upper_bound][0]

    ef = get_fermi(dos_data[lb_index:up_index], up_index, lb_index)

    # probe constants to determine reorganization energy
    r = 3.32 # Angstrom,  reactant radius. From literature
    R = 1.66 # distance from reactant center to image charge on electrode surface. There are assumptions baked in here about polymer acting like metal electrode.
    static_dielectric = 66.1 # from literature

    reorg = reorg_energy()

    A = 0.4 #cm2
    kt = (1.6 * 10**-22) # cm4 s-1
    concentration = 3 # mM

    # fig, ax = plt.subplots()
    # ax.plot(dos_data['DOS (states/(eV cm^3))'][lb_index[0]:up_index[0]] / 10**21, dos_data['Energy wrt Vac (eV)'][lb_index[0]:up_index[0]])
    # plt.hlines(y=ef, xmin=0, xmax=5)
    # plt.show()


def reorg_energy():
    # I don't think Ferrocene has a huge inner-sphere reorganization energy contribution, so I will only approximate outer sphere
    print('hello')


def gerischer_approx(A, conc, kt, dos, ef, eo, reorg):
    print('hello')



def get_fermi(data, upper_bound, lower_bound):
    # this will be used to get the Fermi level by approximating the location where half the states would be occupied.
    area = integrate.simpson(y=data['DOS (states/(eV cm^3))'], x=data['Energy wrt Vac (eV)'])
    half_area = area / 2
    ef_index = lower_bound + 1
    ef_index_met = True

    while ef_index_met:
        area = integrate.simpson(y=data['DOS (states/(eV cm^3))'].iloc[lower_bound:ef_index], x=data['Energy wrt Vac (eV)'].iloc[lower_bound:ef_index])
        if area <= half_area:
            ef_index_met = False
        else:
            ef_index += 1

    return (data['Energy wrt Vac (eV)'].iloc[ef_index])


if __name__ == "__main__":
    main()
