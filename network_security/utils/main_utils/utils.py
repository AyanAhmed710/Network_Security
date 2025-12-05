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