import os
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
import pandas as pd
from tkinter import *
from fileSelect import select

root = Tk()
root.withdraw()

def load():
    name = sd.askstring(title="Enter label", prompt="Enter label for data set")
    workingdir, workingfile= select()
    print(workingfile)
    # df = pd.read_csv(workingfile)



# Everything below is for debugging only


def main():
    load()


if __name__ == "__main__":
    main()
