# User Guide

## 📋 Overview

This user guide provides comprehensive instructions for using the Network Security MLOps Pipeline application. Whether you're a data scientist, ML engineer, or end user, this guide will help you effectively use the system for phishing detection and network security analysis.

## 👥 Target Audience

- **Data Scientists**: Training models and analyzing results
- **ML Engineers**: Deploying and monitoring the pipeline
- **Security Analysts**: Making predictions on network data
- **End Users**: Uploading data for phishing detection

## 🚀 Getting Started

### Prerequisites

Before using the application, ensure you have:
- Access to the deployed application (web interface)
- Network security data in CSV or Excel format
- Basic understanding of machine learning concepts
- (Optional) MongoDB connection for data ingestion

### System Requirements

- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **File Formats**: CSV (.csv) or Excel (.xlsx)
- **Internet Connection**: Required for cloud-based deployments
- **File Size**: Maximum 16MB per upload

## 🌐 Accessing the Application

### Web Interface

1. **Navigate to the application URL**
   - Local development: `http://localhost:8000`
   - Production: `https://your-domain.com`

2. **Main page redirect**
   - The root URL (`/`) automatically redirects to the API documentation
   - Interactive documentation is available at `/docs`

### API Documentation

The application provides interactive API documentation:
- **Swagger UI**: Accessible at `/docs`
- **OpenAPI Schema**: Available at `/openapi.json`
- **Interactive testing**: Built-in request/response testing

## 📊 Understanding the Data

### Input Data Format

The application expects data with 30 specific features related to website characteristics:

#### URL & Domain Features
| Feature | Description | Values |
|---------|-------------|---------|
| having_IP_Address | URL contains IP address | 0 (No) / 1 (Yes) |
| URL_Length | Length of the URL | Integer |
| Shortining_Service | URL shortening service used | 0 (No) / 1 (Yes) |
| having_At_Symbol | @ symbol in URL | 0 (No) / 1 (Yes) |
| double_slash_redirecting | Double slash in URL path | 0 (No) / 1 (Yes) |
| Prefix_Suffix | Prefix/suffix in domain | 0 (No) / 1 (Yes) |
| having_Sub_Domain | Number of subdomains | Integer |

#### Security Features
| Feature | Description | Values |
|---------|-------------|---------|
| SSLfinal_State | SSL certificate status | 0/1/2 |
| Domain_registeration_length | Domain registration period | Integer |
| HTTPS_token | HTTPS token usage | 0 (No) / 1 (Yes) |
| Request_URL | External request URLs % | 0/1/2 |
| URL_of_Anchor | Anchor URL characteristics | 0/1/2 |
| Links_in_tags | Links in HTML tags | 0/1/2 |
| SFH | Server Form Handler | 0/1/2 |
| Submitting_to_email | Email submission | 0 (No) / 1 (Yes) |
| Abnormal_URL | URL abnormality | 0 (No) / 1 (Yes) |
| Redirect | Page redirection | 0/1/2 |
| on_mouseover | Mouse-over events | 0 (No) / 1 (Yes) |
| RightClick | Right-click behavior | 0 (No) / 1 (Yes) |
| popUpWidnow | Pop-up windows | 0 (No) / 1 (Yes) |
| Iframe | Iframe usage | 0 (No) / 1 (Yes) |

#### Technical Features
| Feature | Description | Values |
|---------|-------------|---------|
| Favicon | Favicon characteristics | 0/1/2 |
| port | Port usage | 0 (No) / 1 (Yes) |
| age_of_domain | Domain age | Integer |
| DNSRecord | DNS record status | 0 (No) / 1 (Yes) |
| web_traffic | Website traffic rank | 0/1/2 |
| Page_Rank | Google PageRank | 0/1/2 |
| Google_Index | Google indexing | 0 (No) / 1 (Yes) |
| Links_pointing_to_page | Inbound links count | 0/1/2 |

### Sample Data Format

#### CSV Example
```csv
having_IP_Address,URL_Length,Shortining_Service,having_At_Symbol,double_slash_redirecting,Prefix_Suffix,having_Sub_Domain,SSLfinal_State,Domain_registeration_length,Favicon,port,HTTPS_token,Request_URL,URL_of_Anchor,Links_in_tags,SFH,Submitting_to_email,Abnormal_URL,Redirect,on_mouseover,RightClick,popUpWidnow,Iframe,age_of_domain,DNSRecord,web_traffic,Page_Rank,Google_Index,Links_pointing_to_page
1,54,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

#### Excel Example
Create an Excel file with the same column headers and data values.

## 🔄 Using the Training Pipeline

### When to Train

Train a new model when:
- New data is available
- Model performance degrades
- Business requirements change
- Regular retraining schedule

### Training Process

1. **Access Training Endpoint**
   - Navigate to `http://your-domain.com/train`
   - Or use the API documentation interface

2. **Initiate Training**
   - Click "Execute" in the Swagger UI
   - Or make a GET request to `/train`

3. **Monitor Progress**
   - Training progress is logged in real-time
   - Check logs for detailed information
   - Wait for completion message

4. **Training Steps**
   The system automatically:
   - Connects to MongoDB
   - Extracts latest data
   - Validates data quality
   - Transforms features
   - Trains multiple models
   - Selects best performer
   - Saves model artifacts

### Training Output

After successful training:
- **Model artifacts**: Saved to `final_model/`
- **Training logs**: Available in `logs/`
- **Performance metrics**: Tracked in MLflow
- **Artifacts**: Timestamped in `artifacts/`

## 🔮 Making Predictions

### Prediction Process

1. **Prepare Your Data**
   - Ensure data has all 30 required features
   - Use CSV or Excel format
   - Verify data quality and formats

2. **Access Prediction Interface**
   - Navigate to `/predict` endpoint
   - Use the API documentation interface

3. **Upload Data File**
   - Click "Choose File" button
   - Select your CSV or Excel file
   - Click "Execute" to submit

4. **View Results**
   - Results displayed in HTML table format
   - Predictions added as new column
   - Original data preserved

### Prediction Output

The system returns:
- **HTML Table**: Formatted results in browser
- **Saved File**: Results saved to `prediction_output/predictions.csv`
- **Added Column**: `predicted_column` with values:
  - `0`: Legitimate website
  - `1`: Phishing website

### Example Prediction Workflow

1. **Prepare test data**:
   ```csv
   having_IP_Address,URL_Length,Shortining_Service,...
   1,54,1,...
   0,32,0,...
   ```

2. **Upload file** through web interface

3. **View results**:
   ```html
   <table>
   <tr>
     <th>having_IP_Address</th>
     <th>URL_Length</th>
     <th>predicted_column</th>
   </tr>
   <tr>
     <td>1</td>
     <td>54</td>
     <td>1</td>  <!-- Phishing -->
   </tr>
   <tr>
     <td>0</td>
     <td>32</td>
     <td>0</td>  <!-- Legitimate -->
   </tr>
   </table>
   ```

## 🛠️ Advanced Usage

### Using API Programmatically

#### Python Example
```python
import requests
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Make prediction request
files = {'file': open('your_data.csv', 'rb')}
response = requests.post('http://localhost:8000/predict', files=files)

# Process results
if response.status_code == 200:
    print("Prediction successful!")
    # Response contains HTML table
    html_results = response.text
else:
    print("Prediction failed:", response.text)
```

#### cURL Example
```bash
# Training
curl -X GET "http://localhost:8000/train"

# Prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_data.csv"
```

#### JavaScript Example
```javascript
// File upload for prediction
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.text())
.then(data => {
  document.getElementById('results').innerHTML = data;
});
```

### Batch Processing

For large datasets:

1. **Split large files** into smaller chunks
2. **Process sequentially** to avoid memory issues
3. **Combine results** from multiple requests
4. **Monitor performance** and adjust batch sizes

## 📊 Interpreting Results

### Prediction Values

| Value | Meaning | Action |
|-------|---------|--------|
| 0 | Legitimate website | Safe to access |
| 1 | Phishing website | Block or investigate |

### Confidence Levels

While the current model returns binary predictions, consider:
- **Model accuracy**: Check training metrics
- **Data quality**: Ensure input data is complete
- **Context**: Consider additional security measures

### Result Analysis

1. **High phishing predictions**: Investigate URLs manually
2. **Mixed results**: Review data quality and patterns
3. **All legitimate**: Verify data is representative

## 🔧 Troubleshooting

### Common Issues

#### 1. File Upload Errors

**Problem**: "Unsupported file format"
**Solution**: 
- Ensure file has `.csv` or `.xlsx` extension
- Check file is not corrupted
- Try saving in different format

**Problem**: File too large
**Solution**:
- Split large files into smaller chunks
- Compress data if possible
- Contact administrator for size limits

#### 2. Missing Features

**Problem**: "KeyError: 'feature_name'"
**Solution**:
- Verify all 30 features are present
- Check column names match exactly
- Review sample data format

#### 3. Data Format Issues

**Problem**: Invalid data types
**Solution**:
- Ensure all values are integers
- Check for missing values
- Verify data ranges (0, 1, 2 for categorical)

#### 4. Training Failures

**Problem**: Training endpoint not responding
**Solution**:
- Check system resources
- Verify MongoDB connection
- Review training logs

### Getting Help

1. **Check logs**: Review application logs for errors
2. **Validate data**: Ensure input data meets requirements
3. **Test connection**: Verify system is accessible
4. **Contact support**: Reach out to system administrators

## 📋 Best Practices

### Data Preparation

1. **Validate data quality** before upload
2. **Remove duplicates** and outliers
3. **Check feature completeness**
4. **Maintain data consistency**

### Model Usage

1. **Regular retraining** with new data
2. **Monitor prediction quality**
3. **Validate results** against known samples
4. **Document prediction contexts**

### Security Considerations

1. **Sanitize input data**
2. **Validate file sources**
3. **Monitor for suspicious patterns**
4. **Implement additional security checks**

## 📈 Performance Optimization

### File Upload Tips

1. **Use CSV format** for better performance
2. **Compress large files** before upload
3. **Split very large datasets**
4. **Upload during off-peak hours**

### Prediction Efficiency

1. **Batch similar requests**
2. **Cache frequent predictions**
3. **Monitor response times**
4. **Use appropriate file sizes**

## 📚 Additional Resources

### Documentation
- **API Documentation**: `/docs` endpoint
- **Technical Documentation**: See TECHNICAL_DOCUMENTATION.md
- **Deployment Guide**: See DEPLOYMENT_GUIDE.md

### Sample Data
- **Training data**: `network_data/phisingData.csv`
- **Test samples**: Available in repository
- **Schema definition**: `data_schema/schema.yaml`

### Support Channels
- **Issue tracker**: GitHub issues
- **Documentation**: Project README
- **Community**: Project discussions

## 🎯 Use Cases

### Security Operations Center (SOC)

1. **Daily threat analysis**
   - Upload daily URL feeds
   - Batch process suspicious domains
   - Generate security reports

2. **Real-time monitoring**
   - API integration with security tools
   - Automated threat detection
   - Alert generation

### Research and Development

1. **Model evaluation**
   - Test new feature sets
   - Compare model performance
   - Validate detection accuracy

2. **Data analysis**
   - Explore phishing patterns
   - Analyze feature importance
   - Generate insights

### Educational Purposes

1. **Learning ML concepts**
   - Understand classification models
   - Practice data preprocessing
   - Explore feature engineering

2. **Cybersecurity training**
   - Learn phishing detection
   - Understand threat vectors
   - Practice incident response

## 🔄 Workflow Examples

### Daily Security Monitoring

```
1. Collect URL data → 2. Format as CSV → 3. Upload to system → 
4. Review predictions → 5. Investigate threats → 6. Update blocklists
```

### Weekly Model Retraining

```
1. Gather new data → 2. Upload to MongoDB → 3. Trigger training → 
4. Evaluate performance → 5. Deploy if improved → 6. Update documentation
```

### Incident Response

```
1. Suspicious URL reported → 2. Create test dataset → 3. Get prediction → 
4. Analyze result → 5. Take action → 6. Document findings
```

---

This user guide provides comprehensive instructions for effectively using the Network Security MLOps Pipeline application for phishing detection and network security analysis.
