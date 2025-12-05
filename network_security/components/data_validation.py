from network_security.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecuritySystem
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import sys,os
from network_security.utils.main_utils.utils import read_yaml_file,write_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
    @staticmethod #As it will only be used once
    def read_csv(file_path):
        try:
            df=pd.read_csv(file_path)
            return df

        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
        
    def validate_columns(self,dataframe):
        try:
            number_of_columns=len(self.schema_config)
            logging.info(f"Required number of columns {number_of_columns}")
            logging.info(f"DataFrame has columns {len(dataframe.columns)}")

            if len(dataframe.columns)==number_of_columns:
                return True
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
        
    def validate_data_type(self,dataframe):
        try:
            for key,values in self.schema_config.items():
                if values=="int64":
                    return True
                
            return False
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05):
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold <=is_sample_dist.pvalue:
                    is_found=False

                else :
                    is_found=True
                    status=False

                report.update({column:{"p_value":float(is_sample_dist.pvalue),status:is_found}})

                

            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)

            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,replace=True)
        except Exception as e:
            raise NetworkSecuritySystem(e,sys)


        

    def initiate_data_validation(self) ->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_dataframe=DataValidation.read_csv(train_file_path)
            test_dataframe=DataValidation.read_csv(test_file_path)

            status=self.validate_columns(train_dataframe)
            if not status:
                error_message=f"Trained dataframe does not contain all columns "

            status=self.validate_columns(test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all columns "

            status=self.validate_data_type(train_dataframe)
            if not status:
                error_message=f"Train dataframe has no int datatype"

            status=self.validate_data_type(test_dataframe)
            if not status:
                error_message=f"Test dataframe has no int datatype"

            status=self.detect_dataset_drift(train_dataframe,test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,header=True,index=False
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,header=True,index=False
            )


            data_validation_artifact = DataValidationArtifact(
                      validation_status=status,
                        valid_train_file_path=self.data_validation_config.valid_train_file_path,
                       valid_test_file_path=self.data_validation_config.valid_test_file_path,
                         invalid_train_file_path=None,
                           invalid_test_file_path=None,
                         drift_report_file_path=self.data_validation_config.drift_report_file_path
                           )
            

            return data_validation_artifact


        except Exception as e:
            raise NetworkSecuritySystem(e,sys)



