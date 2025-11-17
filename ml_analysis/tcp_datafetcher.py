# # Purpose of this program: Fetches data from measurements -database via TCP.

import requests
import pandas as pd
import re
import os
import logging
logger = logging.getLogger(__name__)
from dotenv import load_dotenv


class Dataclient:
    def __init__(self):
        pass
    
    def data_fetch(self):
        load_dotenv()
        url = os.getenv("DATA_FETCH_URL") # ml_analysis has its own .env!
        logger.info(f"Fetching data..")
        response = requests.get(url,timeout=5)
        response.raise_for_status() # raises errors
        return response.text
        

    def data_parsing(self, data_input):
        logger.info(f"Starting data parsing..")
        data_rows = data_input.replace('<br>','\n').splitlines()
        wanted_pattern = re.compile(r"Time:\s*(.+?)\s*-\s*Sensor X:\s*(\d+)\s*-\s*Sensor Y:\s*(\d+)\s*-\s*Sensor Z:\s*(\d+)\s*-\s*Sensor Orientation:\s*(\d+)")
        
        match_list = [] # list for data match dicts

        for row in data_rows:
            # match = pattern.match(pattern, string) # og syntax 
            data_match = wanted_pattern.match(row.strip()) 
            if data_match: 
                timestamp, x, y, z, orientation = data_match.groups() # Pattern.groups: The number of capturing groups in the pattern
                match_list.append({
                    "time": timestamp,
                    "sensor_x": int(x),
                    "sensor_y": int(y),
                    "sensor_z": int(z),
                    "sensor_orientation": int(orientation),
                })
        df = pd.DataFrame(match_list)
        return df
        
        
    def clean_dataframe(self, dataframe_in):
        # logger.info(f"Columns are: {dataframe_in.columns}") # debug
        
        logger.info(f"Checking dataframe for NULL values..")
        null_count = dataframe_in.isnull().sum().sum()
        logger.info(f"Dataframe_in had: {null_count} NULL values.")

        if null_count == 0:
            logger.info(f"No NULL values found. Continuing..")
            return dataframe_in
        
        logger.info(f"Total of {null_count} null values detected.")
        dataframe_out = dataframe_in.dropna() # Dropping NULL rows

        new_row_count = len(dataframe_in) - len(dataframe_out)
        logger.info(f"Removed total of {new_row_count} null values.")
        return dataframe_out
    

    def csv_conversion(self, dataframe_in):
        outputfile='./ml_analysis/data/measurementdata.csv'
        dataframe_in.to_csv(outputfile,index=False) #if index isn't necessary, use index=False or data.drop("Unnamed: 0",etc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = Dataclient()
    received_data = client.data_fetch()
    raw_dataf = client.data_parsing(received_data)
    cleaned_dataf = client.clean_dataframe(raw_dataf)
    client.csv_conversion(cleaned_dataf)