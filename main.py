from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
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

    except NetworkSecurityException as e:
        print(e)
        logging.error(f"An error occurred during data ingestion: {e}")
