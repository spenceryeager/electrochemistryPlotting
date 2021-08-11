import matplotlib.pyplot as ply
import numpy as np
import pandas as pd
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
from tkinter import *
root = Tk()
root.withdraw()


def sizing(dimension):
    dim = sd.askinteger(title=("Enter "+dimension), prompt=("Enter figure " + dimension))
    return dim


def labels(axis):
    axLabel = sd.askstring(title= axis + " label", prompt=("Enter " + axis + " label. LaTeX formatting can be used"))
    return axLabel


def plotSettings():
    width = sizing("width")
    height = sizing("height")
    yax = labels("y axis")
    xax = labels("x axis")
    titlechoice = mb.askyesno(title="Title?", message="Make a graph title?")
    title = None
    if titlechoice:
        title = sd.askstring(title="Title", message="Enter graph title")
    fontsize = sd.askinteger(title="Font Size", message="Enter font size for graph")

    return width, height, yax, xax, title, fontsize
