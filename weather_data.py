import pandas as pd
import os

# Base directory containing year folders
data_dir = r"D:\OpenHack\Hackathon Datasets\Copernicus Weather Data"

# List of years
years = range(2008, 2022)

# Dictionary to store combined data
combined_data = pd.DataFrame()

flag = 0

for year in years:
    # Path to year folder
    year_dir = os.path.join(data_dir, str(year))

    # Create an empty DataFrame for this year
    year_data = pd.DataFrame()

    # Loop through each file in the year folder
    for filename in ["Relative_humidity", "Soil_Type", "Surface_net_solar_radiation", "Temperature", "Total_precipitation"]:
        # Full file path
        filepath = os.path.join(year_dir, filename)+str(year)+".csv"

        print(f"Reading {filepath}")

        # Read the file based on extension (using csv loader for example)
        if filepath.endswith(".csv"):
            data = pd.read_csv(filepath, header=0, delimiter=",")
            # rename the last coluns as the filename
            data.rename(columns={data.columns[-1]: filename}, inplace=True)
        else:
            # Handle other file formats with specific loading functions
            raise NotImplementedError(f"Unsupported file format: {filename}")

        # Merge the data into the year's DataFrame
        year_data = pd.concat([year_data, data], axis=1)

        # drop duplicate columns
        year_data = year_data.loc[:, ~year_data.columns.duplicated()]
        

    # Add year's data to combined dataframes
    combined_data = pd.concat([combined_data, year_data], ignore_index=True)

# drop the first column
combined_data = combined_data.drop(combined_data.columns[0], axis=1)

# Save the combined data to a file
combined_data.to_csv("combined_data.csv", index=False)
