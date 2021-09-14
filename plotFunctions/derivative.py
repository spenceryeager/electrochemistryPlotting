import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import tkinter.messagebox as mb
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
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
    ax.plot(potential, current, color='firebrick')
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
    ax.plot(xval, yval, color='firebrick', label='Experimental CV')
    dydx, filter_dydx = differential(xval, yval, True) # returns derivative and Savitzky-Golay filtered derivative.
    dydx_xvals = xval[:-1]
    ax.plot(dydx_xvals, dydx, color='lightblue', label='Calculated Derivative')
    ax.plot(dydx_xvals, filter_dydx, color='blue', label='Savitzky-Golay Filtered Derivative')
    ax.legend(loc='best')
    rectprops = dict(facecolor='red', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.title('Select the inflection point on the derivative')
    plt.show()

    
    # Picking out second set of indexes for the average
    min_index = indexer(dydx_xvals, min_compval)
    max_index = indexer(dydx_xvals, max_compval)

    dydx_gauss = gauss_smooth(dydx[min_index:max_index])
    dydx_gauss_xval = dydx_xvals[min_index:max_index]

    dydx3 = differential(differential(dydx_gauss, dydx_gauss_xval, False), dydx_gauss_xval[:-1], False)
    print(len(dydx3))

    # fig, ax = plt.subplots()
    # ax.plot(xval, yval, color='firebrick', label='Experimental CV')
    # ax.plot(dydx_xvals, dydx, color='lightblue', label='Calculated Derivative')
    # ax.plot(dydx_xvals, filter_dydx, color='blue', label='Savitzky-Golay Filtered Derivative')
    # # ax.plot(dydx_xvals[:-2], dydx3)
    # ax.legend(loc='best')
    # plt.title('Select the inflection point on the derivative')
    # plt.show()
    # gauss1d = gauss_smooth(dydx)
    # dydx2, filter_dydx2 = differential(gauss1d, dydx_xvals)
    # dydx2_xvals = dydx_xvals[:-1]
    # dydx2 = dydx2/np.max(dydx2)
    # dydx3, filter_dydx3 = differential(dydx2, dydx2_xvals)
    # dydx3_xvals = dydx2_xvals[:-1]
    # ax.plot(dydx3_xvals, (dydx3/np.max(dydx3)))
    # dydx2 = filter_dydx[min_index:max_index]
    # dydx2_xvals = dydx_xvals[min_index:max_index]
    # dydx2, filter_dydx2 = differential(dydx2, dydx2_xvals)
    # dydx2_xvals = dydx2_xvals[:-1]
    # note: take the maximum of the dydx and use that as the starting point.
    
def differential(x, y, apply_filter):
    dydx = np.diff(y) / np.diff(x) # this gets a list of the differential values
    if apply_filter:
        filter_dydx = savgol_filter(dydx, window_length=31, polyorder=3)
        return dydx, filter_dydx
    else:
        return dydx

def gauss_smooth(x):
    smoothed = gaussian_filter1d(x, 10)
    return smoothed

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
