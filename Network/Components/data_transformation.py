import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from Network.Constants import DATA_TRANSFORMATION_IMPUTER_PARAMS

from Network.Constants import TARGET_COLUMN

from Network.entity.artifact_entity import (DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact
)

from Network.entity.config_entity import DataTransformationConfig
from Network.exception.exception import NetworkException 
from Network.logging.logger import logging
from Network.utils.main_utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkException(e, sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)  # ✅ Uses instance variable ,Using ** unpacks the dictionary into individual arguments.

           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkException(e,sys)
        

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
            
            
                logging.info("Got the preprocessor object")

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            ## training dataframe
                input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]

                target_feature_train_df = target_feature_train_df.replace(-1, 0)

            #testing dataframe
                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                target_feature_test_df = target_feature_test_df.replace(-1, 0)

                preprocessor=self.get_data_transformer_object()

                preprocessor_object=preprocessor.fit(input_feature_train_df)
                transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
                transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
             

                

                smt = SMOTE(sampling_strategy="minority")

                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    transformed_input_train_feature, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                logging.info("Applying SMOTEENN on testing dataset")

                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    transformed_input_test_feature, target_feature_test_df
                )

                logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")

                train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]
                #save numpy array data
                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("Saved the preprocessor object")

                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )



            #preparing artifacts

                data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)


            
        except Exception as e:
            raise NetworkException(e,sys)
    