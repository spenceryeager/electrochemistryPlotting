import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants as constants
import scipy.integrate as integrate

# This is used to calculate the forward and backward rate coefficients in conductive polymers using Marcus Theory
# Basis for this script is from this paper, eqns 3 & 4, Figure 3.
# https://pubs.acs.org/doi/10.1021/acs.jpcc.8b06861


def main():
    # Constants!
    polymer_dos = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\calculated_DOS\p3ht_calculated_DOS.csv"
    polymer_dos_load = pd.read_csv(polymer_dos)
    reorganization_energy = 0.39 # eV. Calculated from reorganization_energy.py
    formal_potential = -5.05 # eV. Of Ferrocene, from literature.
    temperature = 298 # K
    conc_red = 0.003 # molar

    ef = fermi_level_polymer(polymer_dos_load)
    # fermi_dirac = fermi_dirac_distribution(polymer_dos_load['Energy wrt Vac (eV)'], ef, temperature)


    fc_dos = dos_estimate_red(reorganization_energy, conc_red, temperature, formal_potential, polymer_dos_load['Energy wrt Vac (eV)'])
    # print(fc_dos)
    # print(polymer_dos_load['Energy wrt Vac (eV)'])


    combined_dos = polymer_dos_load['DOS (states/(eV cm^3))'] * fc_dos 
    kf = kf_preintegral(polymer_dos_load['Energy wrt Vac (eV)'], combined_dos, reorganization_energy, formal_potential, temperature, ef)
    kf = integrate.cumulative_trapezoid(kf, x=polymer_dos_load['Energy wrt Vac (eV)'], dx=0.001)
    kf = kf * (1.6*10**-22) # time constant

    fig, ax = plt.subplots()
    ax.plot(polymer_dos_load['Energy wrt Vac (eV)'][1:], kf)
    ax.set_yscale('log')
    plt.show()



    # fc_dos = dos_estimate_red(reorganization_energy, conc_red, temperature, formal_potential, polymer_dos_load['Energy wrt Vac (eV)'])
    # print(fc_dos)
    # print(polymer_dos_load['Energy wrt Vac (eV)'])
    

    # combined_dos = polymer_dos_load['DOS (states/(eV cm^3))'] * fc_dos
    # print('combined_dos')
    # print(combined_dos)

    # integrated_dos = integrate.cumulative_trapezoid(combined_dos, np.negative(polymer_dos_load['Energy wrt Vac (eV)']))
    # print('integrated_dos')
    # print(integrated_dos)

    # kox = integrated_dos / ((1.6 * 10**-19) * (6 * 10**17))
    
    # print('kox')
    # print(kox)
    # fig, ax = plt.subplots()
    # ax.plot(polymer_dos_load['Energy wrt Vac (eV)'], (fc_dos))
    # # plt.show()
    # # ax.set_yscale('log')
    # plt.show()


    # # Calculation
    # kf = kf_preintegral(polymer_dos_load['Energy wrt Vac (eV)'], polymer_dos_load['DOS (states/(eV cm^3))'], reorganization_energy, formal_potential, temperature, ef)
    # kf = integrate.cumulative_trapezoid(kf, x=polymer_dos_load['Energy wrt Vac (eV)'], dx=0.001)
    # kf = kf * (1.6*10**-22) # time constant

    # # kb = kb_preintegral(polymer_dos_load['Energy wrt Vac (eV)'], polymer_dos_load['DOS (states/(eV cm^3))'], reorganization_energy, formal_potential, temperature, ef)
    # # kb = integrate.cumulative_trapezoid(kb, x=polymer_dos_load['Energy wrt Vac (eV)'], dx=0.001)
    # # kb = kb * (1.6*10**-22) # time constant

    # print(integral_term)
    # fig, ax = plt.subplots()
    # # ax.plot(polymer_dos_load['DOS (states/(eV cm^3))'], polymer_dos_load['Energy wrt Vac (eV)'])

    # ax.plot(polymer_dos_load['Energy wrt Vac (eV)'][1:], np.abs(kf))
    # # ax.plot(polymer_dos_load['Energy wrt Vac (eV)'][1:], kb)

    # ax.set_yscale('log')

    # plt.show()
    # final_index = int(len(polymer_dos_load))
    

    # kfs = integrate.cumulative_trapezoid(kf, x=polymer_dos_load['Energy wrt Vac (eV)'], dx=0.001)
    # print(kfs)
  

def dos_estimate_red(reorg_energy, concentration, temperature, eo, e):
    k = constants.physical_constants['Boltzmann constant in eV/K'][0] # boltzmann
    electron = constants.e # electron charge
    # term1 = concentration
    # term2 = np.reciprocal(np.sqrt(4 * reorg_energy * k * temperature))
    term1 = 1
    term2 = 1
    term3_num = (e -  eo - reorg_energy) ** 2
    term3_denom = (4 * k * reorg_energy * temperature)
    term3_division = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3_division)
    dos_red = term1 * term2 * term3
    dos_red = dos_red * (6.02 * 10**23) /1000

    return dos_red


def dos_estimate_ox(reorg_energy, concentration, temperature, eo, e):
    k = constants.physical_constants['Boltzmann constant in eV/K'][0] # boltzmann
    electron = constants.e # electron charge
    term1 = concentration
    term2 = np.reciprocal(np.sqrt(4 * reorg_energy * k * temperature))
    # term1 = 1
    # term2 = 1
    term3_num = (e -  eo + reorg_energy) ** 2
    term3_denom = (4 * k * reorg_energy * temperature)
    term3_division = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3_division)
    dos_ox = term1 * term2 * term3
    dos_ox = dos_ox / (6.02 * 10**23) / 1000
    print(dos_ox)
    return dos_ox


def kf_preintegral(polymer_energy, polymer_dos, reorganization_energy, formal_potential, temperature, ef):
    term1 = polymer_dos
    # print(term1)
    term2 = (1 - fermi_dirac_distribution(polymer_energy, ef, temperature))
    # print(term2)
    term3_num = np.negative((polymer_energy - (2.718 * formal_potential) - reorganization_energy) ** 2)
    print('Term 3 numerator')
    print(term3_num)
    term3_denom = 4 * reorganization_energy * constants.physical_constants['Boltzmann constant in eV/K'][0] * temperature
    print('Term 3 Denominator')
    print(term3_denom)
    term3 = np.divide(term3_num, term3_denom)
    # term3 = np.exp(term3)
    print('Term 3')
    print(term3)
    return term1 * term2 * term3


def kb_preintegral(polymer_energy, polymer_dos, reorganization_energy, formal_potential, temperature, ef):
    term1 = polymer_dos
    # print(term1)
    term2 = (fermi_dirac_distribution(polymer_energy, ef, temperature))
    # print(term2)
    term3_num = np.negative(polymer_energy - (2.718 * formal_potential) - reorganization_energy) ** 2
    term3_denom = 4 * reorganization_energy * constants.physical_constants['Boltzmann constant in eV/K'][0] * temperature
    term3 = np.divide(term3_num, term3_denom)
    return term1 * term2 * term3


def fermi_dirac_distribution(e, ef, temperature):
    numerator = (e - ef)
    denominator = temperature * constants.physical_constants['Boltzmann constant in eV/K'][0]
    fermi = 1 + np.exp(numerator / denominator)
    return np.reciprocal(fermi)


def fermi_level_polymer(polymer_dos_df):
    integral_dos = np.trapz(polymer_dos_df['DOS (states/(eV cm^3))'], x=polymer_dos_df['Energy wrt Vac (eV)'], dx = 0.001)
    fermi_level_integral_val = integral_dos / 2
    index = 0
    final_index = int(len(polymer_dos_df))
    calculated_fermi_level_integral = 0


    while np.abs(calculated_fermi_level_integral) <= np.abs(fermi_level_integral_val):
        calculated_fermi_level_integral = np.trapz(polymer_dos_df['DOS (states/(eV cm^3))'][0:index], x=polymer_dos_df['Energy wrt Vac (eV)'][0:index], dx = 0.001)
        index+=1

    
    
    return (polymer_dos_df['Energy wrt Vac (eV)'].iloc[index])




if __name__ == "__main__":
    main()