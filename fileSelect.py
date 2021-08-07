import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import Tk

def programquit():
    mb.showerror(title="Abort", message="Program aborting")
    quit()


def select():
    filechoice = False
    messagecount = 0
    while not filechoice:
        if messagecount > 0:
            mb.showinfo(title='Select files again', message='Select files again')
        workingdir = fd.askdirectory(initialdir='/home/spenceryeager/Documents/python_bits/conductivityPlot/conductivity')
        if workingdir == ():
            programquit()
        workingfile = fd.askopenfilename(initialdir=workingdir)
        if workingfile == ():
            programquit()
        filechoice = mb.askyesno(title="Confirm data selection", message="Continue with selected data?")
        messagecount += 1    
    return workingdir, workingfile