import os
import numpy as np
import sys
import pandas as pd


"""
Defining Common Constants for Training Pipeline
"""
TARGET_COLUMN="Result"
PIPELINE_NAME="NetworkSecurity"
ARTIFACT_DIR="Artifacts"
FILE_NAME="phishingData.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")
SAVED_MODEL_DIR=os.path.join("saved_models")











"""
Data Ingestion Related Constants
"""
DATA_INGESTION_COLLECTION_NAME="NetworkData"
DATA_INGESTION_DATABASE_NAME="AyanAI"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2



"""
Data Validation Related Constants
"""

DATA_VALIDATION_DIR_NAME="data validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="report.yaml"


"""
Data Transformation Related Constants
"""

DATA_TRANSFORMATION_DIR_NAME="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_NAME="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR_NAME="transformed_object"
PREPROCESSING_OBJ_FILE_NAME="preprocessing.pkl"

##knn imputer
DATA_TRANSFORMATION_IMPUTER_PARAMS={
    "missing_values" :np.nan,
    "n_neighbors" :3,
    "weights": "uniform"
}


"""
Data Trainer Related Constants
"""
MODEL_TRAINER_DIR_NAME="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_NAME="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE=0.6
MODEL_TRAINER_UNDERFITTING_OVERFITTING_THRESHOLD=0.05
