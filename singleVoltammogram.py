import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter.filedialog as fd

#only works for a single file
working_file = fd.askopenfilename(initialdir="enter initial directory here")
print(working_file)

# opening file, and counting how many lines are present until headers
file = open(working_file, 'r')
count = 0
for line in file:
    if line.strip() == "Potential/V, Current/A":
        row = count
    count += 1

cv = pd.read_csv(working_file, skiprows=row)
plt.rc('font', size=15)
plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.figure(figsize=(10,6))
plt.plot(cv['Potential/V'], cv[' Current/A'], color='red')
plt.xlim(max(cv['Potential/V'] + 0.1), min(cv['Potential/V'] - 0.1))
plt.xlabel('Potential (V)')
plt.ylabel('Current (A)')
plt.show()
# print(cv)