import os
import sys
from src.ml_project.exception import CustomException
from src.ml_project.logger import logging
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.ml_project.utils import read_all_from_mongo

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifact', 'train.csv')
    test_data_path: str = os.path.join('artifact', 'test.csv')
    raw_data: str = os.path.join('artifact', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def intiate_data_ingestion(self):
        """
        Initiates the data ingestion process:
        1. Reads data from MongoDB
        2. Saves raw data as CSV
        3. Splits data into train/test sets
        4. Saves train and test data as CSV files
        """
        try:
            logging.info("Starting data ingestion process")
            
            # Read data from MongoDB
            df = read_all_from_mongo()
            logging.info(f"Successfully read data from MongoDB. Shape: {df.shape}")
            
            # Create artifact directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Save raw data as CSV
            df.to_csv(self.ingestion_config.raw_data, index=False, header=True)
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Data ingestion is completed")
            return(
                self.ingestion_config.test_data_path,
                self.ingestion_config.train_data_path
            )
        except Exception as e:
            logging.error(f"Error in data ingestion: {str(e)}")
            raise CustomException(e, sys)
