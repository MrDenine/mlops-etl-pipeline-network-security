import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, csv_file_path: str) -> str:
        """
        Convert CSV file to JSON format.
        """
        try:
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            record = list(json.loads((data.T.to_json())).values())
            return record
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(
        self, records: list, database, collection_name: str
    ) -> None:
        """
        Insert data into MongoDB collection.
        """
        try:
            self.database = database
            self.collection_name = collection_name
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection_name]
            self.collection.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    file_path = "network_data\phisingData.csv"
    database = "PHANUWAT"
    Collection = "NetworkData"
    network_obj = NetworkDataExtract()
    record = network_obj.csv_to_json_convertor(file_path)
    no_of_record = network_obj.insert_data_to_mongodb(
        records=record, database=database, collection_name=Collection
    )
    print(no_of_record, "records inserted successfully into MongoDB")
