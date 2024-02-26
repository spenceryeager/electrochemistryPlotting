import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy.constants as constants


def main():
    # outersphere parameters:
    a = 1.66 * 10**-10
    static_dielectric = 64
    frequency_dielectric = 5.5
    reorganization_energy(a, static_dielectric, frequency_dielectric)


def reorganization_energy(a, static_dielectric, frequency_dielectric):
    outer_sphere(a, static_dielectric, frequency_dielectric)


def inner_sphere():
    print('hi')


def outer_sphere(a, static_dielectric, frequency_dielectric):  # this component is taken from this publication: https://doi.org/10.1016/0022-0728(89)85030-2
    avogadro = constants.physical_constants['Avogadro constant'][0] # molecules / mol
    # print(avogadro)
    e0 = constants.epsilon_0 # F m^-1
    e = constants.elementary_charge # c

    term1 = (avogadro * (e**2)) / (16 * constants.pi * e0)
    term2 = np.reciprocal(a)
    term3 = (np.reciprocal(frequency_dielectric)) - (np.reciprocal(static_dielectric))
    print(term3)
    


if __name__ == "__main__":
    main()