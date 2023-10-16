from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.weight'] = 'bold'
rcParams['axes.labelweight'] = 'bold'
rcParams['savefig.dpi'] = 300

def main():
    file = r"R:\Spencer Yeager\data\SPECS-Project\2023\16Oct2023_100kgP3HT_NewMat\SpecEchemCV\CV1.TXT"
    specechem_data = pd.read_csv(file, skiprows=5, sep='\t')
    print(specechem_data.head())
    fig, ax = plt.subplots(figsize=(14,10), tight_layout=True)
    data_range = np.arange(1, 30, 1)
    voltages = np.linspace(-0.2, 1.4, len(data_range))
    colormap = cm.get_cmap('Reds')
    color_range = colormap(np.linspace(0, 1, 30))
    print(color_range)


    for i in data_range:
        ax.plot(specechem_data.iloc[:,0], specechem_data.iloc[:,i], color=color_range[i], linewidth=7)
        

    ax.set_xlim(350, 1100)
    ax.set_xlabel('Wavelength (nm)', fontweight='bold')
    ax.set_ylabel('Differential Absorbance (arb. units)', fontweight='bold')
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=-0.2, vmax=1.4))
    cbar = plt.colorbar(sm)
    cbar.set_label('Potential (V) versus Ag/Ag$^{+}$', rotation=270, fontweight='bold', labelpad=20)
    cbar.outline.set_linewidth(3)
    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.tick_params(axis = 'both', direction='in', which='both', length=18, width=3)
    

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)


    plt.show()


if __name__ == "__main__":
    main()