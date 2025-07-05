from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
)
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Starting data ingestion process...")
        print("Starting data ingestion process...")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(
            f"Data ingestion completed successfully: {data_ingestion_artifact}"
        )
        print(f"Data ingestion completed successfully: {data_ingestion_artifact}")

        logging.info("Starting data validation process...")
        print("Starting data validation process...")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        logging.info("Initiating data validation...")
        data_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed successfully.")
        logging.info(f"Data Validation Artifact: {data_artifact}")
        print(f"Data Validation Artifact: {data_artifact}")

    except NetworkSecurityException as e:
        print(e)
        logging.error(f"An error occurred during data ingestion: {e}")
