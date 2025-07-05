from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.logging.logger import logging
from scipy.stats import ks_2samp
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file
import pandas as pd
import os, sys


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

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

    def validate_number_of_columns(self, data_frame: pd.DataFrame) -> bool:
        """
        Validates the number of columns in the DataFrame against the schema configuration.
        """
        try:
            number_of_columns = len(data_frame.columns)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"DataFrame columns: {len(data_frame.columns)}")
            if len(data_frame.columns) != number_of_columns:
                logging.error(
                    f"Number of columns validation failed. Expected: {number_of_columns}, Found: {len(data_frame.columns)}"
                )
                return False

            logging.info("Number of columns validation passed.")
            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def detect_data_drift(
        self, base_dataframe, current_dataframe, threshold: float = 0.05
    ) -> bool:
        """
        Detects data drift between the base and current DataFrames using the Kolmogorov-Smirnov test.
        """
        try:
            is_found = None
            report = {}

            for column in base_dataframe.columns:
                d1 = base_dataframe[column]
                d2 = current_dataframe[column]
                is_sample_dist = ks_2samp(d1, d2)
                if threshold <= is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                report.update(
                    {
                        column: {
                            "p_value": is_sample_dist.pvalue,
                            "is_drifted": is_found,
                        }
                    }
                )

            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Create directory if it does not exist
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation process...")
            print("Starting data validation process...")

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test file
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = (
                    f"Train DataFrame validation failed for number of columns."
                )

            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = (
                    f"Test DataFrame validation failed for number of columns."
                )

            ## check data drift
            status = self.detect_data_drift(
                base_dataframe=train_dataframe,
                current_dataframe=test_dataframe,
            )
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifact = DataValidationArtifact(
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                validation_status=status,
            )

            logging.info("Data validation completed successfully.")
            print("Data validation completed successfully.")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
