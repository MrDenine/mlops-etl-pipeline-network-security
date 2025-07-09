# MLOps ETL Pipeline for Network Security

## 📋 Project Overview

This project implements a comprehensive MLOps ETL (Extract, Transform, Load) pipeline for network security data analysis and phishing detection. The system uses machine learning to identify potential phishing websites based on various network and URL characteristics.

## 🎯 Objective

The primary goal is to create an end-to-end machine learning pipeline that:
- Ingests network security data from MongoDB
- Validates and transforms the data
- Trains a machine learning model for phishing detection
- Provides a web interface for real-time predictions
- Maintains model versioning and monitoring with MLflow

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Source   │    │   Data Storage  │    │   Web Interface │
│   (MongoDB)     │───▶│   (CSV Files)   │───▶│   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Data Ingestion  │    │ Data Validation │    │ Data Transform  │
│   Component     │───▶│   Component     │───▶│   Component     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │ Model Training  │
                                              │   Component     │
                                              └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │ Model Serving & │
                                              │   Prediction    │
                                              └─────────────────┘
```

## 📊 Dataset Features

The dataset contains 30 features related to website characteristics:

### URL & Domain Features
- `having_IP_Address`: Whether URL contains IP address
- `URL_Length`: Length of the URL
- `Shortining_Service`: Use of URL shortening service
- `having_At_Symbol`: Presence of @ symbol in URL
- `double_slash_redirecting`: Double slash in URL path
- `Prefix_Suffix`: Presence of prefix/suffix in domain
- `having_Sub_Domain`: Number of subdomains

### Security Features
- `SSLfinal_State`: SSL certificate status
- `Domain_registeration_length`: Domain registration period
- `HTTPS_token`: HTTPS token usage
- `Request_URL`: External request URLs percentage
- `URL_of_Anchor`: Anchor URL characteristics
- `Links_in_tags`: Links in HTML tags
- `SFH`: Server Form Handler characteristics
- `Submitting_to_email`: Email submission behavior
- `Abnormal_URL`: URL abnormality detection
- `Redirect`: Page redirection behavior
- `on_mouseover`: Mouse-over event behavior
- `RightClick`: Right-click behavior
- `popUpWidnow`: Pop-up window behavior
- `Iframe`: Iframe usage

### Technical Features
- `Favicon`: Favicon characteristics
- `port`: Port usage
- `age_of_domain`: Domain age
- `DNSRecord`: DNS record status
- `web_traffic`: Website traffic rank
- `Page_Rank`: Google PageRank
- `Google_Index`: Google indexing status
- `Links_pointing_to_page`: Inbound links count

### Target Variable
- `Result`: Phishing detection result (0: Legitimate, 1: Phishing)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB instance
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mlops-etl-pipeline-network-security
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   MLFLOW_TRACKING_URI=https://dagshub.com/username/repository.mlflow
   ```

5. **Initialize data schema**
   The project uses a YAML schema file located at `data_schema/schema.yaml` for data validation.

## 📁 Project Structure

```
mlops-etl-pipeline-network-security/
├── app.py                      # FastAPI web application
├── main.py                     # Main training pipeline execution
├── push_data.py               # Data ingestion to MongoDB
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup configuration
├── DockerFile                 # Docker configuration
├── README.md                  # Project documentation
├── artifacts/                 # Training artifacts by timestamp
├── data_schema/               # Data validation schema
├── final_model/               # Trained model artifacts
├── logs/                      # Application logs
├── network_data/              # Raw data files
├── network_security/          # Main package
│   ├── components/            # Pipeline components
│   ├── constants/             # Configuration constants
│   ├── entity/               # Data classes and entities
│   ├── exception/            # Custom exceptions
│   ├── logging/              # Logging configuration
│   ├── pipeline/             # Pipeline orchestration
│   └── utils/                # Utility functions
├── notebooks/                 # Jupyter notebooks
├── prediction_output/         # Prediction results
├── templates/                # HTML templates
└── tests/                    # Test files
```

## 🔧 Components

### 1. Data Ingestion (`network_security/components/data_ingestion.py`)
- Connects to MongoDB database
- Extracts network security data
- Splits data into training and testing sets
- Saves data to feature store

### 2. Data Validation (`network_security/components/data_validation.py`)
- Validates data schema against YAML configuration
- Checks for data drift
- Generates validation reports
- Separates valid and invalid data

### 3. Data Transformation (`network_security/components/data_transformation.py`)
- Handles missing values using KNN imputation
- Applies feature scaling and encoding
- Generates preprocessor object
- Saves transformed data arrays

### 4. Model Training (`network_security/components/model_trainer.py`)
- Trains multiple machine learning models
- Performs hyperparameter tuning
- Evaluates model performance
- Saves best model with MLflow tracking

### 5. Model Serving (`network_security/utils/ml_utils/model/estimator.py`)
- Loads trained model and preprocessor
- Provides prediction interface
- Handles batch predictions

## 🔄 Pipeline Execution

### Training Pipeline

Run the complete training pipeline:

```bash
python main.py
```

This executes the following steps:
1. Data ingestion from MongoDB
2. Data validation and drift detection
3. Data transformation and preprocessing
4. Model training and evaluation
5. Model artifact storage

### Web Application

Start the FastAPI web server:

```bash
python app.py
```

The application provides:
- **Training endpoint** (`/train`): Triggers the training pipeline
- **Prediction endpoint** (`/predict`): Accepts CSV/Excel files for batch predictions
- **Documentation** (`/docs`): Interactive API documentation

## 🌐 API Endpoints

### Training
- **POST** `/train`
  - Triggers the complete training pipeline
  - Returns training status

### Prediction
- **POST** `/predict`
  - Accepts file upload (CSV/Excel)
  - Returns predictions in HTML table format
  - Saves results to `prediction_output/predictions.csv`

### Documentation
- **GET** `/docs`
  - Interactive API documentation
  - Swagger UI interface

## 📊 Model Performance

The pipeline includes comprehensive model evaluation:
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Validation**: Cross-validation and holdout testing
- **Monitoring**: MLflow experiment tracking
- **Thresholds**: Expected accuracy > 60%

## 🐳 Docker Deployment

Build and run the Docker container:

```bash
docker build -t network-security-pipeline .
docker run -p 8000:8000 network-security-pipeline
```

## 📈 MLflow Integration

The project integrates with MLflow for:
- Experiment tracking
- Model versioning
- Performance monitoring
- Artifact management

Access MLflow UI through DagsHub or local setup.

## 🔐 Security Considerations

- Environment variables for sensitive data
- SSL/TLS certificate validation
- Input validation for file uploads
- Error handling and logging

## 📝 Logging

Comprehensive logging system:
- Timestamped log files in `logs/` directory
- Different log levels (INFO, ERROR, DEBUG)
- Component-specific logging
- Error tracking and debugging

## 🧪 Testing

Run tests using:

```bash
python -m pytest tests/
```

Test coverage includes:
- MongoDB connection testing
- Component unit tests
- Integration testing
- API endpoint testing

## 🔄 Continuous Integration

The pipeline supports CI/CD with:
- Automated testing
- Model validation
- Performance monitoring
- Deployment automation

## 📋 Configuration

### Training Pipeline Constants
- **Target Column**: `Result`
- **Pipeline Name**: `network_security`
- **Train/Test Split**: 80/20
- **Imputation**: KNN with k=3
- **Model Threshold**: 60% accuracy

### Data Validation
- Schema validation using YAML
- Data drift detection
- Missing value analysis
- Data type validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Krish Naik** for the MLOps bootcamp and guidance
- **MongoDB** for data storage solution
- **MLflow** for experiment tracking
- **FastAPI** for web framework
- **scikit-learn** for machine learning algorithms
---

**Note**: This is an educational project for learning MLOps concepts and best practices. For production use, additional security measures and optimizations should be implemented.
