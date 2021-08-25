import tkinter.simpledialog as sd

# cleans up all the extra stuff in the header

def rowSkip(workingfile): 
    header = sd.askstring(title="Enter header", prompt="enter the header of the data file")
    file = open(workingfile, 'r')
    count1 = 0
    for line in file:
        if line.strip() == header:
            row = count1
        count1 += 1
    return row