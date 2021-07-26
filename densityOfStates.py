import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import numpy as np
# a program to plot and calculate the density of states from a cyclic voltammogram file

root = Tk()
root.withdraw()

workingfile = fd.askopenfilename(initialdir="/home/spenceryeager/Documents/python_bits/densityOfStates")

file = open(workingfile, 'r')
count2 = 0
for line in file:
    if line.strip() == "Potential/V, Current/A":
        row = count2
    count2 += 1

cv = pd.read_csv(workingfile, skiprows=row)

potential_list = []
current_list = []

count = 0
while cv['Potential/V'][count] != 0.900:
    potential_list.append(cv['Potential/V'][count])
    current_list.append(cv[' Current/A'][count])
    count +=1

