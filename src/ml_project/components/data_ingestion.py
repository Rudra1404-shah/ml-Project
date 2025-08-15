import os
import sys
from src.ml_project.exception import CustomException
from src.ml_project.logger import logging
import pandas as pd
from dataclasses import dataclass
from src.ml_project.utils import read_all_from_mongo
@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.joins('artifact','train.csv')
    test_data_path:str=os.path.joins('artifact','test.csv')
    raw_data:str=os.path.joins('artifact','raw.csv')
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    def intiate_data_ingestion(self):
        try:

            logging.info("Reading from MongoDB")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df=read_all_from_mongo()
            pass
        except Exception as e:
            raise CustomException(e,sys)
