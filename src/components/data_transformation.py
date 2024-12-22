import os
import sys
import nltk
import numpy as np
import pandas as pd
import string
import json


    
    

from src.exception import custom_exception
from src.logger import logging
from src.utils import save_object



try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt_tab')



from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline



from dataclasses import dataclass

@dataclass
class DataTransformatinConfig:
    preprocessor_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.transformation_config=DataTransformatinConfig()
        self.ps=PorterStemmer()

    def extract_data(self,json_str,target_job=None):
        cleaned_text=""
        try:
            if not isinstance(json_str,str):
                return cleaned_text
            data_list=json.loads(json_str)
            for enter in data_list:
                if target_job is None or enter.get('job')==target_job:
                    name=enter.get('name',"").replace(" ","")
                    cleaned_text+=name+" "
            return cleaned_text.strip()
        except json.JSONDecodeError:
            return ""


    def extract_cast_names(self,json_str):
            s=""
            try:
                if not isinstance(json_str,str):
                    return s
                listcast=json.loads(json_str)
                if(listcast!=[] and len(listcast)>=4):
                    for i in range(4):
                        listcast[i]['name']=listcast[i]['name'].replace(" ","")
                        s+=listcast[i]['name']
                        s+=" "
                else:
                    for i in listcast:
                        i['name']=i['name'].replace(" ","")
                        s+=i['name']
                        s+=" "
                return s.strip()    
            except json.JSONDecodeError:
                return ""

    def transform_text(self,text):
        if not isinstance(text,str):
            return ""
        
        text=text.lower()
        tokens=nltk.word_tokenize(text)

        cleaned_tokens=[
            self.ps.stem(word) for word in tokens if word.isalpha() and word not in string.punctuation and word not in stopwords.words('english')
        ]

        return " ".join(cleaned_tokens)
    
    def apply_transformation(self,df):
        columns_to_process = ['crew', 'genres', 'keywords', 'overview', 'tagline', 'cast']
        df[columns_to_process] = df[columns_to_process].fillna("")
    
        df['crew']=df['crew'].apply(lambda x:self.extract_data(x,target_job='Director'))
        df['genres']=df['genres'].apply(lambda x:self.extract_data(x))
        df['keywords']=df['keywords'].apply(lambda x:self.extract_data(x))
        df['overview']=df['overview'].apply(lambda x:self.extract_data(x))
        df['tagline']=df['tagline'].apply(lambda x:self.extract_data(x))
        df['cast']=df['cast'].apply(lambda x:self.extract_cast_names(x))
        df['finalcol']=(df['cast']+" "+df['crew']+" "+df['overview']+" "+df['genres']+" "+df['tagline']+" "+df['keywords'])
        df['finalcol']=df['finalcol'].apply(lambda x:x.lower())

        return df
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        return self.apply_transformation(X)
    
    def get_transformer_object(self):
        try:
            df=pd.read_csv('artifacts/data.csv')

            df.drop(columns=['status', 'movie_id', 'budget', 'homepage', 'id', 'original_language', 
                             'original_title', 'popularity', 'production_countries', 
                             'revenue', 'vote_count', 'production_companies', 
                             'spoken_languages'], inplace=True)
    
            pipeline=Pipeline(
                [
                    ("data_transformation",DataTransformation())
                ]
            )

            transformed_df=pipeline.fit_transform(df)

            transformed_df.to_csv('artifacts/transformed_data.csv',index=False,header=True)
            logging.info("data transformation done successfully")

            save_object(
                file_path=self.transformation_config.preprocessor_file_path,
                obj=pipeline
            )

            return transformed_df

            logging.info("preprocessor file saved successfully")


        except Exception as ep:
            raise custom_exception(ep,sys)
        
    
if __name__=='__main__':
    obj=DataTransformation()
    obj.get_transformer_object()