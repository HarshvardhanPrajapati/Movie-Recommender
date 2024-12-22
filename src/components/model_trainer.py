import os
import sys

from src.exception import custom_exception
from src.logger import logging
from src.utils import save_object

import numpy as np
import pandas as pd

from dataclasses import dataclass

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')



@dataclass
class ModelTrainerConfig:
    trained_model_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_training(self,df):
        try:
            logging.info("model training begun")
            if 'finalcol' not in df.columns:
                raise ValueError("'finalcol' column is missing in the DataFrame")
            if df['finalcol'].isnull().any():
                raise ValueError("'finalcol' contains null values")
            vectors=cv.fit_transform(df['finalcol']).toarray()
            similarity_matrix=cosine_similarity(vectors)

            save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj=cosine_similarity(vectors)
            )
            
            logging.info("pickle file of model saved successfully!!")
        except Exception as ep:
            raise(ep,sys)
                





