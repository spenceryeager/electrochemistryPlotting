import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter.filedialog as fd
import numpy as np

#only works for a single file
working_file = fd.askopenfilename(initialdir="enter working directory")
print(working_file)

# opening file, and counting how many lines are present until headers
file = open(working_file, 'r')
count = 0
for line in file:
    if line.strip() == "Potential/V, Current/A":
        row = count
    count += 1

cv = pd.read_csv(working_file, skiprows=row)
j = np.array(cv[' Current/A'])
j = j / 0.71
plt.rc('font', size=15)
plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.figure(figsize=(10,6))
plt.plot(cv['Potential/V'], j, color='red')
plt.xlim(max(cv['Potential/V'] + 0.1), min(cv['Potential/V'] - 0.1))
plt.xlabel('Potential (V)')
plt.ylabel('Current Density (A/cm$^{2}$)')
plt.show()
# print(cv)