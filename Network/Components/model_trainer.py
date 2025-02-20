import os
import sys
from pathlib import Path

from Network.exception.exception import NetworkException 
from Network.logging.logger import logging

from Network.entity.artifact_entity import DataTransformationArtifact,ClassificationMetricArtifact,ModelTrainerArtifact
from Network.entity.config_entity import ModelTrainerConfig
from dataclasses import dataclass, asdict

import pandas as pd
import numpy as np
from Network.entity.estimator import NetworkModel
from Network.utils.main_utils import save_object,load_object
from Network.utils.main_utils import load_numpy_array_data,write_yaml_file
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf  import ModelFactory
#from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
#from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow
from urllib.parse import urlparse

import dagshub

MLFLOW_TRACKING_URI='https://dagshub.com/judirispah/Network-Security-System.mlflow'

dagshub.init(repo_owner='judirispah', repo_name='Network-Security-System', mlflow=True)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkException(e,sys)
    def track_mlflow(self,best_model,classificationmetric:ClassificationMetricArtifact):

        mlflow.set_registry_uri(MLFLOW_TRACKING_URI)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme #http
        logging.info(tracking_url_type_store)

        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score
            accuracy_score=classificationmetric.accuracy_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.log_metric("accuracy_score",accuracy_score)


            # Model registry does not work with file store
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.sklearn.log_model(best_model, "model", registered_model_name=type(best_model).__name__)
            else:
                mlflow.sklearn.log_model(best_model, "model")



    
    def get_model_object_report(self,train:np.array,test:np.array):
        """
        Method Name :   get_model_object_and_report
        Description :   This function uses neuro_mf to get the best model object and report of the best model
        
        Output      :   Returns metric artifact object and best model object
        On Failure  :   Write an exception log and then raise an exception
        """

        try: 
            logging.info("Using neuro_mf to get best model object and report")
            model_factory=ModelFactory(self.model_trainer_config.model_config_file_path)
            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            best_model_detail = model_factory.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy
            ) 
            model_obj = best_model_detail.best_model

            y_pred=model_obj.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)  
            precision = precision_score(y_test, y_pred)  
            recall = recall_score(y_test, y_pred)  

            metric_artifact=ClassificationMetricArtifact(f1_score=f1,precision_score=precision,recall_score=recall,accuracy_score=accuracy) 

            return best_model_detail,metric_artifact

        except Exception as e:
            raise NetworkException(e, sys)
        
    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates a model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            train_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            best_model_detail,metric_artifact=self.get_model_object_report(train=train_arr,test=test_arr)
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            write_yaml_file(Path(self.model_trainer_config.model_trainer_dir)/'metrics.yaml',asdict(metric_artifact))
            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")
            else:
                network_model=NetworkModel(preprocessing_object=preprocessing_obj,trained_model_object=best_model_detail.best_model)
                logging.info("Created NETWORK model object with preprocessor and model")
                logging.info("Created best model file path.")

            save_object(self.model_trainer_config.trained_model_file_path, network_model)
            save_object("final_model/model.pkl",network_model)
            save_object("final_model/preprocessing.pkl",preprocessing_obj)

            self.track_mlflow(best_model_detail.best_model,metric_artifact)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkException(e, sys) from e

            
    

   