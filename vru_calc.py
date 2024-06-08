# Import necessary modules
import pandas as pd
import os
import geopandas as gpd
import vru_helper as vh

#===========================================================================================
def main():
    # Configure the below parameters to match your setup
    username = 'juwon.drake'
    file_name = "Markerless data.xlsx"
    filename_column = 'FileName - 20 m'

    #==============================================================================================

    forward_line = pd.DataFrame({'x': [0, 0], 'y': [0, 30]})
    forward_line = gpd.GeoDataFrame(forward_line, geometry=gpd.points_from_xy(forward_line.x, forward_line.y), crs = 'EPSG:6481')
    forward_line = forward_line.shortest_line(forward_line.iloc[1,].geometry)
    passenger_line = pd.DataFrame({'x': [0, 30], 'y': [0, 0]})
    passenger_line = gpd.GeoDataFrame(passenger_line, geometry=gpd.points_from_xy(passenger_line.x, passenger_line.y), crs = 'EPSG:6481')
    passenger_line = passenger_line.shortest_line(passenger_line.iloc[1,].geometry)

    file_path = os.path.join(r'C:\Users', username, 'DOT OST','VIEW - MassDOT','Data Collection')
    markerless_data = pd.read_excel(os.path.join(file_path, file_name))

    if (len(markerless_data.columns) > 0) and ('unnamed' in markerless_data.columns[1].lower()):
        # Below was needed to create column headers on my run. - Juwon
        markerless_data.columns = markerless_data.iloc[1]
        markerless_data = markerless_data.drop(markerless_data.index[0:2])

    # Index just the vehicles you need for debugging (uncomment below)
    # markerless_data = markerless_data.loc[76:,]

    markerless_data = vh.markerless_loop(markerless_data, file_path, filename_column, forward_line, passenger_line)

    print('Writing Excel file to {}'.format(file_path))
    markerless_data.to_excel(os.path.join(file_path, "Markerless data results {}.xlsx".format(filename_column)))
    print('Done.')

if __name__ == '__main__':
    main()
