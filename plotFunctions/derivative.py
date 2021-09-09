import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import tkinter.messagebox as mb
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

def getDerivatives():
    workingfile = "/home/spenceryeager/Documents/calculations/derivative_calc/010Vs.csv"
    row = rowskip(workingfile)
    df = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    survey_plot(df)
    index = indexer(df, compval)
    df = df[0:index]

    xval = np.array(df['Potential/V'])
    yval = np.array(df[' Current/A'])
    yval = yval * -1

    plt.plot(xval, yval, color='red')
    dydx = np.diff(yval) / np.diff(xval)
    plt.plot(xval[:-1], dydx, color='lightblue')

    # popt = curve_fit(expfit, xval[:1], dydx)
    # plt.plot(xval[:-1], expfit(xval[:-1], *popt))
    plt.show()
    
def expfit(x, a, b, c):
    return a * np.exp(-b * x) + c


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
    while data['Potential/V'][index] <= comp_value:
        index += 1
    return index


def survey_plot(data):


    def onselect(vmin, vmax):
        global compval
        compval = vmax
        mb.showinfo(title="Close out", message="The following maximum potential was selected:" + str(compval) + " If this value is okay, close out of plot. If not, reselect")


    fig, ax = plt.subplots()
    ax.plot(data['Potential/V'], data[' Current/A'])
    rectprops = dict(facecolor='red', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.show()


# def deriv_plot()



if __name__ == '__main__':
    getDerivatives()
