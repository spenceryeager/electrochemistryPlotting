import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import tkinter.messagebox as mb
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd

def getDerivatives():
    # Getting the data
    workingfile = "/home/spenceryeager/Documents/calculations/derivative_calc/010Vs.csv"
    row = rowskip(workingfile)
    df = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    potential = np.array(df['Potential/V'])
    current = np.array(df[' Current/A'])
    
    # Making the initial selection plot
    fig, ax = plt.subplots()
    ax.plot(potential, current)
    rectprops = dict(facecolor='red', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.title("Only select the maximum x value")
    plt.show()

    # skipping the first scan and using 2nd scan.
    initial_potential = potential[0]
    initial_index = indexer2(potential[1:], initial_potential)
    initial_index = initial_index + 1 
    subarray = potential[initial_index:]
    index = indexer(subarray, max_compval)
    index = initial_index + index

    # Making second selection plot
    xval = potential[initial_index:index]
    yval = current[initial_index:index]
    fig, ax = plt.subplots()
    ax.plot(xval, yval, color='red', label='Experimental CV')
    dydx, filter_dydx = differential(xval, yval) # returns derivative and Savitzky-Golay filtered derivative.
    dydx_xvals = xval[:-1]
    ax.plot(dydx_xvals, dydx, color='lightblue', label='Calculated Derivative')
    ax.plot(dydx_xvals, filter_dydx, color='blue', label='Savitzky-Golay Filtered Derivative')
    ax.legend(loc='best')
    rectprops = dict(facecolor='red', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.title('Select the most linear range of the SG-Derivative\n and the experimental CV')
    plt.show()

    # Picking out second set of indexes for the average
    min_index = indexer(dydx_xvals, min_compval)
    max_index = indexer(dydx_xvals, max_compval)

    dydx_avg = np.average(dydx[min_index:max_index])
    current_avg = np.average(yval[min_index:max_index])
    print(dydx_avg)
    print(current_avg)
    print(dydx_avg/current_avg)

    
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
    if comp_value >= 0:
        while data[index] <= comp_value:
            index += 1
    else:
        while data[index] <= comp_value:
            index += 1
    return index


def indexer2(data, comp_value): # gets the second (or subsequent) scans
    index = 0
    while data[index] != comp_value:
        index += 1
    return index


def onselect(vmin, vmax):
    global max_compval
    global min_compval
    max_compval = vmax
    min_compval = vmin
    mb.showinfo(title="Close out", message="The following maximum x value was selected:\n" + str(max_compval) + "\nThe following minium x value was select:\n" + str(min_compval)+"\nIf this value is okay, close out of plot. If not, reselect")


if __name__ == '__main__':
    getDerivatives()
