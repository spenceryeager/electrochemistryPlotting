from plotLoading.fileSelect import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300
import pandas as pd
import numpy as np
import os
import tkinter.simpledialog as sd
from tkinter import *
root = Tk()
root.withdraw()


def main():
    workingdir = workingdirSelect()
    label_list, datasets = dataLoading(workingdir)
    plotting(label_list, datasets, colorlist(len(label_list)))


def dataLoading(workingdir):
    number = sd.askinteger(title="Enter number", prompt="Enter number of data sets to load")
    datasets = []
    label_list = []
    count = 0
    while count < number:
        data = singleFileSelect(workingdir)
        label = sd.askstring(title="Enter label", prompt="Enter data label for legend")
        filepath = os.path.join(workingdir, data)
        df = pd.read_csv(filepath, usecols=[0,1])
        label_list.append(label)
        datasets.append(df)
        count += 1
    return label_list, datasets


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
        plt.plot(data['Wavelength (nm)'], data['Absorbance (AU)'], color=colors[count], linewidth=3, label=label_list[count])
        count += 1
    plt.xlim(330, 1000)
    plt.legend(loc='best')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absorbance (arb. units)")
    plt.show()


if __name__ == "__main__":
    main()