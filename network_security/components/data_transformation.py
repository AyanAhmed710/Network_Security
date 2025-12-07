import sys
import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact

from network_security.exception.exception import NetworkSecuritySystem
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataTransformationConfig
from network_security.utils.main_utils.utils import save_numpy_data,save_object



class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
        
    @staticmethod #As it will only be used once
    def read_csv(file_path):
        try:
            df=pd.read_csv(file_path)
            return df

        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
        

    def get_data_transformation_pipeline(self)->Pipeline:
        """
        get_data_transformation_pipeline it will uses KNN imputer for missing value
        
        :param cls: Data transformation
        :return: Description
        :rtype: Pipeline 
        """
        logging.info("get_data_transformer_object method of transformation class")

        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            logging.info(f"Initialize KNN iwth these params {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor = Pipeline([
                            ("imputer", imputer)
                                  ])

            return processor
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)

    def initiate_data_transformation(self):
        logging.info("Inititae data transformation")
        try:
            logging.info("Starting data transformation")
            train_df=self.read_csv(self.data_validation_artifact.valid_train_file_path)
            

            input_feature_df_train=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_df_train=train_df[TARGET_COLUMN]
            target_feature_df_train=target_feature_df_train.replace(-1,0)

            test_df=self.read_csv(self.data_validation_artifact.valid_test_file_path)
            input_feature_df_test=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_df_test=test_df[TARGET_COLUMN]
            target_feature_df_test=target_feature_df_test.replace(-1,0)

            preprocessor=self.get_data_transformation_pipeline()

            preprocessor_obj=preprocessor.fit(input_feature_df_train)
            transformed_input_data_train=preprocessor.transform(input_feature_df_train)
            transformed_input_data_test=preprocessor.transform(input_feature_df_test)


            train_arr=np.c_[transformed_input_data_train,np.array(target_feature_df_train)]
            test_arr=np.c_[transformed_input_data_test,np.array(target_feature_df_test)]


            save_numpy_data(self.data_transformation_config.train_data_transformation_dir,array=train_arr)
            save_numpy_data(self.data_transformation_config.test_data_transformation_dir,array=test_arr)
            save_object(self.data_transformation_config.object_data_transformation_dir,preprocessor_obj)

            save_object("final_Model/preprocessing.pkl",preprocessor_obj)

            #Preparing Artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.object_data_transformation_dir,
                transformed_test_file_path=self.data_transformation_config.test_data_transformation_dir,
                transoformed_train_file_path=self.data_transformation_config.train_data_transformation_dir
            )

            return data_transformation_artifact



        except Exception as e:
            raise NetworkSecuritySystem(e,sys)