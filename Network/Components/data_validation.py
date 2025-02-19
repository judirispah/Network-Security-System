from Network.exception.exception import NetworkException
from Network.logging.logger import logging
from Network.entity.config_entity import DataValidationConfig
from Network.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Network.utils.main_utils import *
import json
import sys
from pandas import DataFrame
from scipy.stats import ks_2samp
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            
        except Exception as e:
            raise NetworkException(e,sys)
        
    @staticmethod
    def read_data(file_path) :
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkException(e, sys)  

    def validate_number_of_columns(self, dataframe) -> bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == 31
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise NetworkException(e, sys) 



    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame,threshold=0.05 ) -> bool:
        """
        Method Name :   detect_dataset_drift
        Description :   This method validates if drift is detected
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference_df, current_df)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report) 
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            #report={}
            #drift_status = False

            #for column in reference_df.columns:
                #df1=reference_df[column]
                #df2=current_df[column]
                #stat,p_value=ks_2samp(df1,df2)
                #drift_status = p_value < threshold # drift_detect

                #report[column] = {
            #"KS Statistic": round(stat, 4),
            #"P-Value": round(p_value, 4),
            #"Drift Status": drift_status}

            #if drift_status:
                #logging.info(f"🚨 Drift detected in column: {column}")
                #drift_status = True  # Update overall drift flag
            #else:
                #logging.info(f"✅ No drift detected in column: {column}")
            #df=pd.DataFrame.from_dict(report,orient="index")
            #df.to_csv(self.data_validation_config.drift_report_file_path, index_label="Column")

            return drift_status
        except Exception as e:
            raise NetworkException(e, sys) from e
        


    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")


            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkException(e, sys) from e        
                    
    
