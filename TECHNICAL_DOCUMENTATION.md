# Technical Documentation

## 📋 Technical Overview

This document provides in-depth technical details about the MLOps ETL Pipeline for Network Security project, including architecture decisions, implementation details, and technical specifications.

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 MLOps Pipeline                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    Data     │  │    Data     │  │    Data     │  │   Model     │         │
│  │  Ingestion  │─▶│ Validation  │─▶│Transformation│─▶│  Training   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                          Infrastructure Layer                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   MongoDB   │  │   MLflow    │  │   FastAPI   │  │   Docker    │         │
│  │  Database   │  │  Tracking   │  │  Web App    │  │ Container   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### Data Flow Architecture
```
Raw Data (MongoDB) → Data Ingestion → Feature Store → Data Validation → 
Data Transformation → Model Training → Model Artifacts → Prediction Service
```

#### Error Handling Flow
```
Component → NetworkSecurityException → Logger → Log Files → Monitoring
```

#### Configuration Flow
```
Constants → Config Entities → Pipeline Components → Artifacts
```

## 🔧 Technical Implementation Details

### 1. Data Ingestion Component

**File**: `network_security/components/data_ingestion.py`

**Key Features**:
- MongoDB connection with SSL certificate validation
- Configurable train-test split (default: 80/20)
- Feature store creation for data versioning
- Artifact generation for downstream components

**Technical Specifications**:
```python
# Configuration Constants
DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_NAME = "PHANUWAT"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2
```

**Input**: MongoDB collection with network security data
**Output**: DataIngestionArtifact with train/test file paths

### 2. Data Validation Component

**File**: `network_security/components/data_validation.py`

**Key Features**:
- Schema validation using YAML configuration
- Data drift detection using statistical methods
- Missing value analysis
- Data type validation

**Technical Specifications**:
```yaml
# Schema Configuration (data_schema/schema.yaml)
columns:
  - having_IP_Address: int64
  - URL_Length: int64
  - Shortining_Service: int64
  # ... additional 27 features
```

**Input**: DataIngestionArtifact
**Output**: DataValidationArtifact with validation status

### 3. Data Transformation Component

**File**: `network_security/components/data_transformation.py`

**Key Features**:
- KNN imputation for missing values
- Feature scaling and normalization
- Preprocessor object serialization
- Numpy array generation for model training

**Technical Specifications**:
```python
# KNN Imputer Configuration
DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
```

**Input**: DataValidationArtifact
**Output**: DataTransformationArtifact with transformed arrays

### 4. Model Training Component

**File**: `network_security/components/model_trainer.py`

**Key Features**:
- Multiple ML algorithm support
- Hyperparameter tuning
- Cross-validation
- MLflow experiment tracking
- Model performance evaluation

**Technical Specifications**:
```python
# Model Training Configuration
MODEL_TRAINER_EXPECTED_SCORE = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD = 0.05
```

**Input**: DataTransformationArtifact
**Output**: ModelTrainerArtifact with best model

## 🏛️ Entity Architecture

### Configuration Entities

**File**: `network_security/entity/config_entity.py`

#### TrainingPipelineConfig
```python
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.pipeline_name = "network_security"
        self.artifact_dir = os.path.join("artifacts", timestamp)
        self.model_dir = "final_model"
```

#### DataIngestionConfig
```python
class DataIngestionConfig:
    def __init__(self, training_pipeline_config):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir, "data_ingestion"
        )
        self.feature_store_file_path = "feature_store/phisingData.csv"
```

### Artifact Entities

**File**: `network_security/entity/artifact_entity.py`

#### DataIngestionArtifact
```python
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
```

#### ModelTrainerArtifact
```python
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: object
    test_metric_artifact: object
```

## 🔄 Pipeline Orchestration

### Training Pipeline

**File**: `network_security/pipeline/training_pipeline.py`

**Execution Flow**:
1. Initialize training pipeline configuration
2. Execute data ingestion
3. Perform data validation
4. Apply data transformation
5. Train and evaluate model
6. Save model artifacts

### Batch Prediction Pipeline

**File**: `network_security/pipeline/batch_prediction.py`

**Features**:
- Batch processing capabilities
- Model loading and prediction
- Results export functionality

## 🛠️ Utility Functions

### ML Utilities

**File**: `network_security/utils/ml_utils/model/estimator.py`

#### NetworkModel Class
```python
class NetworkModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model
    
    def predict(self, X):
        transformed_feature = self.preprocessor.transform(X)
        return self.model.predict(transformed_feature)
```

### Main Utilities

**File**: `network_security/utils/main_utils/utils.py`

**Key Functions**:
- `load_object()`: Deserialize saved objects
- `save_object()`: Serialize objects to disk
- `load_numpy_array_data()`: Load numpy arrays
- `save_numpy_array_data()`: Save numpy arrays

## 📊 Performance Metrics

### Classification Metrics

**File**: `network_security/utils/ml_utils/metric/classification_metric.py`

**Supported Metrics**:
- Accuracy Score
- Precision Score
- Recall Score
- F1 Score
- ROC AUC Score
- Confusion Matrix

## 🔐 Security Implementation

### Exception Handling

**File**: `network_security/exception/exception.py`

```python
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message
        self.error_details = error_details
```

### Logging System

**File**: `network_security/logging/logger.py`

**Features**:
- Timestamped log files
- Multiple log levels
- Structured logging format
- Centralized logging configuration

## 🐳 Docker Configuration

### Dockerfile Structure
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

## 🌐 FastAPI Web Application

### Application Structure

**File**: `app.py`

**Key Components**:
- CORS middleware configuration
- File upload handling
- Template rendering
- Error handling middleware

### API Endpoints

#### Training Endpoint
```python
@app.get("/train")
async def train_route():
    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()
    return Response("Training pipeline executed successfully.")
```

#### Prediction Endpoint
```python
@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    # File processing and prediction logic
    return templates.TemplateResponse("table.html", context)
```

## 📈 MLflow Integration

### Experiment Tracking
- Model parameters logging
- Metrics tracking
- Artifact storage
- Model versioning

### DagsHub Integration
- Remote experiment tracking
- Model registry
- Collaboration features
- Version control integration

## 🔧 Configuration Management

### Environment Variables
```env
MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/
MLFLOW_TRACKING_URI=https://dagshub.com/username/repository.mlflow
```

### Configuration Constants
- Pipeline parameters
- Model thresholds
- File paths
- Database configurations

## 🧪 Testing Strategy

### Unit Testing
- Component-level testing
- Mock external dependencies
- Isolated functionality testing

### Integration Testing
- End-to-end pipeline testing
- Database connectivity testing
- API endpoint testing

### Test Structure
```
tests/
├── unit/
│   ├── test_data_ingestion.py
│   ├── test_data_validation.py
│   └── test_model_trainer.py
├── integration/
│   ├── test_pipeline.py
│   └── test_api.py
└── test_mongodb.py
```

## 📊 Monitoring and Observability

### Application Monitoring
- Log aggregation
- Performance metrics
- Error tracking
- Resource utilization

### Model Monitoring
- Model performance tracking
- Data drift detection
- Prediction quality metrics
- Model degradation alerts

## 🔄 CI/CD Pipeline

### Continuous Integration
- Automated testing
- Code quality checks
- Security scanning
- Dependency updates

### Continuous Deployment
- Automated deployment
- Environment promotion
- Rollback capabilities
- Blue-green deployments

## 🚀 Performance Optimizations

### Data Processing
- Efficient data loading
- Memory optimization
- Batch processing
- Parallel processing

### Model Serving
- Model caching
- Prediction optimization
- Request batching
- Response compression

## 📋 Best Practices

### Code Quality
- Type hints
- Documentation
- Error handling
- Code reviews

### Security
- Input validation
- Authentication
- Authorization
- Data encryption

### Scalability
- Horizontal scaling
- Load balancing
- Caching strategies
- Database optimization

## 🔧 Troubleshooting Guide

### Common Issues
1. **MongoDB Connection Issues**
   - Check connection string
   - Verify SSL certificates
   - Network connectivity

2. **Model Training Failures**
   - Check data quality
   - Verify schema compliance
   - Resource availability

3. **Prediction Errors**
   - Input data validation
   - Model compatibility
   - Preprocessing issues

### Debug Commands
```bash
# Check logs
tail -f logs/latest.log

# Test MongoDB connection
python tests/test_mongodb.py

# Validate data schema
python -c "from network_security.components.data_validation import DataValidation; dv = DataValidation(); dv.validate_schema()"
```

## 📚 References

- [MLflow Documentation](https://mlflow.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Docker Documentation](https://docs.docker.com/)

---

This technical documentation provides comprehensive details about the implementation, architecture, and technical specifications of the MLOps ETL Pipeline for Network Security project.
