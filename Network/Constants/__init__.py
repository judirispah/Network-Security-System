import os
from datetime import date
import numpy as np

DATABASE_NAME = "network_db"
COLLECTION_NAME = "network_tb"

PIPELINE_NAME: str = "Network"
ARTIFACT_DIR: str = "artifact"

TARGET_COLUMN = "Result"

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
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
DATA_VALIDATION_SCHEMA_FILE: str = SCHEMA_FILE_PATH

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}


"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")



MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
APP_HOST = "0.0.0.0"
APP_PORT = 8080