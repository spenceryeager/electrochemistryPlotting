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
    label_list = list(data)
    label_list = label_list[1:]
    plotting(label_list, data, colorlist(len(list(data))-1))


def dataLoading(workingfile):
    data = pd.read_csv(workingfile)
    data = data.iloc[:, :-1]
    column = column_name()
    data.columns = column
    print(data)
    return data


def column_name():
    columnlist = ['Wavelength']
    init_V = -0.4
    final_V = 0.8
    delta_V = final_V - init_V
    sr = 0.1 # V/s
    value = init_V +0.1
    while value < final_V:
        value = np.add(value, 0.1)
        value = np.round(value, 1)
        columnlist.append(str(value)+"V")
    return columnlist


def colorlist(data_points):
    # quick note: many colormaps in mpl have really light colors not good for plots.
    # so I will double the amount of color points,
    # then create a colormap list starting at the darker colors only.
    colors = plt.cm.BrBG(np.linspace(0, 1, data_points*2))
    colors = colors[data_points:]
    return colors


def plotting(label_list, data, colors):
    plot_number = len(label_list)
    count = 0
    for i in data:
        if i != 'Wavelength':
            plt.plot(data['Wavelength'], data[i], color=colors[count], label=i, linewidth=2)
            print(i)
            count += 1
    # wavelength = data[0]
    # while count < plot_number:
    #     data = datalist[count]
    #     plt.plot(data['Wavelength (nm)'], data['Absorbance (AU)'],
    #              color=colors[count], linewidth=3, label=label_list[count])
    #     count += 1
    plt.xlim(330, 1000)
    plt.legend(loc='best', prop={'size':6})
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Absorbance (arb. units)")
    plt.ylim((-0.25, 0.2))
    plt.show()


if __name__ == "__main__":
    main()