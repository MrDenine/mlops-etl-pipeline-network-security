# API Documentation

## 📋 API Overview

This document provides comprehensive API documentation for the Network Security MLOps Pipeline FastAPI application. The API provides endpoints for training machine learning models and making predictions on network security data.

## 🌐 Base URL

```
http://localhost:8000
```

## 📡 API Endpoints

### 1. Root Endpoint

**Endpoint**: `GET /`

**Description**: Redirects to the API documentation

**Response**:
- **Status Code**: 307 (Temporary Redirect)
- **Location**: `/docs`

**Example**:
```bash
curl -X GET "http://localhost:8000/"
```

### 2. Training Endpoint

**Endpoint**: `GET /train`

**Description**: Initiates the complete machine learning training pipeline

**Tags**: `[Training]`

**Request**:
- **Method**: GET
- **Headers**: None required
- **Body**: None

**Response**:
- **Status Code**: 200 (Success)
- **Content-Type**: `text/plain`
- **Body**: "Training pipeline executed successfully."

**Error Responses**:
- **Status Code**: 500 (Internal Server Error)
- **Content-Type**: `application/json`
- **Body**: 
  ```json
  {
    "detail": "NetworkSecurityException: Error message details"
  }
  ```

**Example**:
```bash
curl -X GET "http://localhost:8000/train"
```

**Response Example**:
```
Training pipeline executed successfully.
```

### 3. Prediction Endpoint

**Endpoint**: `POST /predict`

**Description**: Accepts file upload (CSV/Excel) and returns predictions for network security data

**Tags**: `[Prediction]`

**Request**:
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Body**: File upload (CSV or Excel format)

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | CSV or Excel file containing network security data |

**Supported File Formats**:
- CSV (`.csv`)
- Excel (`.xlsx`)

**Response**:
- **Status Code**: 200 (Success)
- **Content-Type**: `text/html`
- **Body**: HTML table with predictions

**Error Responses**:
- **Status Code**: 400 (Bad Request)
  ```json
  {
    "detail": "Unsupported file format. Please upload a CSV or Excel file."
  }
  ```
- **Status Code**: 500 (Internal Server Error)
  ```json
  {
    "detail": "NetworkSecurityException: Error message details"
  }
  ```

**Example**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_data.csv"
```

**Response Example**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Prediction Results</title>
</head>
<body>
    <h1>Prediction Results</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>having_IP_Address</th>
                <th>URL_Length</th>
                <th>predicted_column</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>54</td>
                <td>1</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

### 4. API Documentation

**Endpoint**: `GET /docs`

**Description**: Interactive API documentation (Swagger UI)

**Response**:
- **Status Code**: 200 (Success)
- **Content-Type**: `text/html`
- **Body**: Swagger UI interface

**Example**:
```bash
curl -X GET "http://localhost:8000/docs"
```

### 5. OpenAPI Schema

**Endpoint**: `GET /openapi.json`

**Description**: OpenAPI schema in JSON format

**Response**:
- **Status Code**: 200 (Success)
- **Content-Type**: `application/json`
- **Body**: OpenAPI specification

## 📊 Data Schema

### Input Data Schema

The prediction endpoint expects data with the following 30 features:

| Feature | Type | Description |
|---------|------|-------------|
| having_IP_Address | int64 | Whether URL contains IP address |
| URL_Length | int64 | Length of the URL |
| Shortining_Service | int64 | Use of URL shortening service |
| having_At_Symbol | int64 | Presence of @ symbol in URL |
| double_slash_redirecting | int64 | Double slash in URL path |
| Prefix_Suffix | int64 | Presence of prefix/suffix in domain |
| having_Sub_Domain | int64 | Number of subdomains |
| SSLfinal_State | int64 | SSL certificate status |
| Domain_registeration_length | int64 | Domain registration period |
| Favicon | int64 | Favicon characteristics |
| port | int64 | Port usage |
| HTTPS_token | int64 | HTTPS token usage |
| Request_URL | int64 | External request URLs percentage |
| URL_of_Anchor | int64 | Anchor URL characteristics |
| Links_in_tags | int64 | Links in HTML tags |
| SFH | int64 | Server Form Handler characteristics |
| Submitting_to_email | int64 | Email submission behavior |
| Abnormal_URL | int64 | URL abnormality detection |
| Redirect | int64 | Page redirection behavior |
| on_mouseover | int64 | Mouse-over event behavior |
| RightClick | int64 | Right-click behavior |
| popUpWidnow | int64 | Pop-up window behavior |
| Iframe | int64 | Iframe usage |
| age_of_domain | int64 | Domain age |
| DNSRecord | int64 | DNS record status |
| web_traffic | int64 | Website traffic rank |
| Page_Rank | int64 | Google PageRank |
| Google_Index | int64 | Google indexing status |
| Links_pointing_to_page | int64 | Inbound links count |

### Output Data Schema

The prediction endpoint returns the input data with an additional column:

| Column | Type | Description |
|--------|------|-------------|
| predicted_column | int64 | Prediction result (0: Legitimate, 1: Phishing) |

## 🔧 CORS Configuration

The API is configured with CORS middleware to allow cross-origin requests:

```python
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📁 File Storage

### Prediction Output

Prediction results are automatically saved to:
- **Path**: `prediction_output/predictions.csv`
- **Format**: CSV with original data plus predictions
- **Overwrite**: Yes (each prediction overwrites the previous file)

### Model Artifacts

The API loads pre-trained models from:
- **Preprocessor**: `final_model/preprocessor.pkl`
- **Model**: `final_model/model.pkl`

## 🛠️ Error Handling

### Exception Types

| Exception | Description | HTTP Status |
|-----------|-------------|-------------|
| NetworkSecurityException | Custom application exceptions | 500 |
| FileNotFoundError | Model files not found | 500 |
| ValueError | Invalid input data | 400 |
| UnicodeDecodeError | File encoding issues | 400 |

### Error Response Format

```json
{
  "detail": "Error message describing the issue"
}
```

## 🔐 Security Considerations

### SSL/TLS Configuration

The application uses SSL certificate validation for MongoDB connections:

```python
import certifi
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
```

### Input Validation

- File format validation (CSV/Excel only)
- Data type validation
- Schema validation against expected features

### Environment Variables

Sensitive configuration is stored in environment variables:
- `MONGO_DB_URL`: MongoDB connection string
- `MLFLOW_TRACKING_URI`: MLflow tracking server URL

## 📈 Performance Considerations

### File Upload Limits

Default FastAPI file upload limits apply:
- **Max file size**: 16MB (configurable)
- **Memory usage**: Files are processed in memory

### Concurrent Requests

The API can handle multiple concurrent requests:
- **Training**: Only one training pipeline can run at a time
- **Prediction**: Multiple prediction requests can be processed concurrently

## 🧪 Testing the API

### Using curl

#### Training Request
```bash
curl -X GET "http://localhost:8000/train"
```

#### Prediction Request
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_data.csv"
```

### Using Python requests

```python
import requests

# Training
response = requests.get("http://localhost:8000/train")
print(response.text)

# Prediction
files = {'file': open('test_data.csv', 'rb')}
response = requests.post("http://localhost:8000/predict", files=files)
print(response.text)
```

### Using JavaScript fetch

```javascript
// Training
fetch('http://localhost:8000/train')
  .then(response => response.text())
  .then(data => console.log(data));

// Prediction
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.text())
.then(data => console.log(data));
```

## 📊 Sample Data

### CSV Format Example

```csv
having_IP_Address,URL_Length,Shortining_Service,having_At_Symbol,double_slash_redirecting,Prefix_Suffix,having_Sub_Domain,SSLfinal_State,Domain_registeration_length,Favicon,port,HTTPS_token,Request_URL,URL_of_Anchor,Links_in_tags,SFH,Submitting_to_email,Abnormal_URL,Redirect,on_mouseover,RightClick,popUpWidnow,Iframe,age_of_domain,DNSRecord,web_traffic,Page_Rank,Google_Index,Links_pointing_to_page
1,54,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

### Excel Format Example

| having_IP_Address | URL_Length | Shortining_Service | ... | Links_pointing_to_page |
|-------------------|------------|--------------------|----|------------------------|
| 1 | 54 | 1 | ... | 1 |
| 0 | 32 | 0 | ... | 0 |

## 🔄 API Versioning

Current API version: `v1`

Future versions will be available at:
- `http://localhost:8000/v2/train`
- `http://localhost:8000/v2/predict`

## 📚 Additional Resources

- **Interactive Documentation**: `http://localhost:8000/docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`
- **Health Check**: `http://localhost:8000/health` (if implemented)

## 🐛 Common Issues and Solutions

### 1. Model Files Not Found

**Error**: `FileNotFoundError: final_model/model.pkl`

**Solution**: 
```bash
# Run training pipeline first
python main.py
```

### 2. Invalid File Format

**Error**: `Unsupported file format`

**Solution**: Ensure file has `.csv` or `.xlsx` extension

### 3. Missing Features

**Error**: `KeyError: 'feature_name'`

**Solution**: Ensure all 30 required features are present in input data

### 4. MongoDB Connection Issues

**Error**: `pymongo.errors.ServerSelectionTimeoutError`

**Solution**: 
- Check `MONGO_DB_URL` environment variable
- Verify network connectivity
- Ensure SSL certificates are valid

---

This API documentation provides comprehensive information about all available endpoints, request/response formats, and usage examples for the Network Security MLOps Pipeline API.
