from tkinter import *
import tkinter.simpledialog as sd
import os
import numpy as np
import pandas as pd
from plotLoading.fileSelect import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300
root = Tk()
root.withdraw()


def main():
    workingdir = workingdirSelect()
    filename = singleFileSelect(workingdir)
    workingfile = os.path.join(workingdir, filename)
    data = dataLoading(workingfile)
    # plotting(label_list, datasets, colorlist(len(label_list)))


def dataLoading(workingfile):
    data = pd.read_csv(workingfile)
    data = data.iloc[:, :-1]
    print(data)
    return data




def colorlist(data_points):
    # quick note: many colormaps in mpl have really light colors not good for plots.
    # so I will double the amount of color points,
    # then create a colormap list starting at the darker colors only.
    colors = plt.cm.Blues(np.linspace(0, 1, data_points*2))
    colors = colors[data_points:]
    return colors


def plotting(label_list, datalist, colors):
    plot_number = len(label_list)
    count = 0
    while count < plot_number:
        data = datalist[count]
        plt.plot(data['Wavelength (nm)'], data['Absorbance (AU)'],
                 color=colors[count], linewidth=3, label=label_list[count])
        count += 1
    plt.xlim(330, 1000)
    plt.legend(loc='best')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absorbance (arb. units)")
    plt.show()


if __name__ == "__main__":
    main()