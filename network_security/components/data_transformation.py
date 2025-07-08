import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
)

from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)

from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact,
    ):
        try:
            self.data_validation_artifact: DataValidationArtifact = (
                data_validation_artifact
            )
            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads data from the specified file path and returns a DataFrame.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def get_data_transformation_object(cls) -> Pipeline:
        """
        It initializes a KNNImputer with the specified parameters and returns a Pipeline object.

        Args:
            cls: DataTransformation

        Returns:
            Pipeline: A scikit-learn Pipeline object containing the KNNImputer.
        """
        logging.info("Entering the get_data_transformation_object method")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialized KNNImputer with parameters: {DATA_TRANSFORMATION_IMPUTER_PARAMS}",
            )

            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            train_dataframe = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_dataframe = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            ## training dataframe
            input_feature_train_dataframe = train_dataframe.drop(
                columns=[TARGET_COLUMN], axis=1
            )
            target_feature_train_dataframe = train_dataframe[TARGET_COLUMN]
            target_feature_train_dataframe = target_feature_train_dataframe.replace(
                -1, 0
            )

            ## testing dataframe
            input_feature_test_dataframe = train_dataframe.drop(
                columns=[TARGET_COLUMN], axis=1
            )
            target_feature_test_dataframe = train_dataframe[TARGET_COLUMN]
            target_feature_test_dataframe = target_feature_test_dataframe.replace(-1, 0)

            preprocessor = self.get_data_transformation_object()
            preprocessor_object = preprocessor.fit(input_feature_train_dataframe)
            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_dataframe
            )
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_dataframe
            )

            train_array = np.c_[
                transformed_input_train_feature,
                np.array(target_feature_train_dataframe),
            ]
            test_array = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_dataframe)
            ]

            ## save numpy array data
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_train_file_path,
                array=train_array,
            )
            save_numpy_array_data(
                file_path=self.data_transformation_config.transformed_test_file_path,
                array=test_array,
            )
            save_object(
                file_path=self.data_transformation_config.transformed_object_file_path,
                obj=preprocessor_object,
            )

            ## Save preprocessor object to final model path
            save_object(
                file_path="final_model/preprocessor.pkl",
                obj=preprocessor_object,
            )

            ## preparing artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
