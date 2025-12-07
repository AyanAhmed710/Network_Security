import yaml
import os,sys
import numpy as np
import pickle
import dill
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecuritySystem
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
     

def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise Exception("No file path exists")
        with open(file_path,"rb")  as file:
            print(file.read)
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecuritySystem(e,sys)
    
def load_numpy_data(file_path):
    try:
        with open(file_path,"rb") as numpy_obj:
            return np.load(file_path)
    except Exception as e:
        raise NetworkSecuritySystem(e,sys)
    

def evaluate_models(x_train, x_test, y_train, y_test, models, params):
    try:
        report = {}

        model_names = list(models.keys())
        model_list = list(models.values())

        for i in range(len(model_list)):
            model = model_list[i]
            param = params[model_names[i]]

            # Grid Search
            gs = GridSearchCV(model, param, cv=3)
            gs.fit(x_train, y_train)

            # Set best params
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            # Predictions
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            # Scores
            train_score = r2_score(y_train, y_train_pred)
            test_score = r2_score(y_test, y_test_pred)

            # Save best score for the model
            report[model_names[i]] = test_score

        return report   # OUTSIDE the loop

    except Exception as e:
        raise NetworkSecuritySystem(e, sys)
