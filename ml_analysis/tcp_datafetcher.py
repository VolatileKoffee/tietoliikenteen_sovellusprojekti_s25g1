# # Purpose of this program: Fetches data from measurements -database via TCP.

import requests
import pandas as pd
import mysql
import os
import logging
logger = logging.getLogger(__name__)

class Dataclient:
    def __init__(self):
        pass
    

    def http_request(self):
        url = 'http://172.20.241.11/db_fetch.php'
        logger.info(f"Trying to fetch data from {url}")
        try:
            response = requests.get(url)
            raw_data = response.text
            
        except:
            pass



    def data_parsing(self):
        # parsing, etc.
        # data1 = pd.read_csv(raw_text_data)
        # data1.to_csv("text_data.csv")
        pass

    # data to dataframe?

    # dataframe.to_csv(outputfile) ?









if __name__ == "__main__":
    client = Dataclient()
    client.http_request()