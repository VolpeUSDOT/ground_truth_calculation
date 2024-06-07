# Import necessary modules
import pandas as pd
import os

import vru_helper as vh

#===========================================================================================
def main():
    # Configure the below parameters to match your setup
    username = 'juwon.drake'
    file_name = "Markerless data.xlsx"

    #==============================================================================================
    file_path = os.path.join(r'C:\Users', username, 'DOT OST','VIEW - MassDOT','Data Collection')
    markerless_data = pd.read_excel(os.path.join(file_path, file_name))

    if (len(markerless_data.columns) > 0) and ('unnamed' in markerless_data.columns[1].lower()):
        # Below was needed to create column headers on my run. - Juwon
        markerless_data.columns = markerless_data.iloc[1]
        markerless_data = markerless_data.drop(markerless_data.index[0:2])

    markerless_data = vh.markerless_loop(markerless_data = markerless_data, file_path = file_path, filename_col = 'FileName - 20 m')

    markerless_data.to_excel(file_path + "MassDOT Markerless data_results_python.xlsx")

if __name__ == '__main__':
    main()
