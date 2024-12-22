import sys
import os
import pandas as pd
import numpy as np

from src.exception import custom_exception
from src.logger import logging
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def recommend(self,movie_name):
        try:
            df=pd.read_csv("artifacts/transformed_data.csv")
            model_path=os.path.join("artifacts","model.pkl")
            model=load_object(file_path=model_path)

            movie_ind=df[df['title']==movie_name].index[0]
            sim=model[movie_ind]
            movies=sorted(list(enumerate(sim)),reverse=True,key=lambda x:x[1])[1:6]

            recommend_movies=[df.iloc[movies[0]].title for movie in movies]
            return recommend_movies
        except IndexError:
            return {"return":["Sorry, the entered movie is not present in our database.maybe try some other movie?"]}

        except Exception as ep:
            raise custom_exception(ep,sys)




