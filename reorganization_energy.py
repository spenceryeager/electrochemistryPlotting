import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy.constants as constants


def main():
    reorganization_energy()


def reorganization_energy():
    outer_sphere()


def inner_sphere():
    print('hi')


def outer_sphere():  # this component is taken from this publication: https://doi.org/10.1016/0022-0728(89)85030-2
    avogadro = constants.physical_constants['Avogadro constant'][0] # molecules / mol
    # print(avogadro)
    e0 = constants.epsilon_0 # F m^-1
    print(e0)
    


if __name__ == "__main__":
    main()