# Conductivity plotting

This folder contains the functions that I use within the "conductivityPlot.py" program. cond_derivative.py is used to get the instantaneously slope at each point. A deriviative is taken using Numpy and that value is used as the particular conductivity at potential X. In doing this, the sample set loses one point at the very end, making the size n to n-1.