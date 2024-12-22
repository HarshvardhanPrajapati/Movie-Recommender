import os
import sys

from src.exception import custom_exception
from src.logger import logging
from src.components.data_transformation import DataTransformatinConfig
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig




import pandas as pd



from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@dataclass
class DataIngestionConfig:
    raw_data_path:str=os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        try:
            df1=pd.read_csv('notebook/tmdb_5000_credits.csv')
            df2=pd.read_csv('notebook/tmdb_5000_movies.csv')

            df=df1.merge(df2,on='title')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)


            logging.info("ingestion successful")

            return self.ingestion_config.raw_data_path

        except Exception as exp:
            raise custom_exception(exp,sys)

if __name__=='__main__':
    obj=DataIngestion()
    obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    transformed_data=data_transformation.get_transformer_object()

    modeltrainer=ModelTrainer()
    modeltrainer.initiate_model_training(transformed_data)


