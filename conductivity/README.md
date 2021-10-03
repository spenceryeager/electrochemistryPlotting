# Conductivity plotting

This folder contains all of the code I use to calculate and plot conductivity. To get the instantaneously slope at each point, a deriviative is taken using Numpy and that value is used as the particular conductivity at potential X. In doing this, the sample set loses one point at the very end, making the size n to n-1.