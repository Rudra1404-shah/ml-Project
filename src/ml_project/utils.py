import os
import sys
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from src.ml_project.exception import CustomException
from src.ml_project.logger import logging

# Load environment variables
load_dotenv()
CLIENT = os.getenv('CLIENT')  
DB = os.getenv('DB')
COLLECTION = os.getenv('COLLECTION')


def read_all_from_mongo():
    """
    Reads all documents from the MongoDB collection.
    Returns a Pandas DataFrame.
    """
    try:
        logging.info("Connecting to MongoDB...")
        client = MongoClient(CLIENT)
        db = client[DB]
        collection = db[COLLECTION]
        logging.info(f"Connected to MongoDB collection: {COLLECTION}")
        logging.info("Reading all data from MongoDB collection...")
        data = list(collection.find({}))  # SELECT * equivalent

        if not data:
            logging.warning("No data found in MongoDB collection.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
    

        # Drop the MongoDB '_id' column if present
        if '_id' in df.columns:
            df.drop('_id', axis=1, inplace=True)

        logging.info(f"Data read successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        raise CustomException(e, sys)
