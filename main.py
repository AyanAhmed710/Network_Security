from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecuritySystem
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.components.data_validation import DataValidation
import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestion=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestion)
        
        logging.info("Initiate the Data Ingestion")

        data_ingestion_artifact=dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data Ingestion Completed")
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        
        data_validation=DataValidation(data_ingestion_artifact,datavalidationconfig)
        logging.info("Data Validation has started")
        data_validation_Artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_Artifact)
        

    except Exception as e:
        raise NetworkSecuritySystem(e,sys)