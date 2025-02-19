import os
from datetime import date

DATABASE_NAME = "network_db"
COLLECTION_NAME = "network_tb"

PIPELINE_NAME: str = "Network"
ARTIFACT_DIR: str = "artifact"

TARGET_COLUMN = "phishing"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
FILE_NAME: str = "phishing.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
MODEL_FILE_NAME = "model.pkl"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DATABASE_NAME: str = "network_db"
DATA_INGESTION_COLLECTION_NAME: str = "network_tb"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.csv"
DATA_VALIDATION_SCHEMA_FILE: str = SCHEMA_FILE_PATH