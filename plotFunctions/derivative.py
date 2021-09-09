import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import numpy as np
import pandas as pd

def main():
    workingfile = "/home/spenceryeager/Documents/calculations/derivative_calc/010Vs.csv"
    row = rowskip(workingfile)
    df = pd.read_csv(workingfile, skiprows=rowskip(workingfile))
    survey_plot(df)
    indexer(df, compval)
    


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
    loc = 0
    while data['Potential/V'][index] <= comp_value:
        index += 1
    print(index)
    print(data['Potential/V'][index])


def survey_plot(data):


    def onselect(vmin, vmax):
        global compval
        compval = vmax


    fig, ax = plt.subplots()
    ax.plot(data['Potential/V'], data[' Current/A'])
    rectprops = dict(facecolor='red', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.show()

if __name__ == '__main__':
    main()
