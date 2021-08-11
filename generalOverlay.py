import matplotlib.pyplot as plt
import pandas as pd
import numpy as numpy
import os
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import tkinter.filedialog as fd
from fileSelect import select
from tkinter import *

# this program makes a general plotting. It may need to be rewritten to accomodate certain files.

root = Tk()
root.withdraw()

workingdir, workingfile = select()
