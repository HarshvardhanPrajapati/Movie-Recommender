import os
import sys
import dill
import pickle

from src.exception import custom_exception

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file:
            dill.dump(obj,file)
        
    except Exception as ep:
        raise custom_exception(ep,sys)
    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
        
    except Exception as ep:
        raise custom_exception(ep,sys)
    