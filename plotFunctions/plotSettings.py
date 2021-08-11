import matplotlib.pyplot as ply
import numpy as np
import pandas as pd
import tkinter.messagebox as mb
from tkinter import *
root = Tk()
root.withdraw()


def makePlot(x, y):
    plotOK = False
    



    while not plotOK:
        plotOK = mb.askyesno(title="Keep Plot?", message="Keep the plot? (Yes to keep, No to redefine graph parameters)")
