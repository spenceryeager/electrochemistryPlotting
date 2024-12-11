import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy.constants as constants
import scipy.integrate as integrate

# This is used to calculate the forward and backward rate coefficients in conductive polymers using Marcus Theory
# Basis for this script is from this paper, eqns 3 & 4, Figure 3.
# https://pubs.acs.org/doi/10.1021/acs.jpcc.8b06861


def main():
    # Constants!
    polymer_dos = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\calculated_DOS\p3ht_oxidation_DOS.csv"
    polymer_red_dos = r"E:\RDrive_Backup\Spencer Yeager\papers\paper4_pbtttt_p3ht_transfer_kinetics\worked-up-data\calculated_DOS\p3ht_reduction_DOS.csv"
    polymer_dos_load = pd.read_csv(polymer_dos)
    polymyer_dos_red_load = pd.read_csv(polymer_red_dos)
    kf_filename = "kf_dmso.csv"
    kb_filename =  "kb_dmso.csv"
    reorganization_energy = 0.6806347383955402 # eV. Calculated from reorganization_energy.py
    formal_potential = -5.05 # eV. Of Ferrocene, from literature.
    temperature = 298 # K
    conc_red = 0.003 # concentration of reductant in electrolyte. Molar
    conc_ox = 0.003 # concentration of oxidant in electrolyte. Molar

    # Fermi Level and Fermi Dirac function section
    ef = fermi_level_polymer(polymer_dos_load) # approximating the Fermi level of the polymer from DOS(E)
    ef_red = fermi_level_polymer(polymyer_dos_red_load)
    print(ef_red)

    # Fermi stuff for the Kf
    fermi_dirac = fermi_dirac_distribution(polymer_dos_load['Energy wrt Vac (eV)'], ef, temperature) 
    subtracted_fermi = (1 - fermi_dirac) # Use this one for determining the kf

    # Fermi stuff for the Kb
    fermi_dirac_kb = fermi_dirac_distribution(polymyer_dos_red_load['Energy wrt Vac (eV)'], ef_red, temperature) 


    # Electrolyte DOS section
    electrolyte_dos_ox = dos_estimate_ox(reorganization_energy, conc_ox, temperature, formal_potential, polymer_dos_load['Energy wrt Vac (eV)']) # Use this one for determining kf. Oxidant is species being REDUCED.

    electrolyte_dos_red = dos_estimate_red(reorganization_energy, conc_red, temperature, formal_potential, polymer_dos_load['Energy wrt Vac (eV)']) # Use this one for determining the kf. Gerischer language is sort of inversed - this is the REDUCTANT DOS(E), i.e. the species that gets oxidized

    # Kb section
    polymyer_dos_red_load = polymyer_dos_red_load.reindex(index = polymyer_dos_red_load.index[::-1]).reset_index(drop=True)
    combined_kb_terms = polymyer_dos_red_load['DOS (states/(eV cm^3))'] * electrolyte_dos_ox * fermi_dirac_kb
    kb = integrate.cumulative_trapezoid(combined_kb_terms, polymer_dos_load['Energy wrt Vac (eV)'])
    kb = kb * (1.6*10**-22) # time constant
    kb = np.abs(kb)

    # Kf section
    # Multiplying the polymer DOS(E), electrolyte DOS(E) and the Fermi Dirac distribution for kf
    combined_kf_terms = polymer_dos_load['DOS (states/(eV cm^3))'] * electrolyte_dos_red * subtracted_fermi
    kf = integrate.cumulative_trapezoid(combined_kf_terms, x=polymer_dos_load['Energy wrt Vac (eV)'], dx=0.001)
    kf = kf * (1.6*10**-22) # time constant
    kf = np.abs(kf)

    data_ox = {'Energy (eV)': polymer_dos_load['Energy wrt Vac (eV)'][1:], "Kf (cm s^-1)":kf}
    kf_df = pd.DataFrame(data_ox).reset_index(drop=True)
    
    data_red = {'Energy (eV)': polymyer_dos_red_load['Energy wrt Vac (eV)'][1:], "Kb (cm s^-1)":kb}
    kb_df = pd.DataFrame(data_red).reset_index(drop=True)

    kf_df.to_csv(os.path.join(r"E:\Electrochemical_Parameters\kf_kb_reorg", kf_filename))
    kb_df.to_csv(os.path.join(r"E:\Electrochemical_Parameters\kf_kb_reorg", kb_filename))

    fig, ax = plt.subplots()
    ax.plot(polymyer_dos_red_load['Energy wrt Vac (eV)'][1:], kb)
    ax.plot(polymer_dos_load['Energy wrt Vac (eV)'][1:], kf)
    ax.set_yscale('log')
    plt.show()

  

def dos_estimate_red(reorg_energy, concentration, temperature, eo, e):

    k = constants.physical_constants['Boltzmann constant in eV/K'][0] # boltzmann
    electron = constants.e # electron charge
    # term1 = concentration # We do not need to incorporate this into the formulation. It is canceled out ultimately.
    # term2 = np.reciprocal(np.sqrt(4 * reorg_energy * k * temperature)) # We do not need to incorporate this into the formulation. It is a normalization parameter
    term3_num = (e -  eo + reorg_energy) ** 2
    term3_denom = (4 * k * reorg_energy * temperature)
    term3_division = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3_division)
    dos_red = term3
    return dos_red


def dos_estimate_ox(reorg_energy, concentration, temperature, eo, e):
    k = constants.physical_constants['Boltzmann constant in eV/K'][0] # boltzmann
    electron = constants.e # electron charge

    term3_num = (e -  eo - reorg_energy) ** 2
    term3_denom = (4 * k * reorg_energy * temperature)
    term3_division = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3_division)
    dos_ox = term3
    return dos_ox


def kf_preintegral(polymer_energy, polymer_dos, reorganization_energy, formal_potential, temperature, ef):
    term1 = polymer_dos
    term2 = (1 - fermi_dirac_distribution(polymer_energy, ef, temperature))
    term3_num = np.negative((polymer_energy - (2.718 * formal_potential) + reorganization_energy) ** 2)
    term3_denom = 4 * reorganization_energy * constants.physical_constants['Boltzmann constant in eV/K'][0] * temperature
    term3 = np.divide(term3_num, term3_denom)
    term3 = np.exp(-term3)
    # print('Term 3')
    # print(term3)
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