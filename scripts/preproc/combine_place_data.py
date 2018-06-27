"""
Combine the Google Places data with manually curated citywide destination data. 

Inputs:
    - Citywide places file containing urban villages, destination parks, and
        citywide points.
    - Google Places data from API.

Outputs: 
    - CSV containing merged data.

Usage: combine_place_data.py
"""
import os

import pandas as pd


DATADIR = os.path.join(os.getcwd(), "../../seamo/data/")

if __name__ == "__main__":
    """
    Open the raw place & citywide data as Pandas dataframes.

    Create a new dataframe that joins the two and store that as a CSV. 
    """

    # Filepaths
    places_path = os.path.join(DATADIR, 'raw/GoogleMatrixPlaces.csv')
    citywide_path = os.path.join(DATADIR, 'raw/GoogleMatrix_Places_Citywide.csv')
    output_path = os.path.join(DATADIR, 'processed/GoogleMatrix_Places_Full.csv')

    # Create the dataframes and concatenate them
    places_df = pd.read_csv(places_path)
    citywide_df = pd.read_csv(citywide_path)
    full_places_df = pd.concat([places_df, citywide_df])

    # Write combined DF to a CSV
    full_places_df.to_csv(output_path, mode='w', header=True, index=False)
