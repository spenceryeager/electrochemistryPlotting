import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy.constants as constants

# reorganization energy is the combination of the (1) inner sphere and (2) outersphere components
# Inner sphere components represent the changes in bond lengths and angles of the redox mediator
# Outersphere components represent the changes in solvent molecular polarization around the mediator
# All solvent, ion, and probe geometries assume a SPHERICAL molecule. This can be back calculated from the density of each. I do not show this calculation / relationship, but it's pretty fundamental so Googling "density to volume of molecule" should lend insight

def main():
    # outersphere parameters:
    a = 3.66 * 10**-10 # radius of redox probe used, in meters
    re = (2 * (8.91* 10**-10)) # twice the distance from the image charge at the interface to the redox probe. This is considered the 2 x (SOLVENT DIAMETER + ION RADIUS), in METERS
    static_dielectric = 37.5 # Dielectric constant of the solvent system. Can be found in literature
    frequency_dielectric = 1.79 # NOTE: This value is commonly taken to be the refractive index squared.
    
    reorg_val = reorganization_energy(a, re, static_dielectric, frequency_dielectric)
    print(reorg_val)



def reorganization_energy(a, re, static_dielectric, frequency_dielectric):
    inner_sphere()
    outersphere_val = outer_sphere(a, re, static_dielectric, frequency_dielectric)
    return outersphere_val

 
def inner_sphere():
    # leaving this section blank for now because I only use ferrocene, which has negligible changes in bond distances
    # for future implementations: normal-mode force constants can be approximated from reduced mass and bond vibrations from FT-IR
    print()


def outer_sphere(a, re, static_dielectric, frequency_dielectric):
    # this component is taken from this publication: https://doi.org/10.1016/0022-0728(89)85030-2 and explained further in this one https://www.sciencedirect.com/science/article/pii/0009261491905032

    avogadro = constants.physical_constants['Avogadro constant'][0] # molecules / mol
    # print(avogadro)
    e0 = constants.epsilon_0 # F m^-1
    e = constants.elementary_charge # c

    # Note about units here. Term 1 (term1) has units of C^2 F^-1 m mol^-1. Term 2 (term2) is unitless, since it uses dielectric values. Term 3 (term3) has units of m. Multiplying all three terms leaves C^2 F^-1 mol^-1. I won't derive why here, but C^2 F^-1 is equivalent to J, as I note in the final_product comment, leaving the final calculated reorganization energy as J mol^-1. It must be converted to singular eV value for typical presentation, which is why I do so in final_product_ev, by removing the mol^-1 and converting J to eV.

    term1 = (avogadro * (e**2)) / (8 * constants.pi * e0)
    term2 = (np.reciprocal(a) - np.reciprocal(re))
    term3 = (np.reciprocal(frequency_dielectric)) - (np.reciprocal(static_dielectric))
    
    final_product = term1 * term2 * term3 # note: as is, this is in J / mol
    print(final_product, "J mol^-1")
    final_product_ev = final_product * (6.24 * 10**18) / avogadro
    return(final_product_ev)
   
    


if __name__ == "__main__":
    main()