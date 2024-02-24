import pandas as pd
import os

# Base directory containing state folders
data_dir = r"D:\OpenHack\Hackathon Datasets\AgMarknet Price and Arrival Data\Potato"

# List of states
states = os.listdir(data_dir)

# Dictionary to store combined data
combined_data = pd.DataFrame()

# for each state collect data and add it to combined data
for state in states:

    # path to state folder
    state_dir = os.path.join(data_dir, state)

    # empty dataframe to store folder data
    folder_data = pd.DataFrame()

    # loop through each folder in the state folder
    folders = os.listdir((state_dir))
    

    arrival_data = pd.DataFrame()
    price_data = pd.DataFrame()
    for folder in folders:

        folder_dir = os.path.join(state_dir, folder)


        # loop through each file in the folder
        for filename in os.listdir(folder_dir):

            # full file path
            filepath = os.path.join(folder_dir, filename)

            print(f"Reading {filepath}")

            # remove the header row if it is from arrival folder, if it is from price folder remove first 2 rows
            if folder == "Arrival_Annual":
                try:
                    data = pd.read_csv(filepath, header=0, delimiter=",")
                except:
                    continue
                arrival_data = pd.concat([arrival_data, data], axis=0)
            elif folder == "Price_Annual":
                try:
                    data = pd.read_csv(filepath, header=1, delimiter=",")
                except:
                    continue
                price_data = pd.concat([price_data, data], axis=0)

    # join the dataframes on arrival data's 3rd, 4th and 8th columns and price data's 2nd, 3rd and 10th columns
    data_2 = pd.merge(arrival_data, price_data, left_on=[arrival_data.columns[2], arrival_data.columns[3], arrival_data.columns[7]], right_on=[price_data.columns[1], price_data.columns[2], price_data.columns[9]], how='inner')

    # # Merge the data into the folder's DataFrame
    # folder_data = pd.concat([folder_data, data], axis=0)

    # Add folder's data to combined dataframes
    combined_data = pd.concat([combined_data, data_2], ignore_index=True)

# save the combined data to a file
combined_data.to_csv("combined_price_data.csv", index=False)
