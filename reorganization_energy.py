import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy.constants as constants

# reorganization energy is the combination of the (1) inner sphere and (2) outersphere components
# Inner sphere components represent the changes in bond lengths and angles of the redox mediator
# Outersphere components represent the changes in solvent molecular polarization around the mediator

def main():
    # outersphere parameters:
    a = 1.66 * 10**-10 # radius of redox probe used, in meters
    re = (2 * a) # twice the distance from the image charge at the interface to the redox probe. I am assuming this to be twice the distance of the radius (not accounting for solvent shell)
    static_dielectric = 64
    frequency_dielectric = 5.5
    reorganization_energy(a, re, static_dielectric, frequency_dielectric)


def reorganization_energy(a, re, static_dielectric, frequency_dielectric):
    inner_sphere()
    outer_sphere(a, re, static_dielectric, frequency_dielectric)

 
def inner_sphere():
    # leaving this section blank for now because I only use ferrocene, which has negligible changes in bond distances
    # for future implementations: normal-mode force constants can be approximated from reduced mass and bond vibrations from FT-IR
    print()


def outer_sphere(a, re, static_dielectric, frequency_dielectric):
    # this component is taken from this publication: https://doi.org/10.1016/0022-0728(89)85030-2
    # Gotta use a slightly different formulation to account for an electrode as opposed to two molecules transferring charges to each other

    avogadro = constants.physical_constants['Avogadro constant'][0] # molecules / mol
    # print(avogadro)
    e0 = constants.epsilon_0 # F m^-1
    e = constants.elementary_charge # c

    term1 = (avogadro * (e**2)) / (8 * constants.pi * e0)
    term2 = (np.reciprocal(a) - np.reciprocal(re))
    term3 = (np.reciprocal(frequency_dielectric)) - (np.reciprocal(static_dielectric))
    
    final_product = term1 * term2 * term3 # note: as is, this is in J / mol
    print(final_product, "J mol^-1")
    
    final_product_ev = final_product * (6.24 * 10**18) / avogadro
    print(round(final_product_ev, 2), "eV")
    


if __name__ == "__main__":
    main()