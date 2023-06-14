# following Melanie and Erin's paper https://www.nature.com/articles/s41467-017-01264-2

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constant


def main():
    reorg_energy = 0.5 # eV
    eo = -5.05 # eV of ferrocene
    e_red = np.linspace(eo,-4, 1000) # energy scale
    e_ox = np.linspace(eo,-6, 1000) # energy scale
    conc_red = 0.0015 # molar
    temperature = 298 # K
    dos_red = dos_estimate_red(reorg_energy, conc_red, temperature, eo, e_red)
    dos_ox = dos_estimate_ox(reorg_energy, conc_red, temperature, eo, e_ox)

    fig, ax = plt.subplots()
    ax.plot(dos_red, e_red)
    ax.plot(dos_ox, e_ox)
    plt.show()


def dos_estimate_red(reorg_energy, concentration, temperature, eo, e):
    k = constant.k # boltzmann
    electron = constant.e # electron charge
    term1 = concentration
    term2 = np.reciprocal(np.sqrt(4 * reorg_energy * k * temperature))
    term3_num = (e -  eo - reorg_energy) ** 2
    term3_denom = (4 * k * reorg_energy * temperature * (6.2* (10 **18)))
    term3_division = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3_division)
    dos_red = term1 * term2 * term3
    return dos_red


def dos_estimate_ox(reorg_energy, concentration, temperature, eo, e):
    k = constant.k # boltzmann
    electron = constant.e # electron charge
    term1 = concentration
    term2 = np.reciprocal(np.sqrt(4 * reorg_energy * k * temperature))
    term3_num = (e -  eo + reorg_energy) ** 2
    term3_denom = (4 * k * reorg_energy * temperature * (6.2* (10 **18)))
    term3_division = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3_division)
    dos_ox = term1 * term2 * term3
    return dos_ox




if __name__ == "__main__":
    main()
