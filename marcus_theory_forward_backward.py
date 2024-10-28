import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants as constants

# This is used to calculate the forward and backward rate coefficients in conductive polymers using Marcus Theory
# Basis for this script is from this paper, eqns 3 & 4, Figure 3.
# https://pubs.acs.org/doi/10.1021/acs.jpcc.8b06861


def main():
    # Constants!
    polymer_dos = r"D:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\calculated_DOS\p3ht_calculated_DOS.csv"
    polymer_dos_load = pd.read_csv(polymer_dos)
    reorganization_energy = 0.39 # eV. Calculated from reorganization_energy.py
    formal_potential = -5.05 # eV. Of Ferrocene, from literature.
    temperature = 298 # K


def fermi(e, ef, temperature):
    fermi = 1 + np.exp()


if __name__ == "__main__":
    main()