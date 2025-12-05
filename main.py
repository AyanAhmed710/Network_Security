from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecuritySystem
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestion=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestion)
        logging.info("Initiate the Data Ingestion")

        data_ingestion_artifact=dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        

    except Exception as e:
        raise NetworkSecuritySystem(e,sys)