import yaml
import os,sys
import numpy as np
import pickle
import dill
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecuritySystem

def read_yaml_file(file_path):
    try:
        with open(file_path,'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecuritySystem(e,sys)
    
def write_yaml_file(file_path,content,replace):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            with open(file_path,"w") as file:
                yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecuritySystem(e,sys)
    

def save_numpy_data(file_path,array):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,"wb") as file:
            np.save(file,array)
    except Exception as e:
        raise NetworkSecuritySystem(e,sys)
    

def save_object(file_path,obj):
     try:
        logging.info("Object is going to be transfered in the folder")
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,"wb") as file:
         pickle.dump(obj,file)

        logging.info("Object have been successfully been saved")
     except Exception as e:
        raise NetworkSecuritySystem(e,sys)