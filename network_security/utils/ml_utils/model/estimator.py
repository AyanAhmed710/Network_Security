import os
import sys

from network_security.exception.exception import NetworkSecuritySystem
from network_security.logging.logger import logging

from network_security.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME


class Network_Model:
    def __init__(self,preprocessor,model):
        try:
         self.preprocessor=preprocessor
         self.model=model

        except Exception as e:
           raise NetworkSecuritySystem(e,sys)
        

    def predict(self,x):
       try:
          x_transform=self.preprocessor.transform(x)
          y_hat=self.model.predict(x_transform)

       except Exception as e:
          raise NetworkSecuritySystem(e,sys)