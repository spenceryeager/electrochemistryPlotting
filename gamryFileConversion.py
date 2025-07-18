import pandas as pd
import numpy as np
import os

# this program will take a Gamry .DTA file and convert it to a .CSV with headers that match CH Instruments files. This makes it compatible with my other programs!


def main():
    fileloc = r"E:\RDrive_Backup\Spencer Yeager\papers\paper2_GATech_Collab_P3HT-PBTTT\electrochemistry_data\17July2025_Henry_Spincast_Annealed_P3HT\film3\Henry_P3HT_Spincast_Annealed_10mVs.DTA"
    file_save_name = "Henry_P3HT_Spincast_Annealed_10mVs"
    file_save_dir = r"E:\RDrive_Backup\Spencer Yeager\papers\paper2_GATech_Collab_P3HT-PBTTT\electrochemistry_data\17July2025_Henry_Spincast_Annealed_P3HT\film3"
    cleaned_file = gamryConversion(fileloc, True, 65)
    cleaned_file.to_csv(os.path.join(file_save_dir, (file_save_name + ".csv")), index = False)


def gamryConversion(file, convention_conversion, skipping):
    # convention_conversion converts IUPAC to US Convention
    fileload = pd.read_csv(file, skiprows=skipping, sep="\t")
    converted_file = fileload[['V vs. Ref.', 'A']].copy()
    converted_file.rename(columns={'V vs. Ref.': 'Potential/V', 'A': ' Current/A'}, inplace=True)

    try:
        converted_file = converted_file[converted_file['Potential/V'].str.contains("Vf")==False]
    except AttributeError:
        pass

    try:
        converted_file = converted_file[converted_file['Potential/V'].str.contains("V vs. Ref.")==False].dropna()
    except AttributeError:
        pass

    converted_file['Potential/V'] = pd.to_numeric(converted_file['Potential/V'])
    converted_file[' Current/A'] = pd.to_numeric(converted_file[' Current/A'])
    return converted_file


if __name__ == "__main__":
    main()