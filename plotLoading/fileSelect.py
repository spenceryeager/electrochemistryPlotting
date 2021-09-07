import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import Tk

def programquit():
    mb.showerror(title="Abort", message="Program aborting")
    quit()


# used to select a single file 
def singleFileSelect(workingdir):
    filechoice = False
    messagecount = 0
    while not filechoice:
        if messagecount > 0:
            mb.showinfo(title='Select files again', message='Select files again')
        workingfile = fd.askopenfilename(initialdir=workingdir)
        if workingfile == ():
            programquit()
        filechoice = mb.askyesno(title="Confirm data selection", message="Continue with selected data?")
        messagecount += 1    
    return workingfile


def workingdirSelect():
    init_dir = sd.askstring(title="Enter initial direction", prompt="Enter the initial directory path (for remote locations)")
    workingdir = fd.askdirectory(initialdir=init_dir)
    if workingdir == ():
        programquit()
    return workingdir


def select():
    filechoice = False
    messagecount = 0
    init_dir = sd.askstring(title="Enter initial direction", prompt="Enter the initial directory path (for remote locations)")
    while not filechoice:
        if messagecount > 0:
            mb.showinfo(title='Select files again', message='Select files again')
        mb.showinfo(title="Select Working Directory", message="Select the working directory")
        workingdir = fd.askdirectory(initialdir=init_dir)
        if workingdir == ():
            programquit()
        workingfile = fd.askopenfilename(initialdir=workingdir)
        if workingfile == ():
            programquit()
        filechoice = mb.askyesno(title="Confirm data selection", message="Continue with selected data?")
        messagecount += 1    
    return workingdir, workingfile