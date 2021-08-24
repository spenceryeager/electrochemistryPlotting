import os
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
import pandas as pd
from tkinter import *

root = Tk()
root.withdraw()

def load():
    init_dir = sd.askstring(title="Enter initial direction", prompt="Enter the initial directory path (for remote locations)")
    name = sd.askstring(title="Enter label", prompt="Enter label for data set")
    workingfile = fd.askopenfilename(initialdir=init_dir, title="Select data file to load")
    df = pd.read_csv(workingfile)



# Everything below is for debugging only


def main():
    load()


if __name__ == "__main__":
    main()
