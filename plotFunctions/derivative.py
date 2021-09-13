import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import tkinter.messagebox as mb
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd

def getDerivatives():
    workingfile = "/home/spenceryeager/Documents/calculations/derivative_calc/010Vs.csv"
    row = rowskip(workingfile)
    df = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    potential = np.array(df['Potential/V'])
    current = np.array(df[' Current/A'])
    
    fig, ax = plt.subplots()
    ax.plot(potential, current)
    rectprops = dict(facecolor='red', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.show()

    # skipping the first scan and using 2nd scan.
    initial_potential = potential[0]
    print(initial_potential)
    initial_index = indexer(potential[2:], initial_potential)
    print(initial_index)
    # index = indexer(df, compval)

    # xval = np.array(df[0:index]['Potential/V'])
    # yval = np.array(df[0:index][' Current/A'])
    # plt.plot(xval, yval, color='red')
    # dydx, filter_dydx = differential(xval, yval) # returns derivative and Savitzky-Golay filtered derivative.
    # plt.plot(xval[:-1], dydx, color='lightblue')
    # plt.plot(xval[:-1], filter_dydx)
    # plt.show()
    
def differential(x, y):
    dydx = np.diff(y) / np.diff(x) # this gets a list of the differential values
    filter_dydx = savgol_filter(dydx, window_length=31, polyorder=2)
    return dydx, filter_dydx


def rowskip(workingfile):  # cleans up all the extra stuff in the header
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count1
        count1 += 1
    return row


def indexer(data, comp_value):
    index = 0
    while data[index] <= comp_value:
        index += 1
    return index


def indexer2(data, comp_value): # gets the second (or subsequent) scans
    print("placeholder")


def onselect(vmin, vmax):
    global compval
    compval = vmax
    mb.showinfo(title="Close out", message="The following maximum x value was selected:" + str(compval) + " If this value is okay, close out of plot. If not, reselect")


if __name__ == '__main__':
    getDerivatives()
