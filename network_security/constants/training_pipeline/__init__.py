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