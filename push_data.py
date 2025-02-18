
from pymongo.mongo_client import MongoClient
import certifi
import sys
import os
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from Network.exception.exception import NetworkException
from Network.logging.logger import logging
load_dotenv()

MONGO_DB_URL=os.getenv('MONGODB_URL')
print(MONGO_DB_URL)
ca=certifi.where()


class NetworkETL():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df_json = df.to_dict(orient='records')
            return df_json
        except Exception as e:
            raise NetworkException(e,sys)
        
    def insert_data_to_mongodb(self,data,database,collection): 
        try:
            self.database=database
            self.collection=collection
            self.data=data

            self.mongo_client=MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.mongo_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")


            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            batch_size = 10000
            for i in range(0, len(self.data),batch_size):
                batch = self.data[i:i + batch_size]
                self.collection.insert_many(batch)

            return (len(self.data))
        except Exception as e:
            raise NetworkException(e,sys)


if __name__=='__main__':
    file_path=r"Network_Data\dataset_full.csv"
    database="network_db"
    collection="network_tb"
    networkobj=NetworkETL()
    json_data=networkobj.csv_to_json(file_path)
    print(len(json_data))
    no_of_records=networkobj.insert_data_to_mongodb(json_data,database=database,collection=collection)
    print(f"Inserted {no_of_records} records into MongoDB")