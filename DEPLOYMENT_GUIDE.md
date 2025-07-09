# Deployment Guide

## 📋 Deployment Overview

This guide provides step-by-step instructions for deploying the Network Security MLOps Pipeline in various environments, from local development to production cloud deployments.

## 🚀 Deployment Options

### 1. Local Development Deployment
### 2. Docker Container Deployment
### 3. Cloud Deployment (AWS/GCP/Azure)
### 4. Kubernetes Deployment
### 5. CI/CD Pipeline Deployment

## 🏠 Local Development Deployment

### Prerequisites

- Python 3.8+
- MongoDB instance (local or cloud)
- Git
- Virtual environment tool (venv/conda)

### Step-by-Step Local Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd mlops-etl-pipeline-network-security
```

#### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n network-security python=3.8
conda activate network-security
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration
Create `.env` file in project root:
```env
MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/
MLFLOW_TRACKING_URI=https://dagshub.com/username/repository.mlflow
```

#### 5. Initialize Data
```bash
# Upload data to MongoDB
python push_data.py

# Run training pipeline
python main.py
```

#### 6. Start Application
```bash
# Start FastAPI server
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### 7. Access Application
- **API Documentation**: http://localhost:8000/docs
- **Training Endpoint**: http://localhost:8000/train
- **Prediction Interface**: http://localhost:8000/predict

## 🐳 Docker Container Deployment

### Docker Setup

#### 1. Create Dockerfile
```dockerfile
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs artifacts prediction_output final_model

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/docs || exit 1

# Run application
CMD ["python", "app.py"]
```

#### 2. Create .dockerignore
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.git/
.gitignore
README.md
.env
logs/
artifacts/
mlruns/
.pytest_cache/
.coverage
```

#### 3. Build Docker Image
```bash
docker build -t network-security-pipeline .
```

#### 4. Run Docker Container
```bash
# Basic run
docker run -p 8000:8000 network-security-pipeline

# With environment variables
docker run -p 8000:8000 \
  -e MONGO_DB_URL="mongodb+srv://username:password@cluster.mongodb.net/" \
  -e MLFLOW_TRACKING_URI="https://dagshub.com/username/repository.mlflow" \
  network-security-pipeline

# With volume mounts
docker run -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/final_model:/app/final_model \
  network-security-pipeline
```

#### 5. Docker Compose Setup
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_DB_URL=${MONGO_DB_URL}
      - MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
    volumes:
      - ./logs:/app/logs
      - ./artifacts:/app/artifacts
      - ./final_model:/app/final_model
      - ./prediction_output:/app/prediction_output
    depends_on:
      - mongodb
      - mlflow
    restart: unless-stopped

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongodb_data:/data/db

  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_BACKEND_STORE_URI=sqlite:///mlflow.db
    volumes:
      - mlflow_data:/mlflow
    command: mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0

volumes:
  mongodb_data:
  mlflow_data:
```

Run with Docker Compose:
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS Deployment

#### 1. EC2 Deployment

**Step 1: Launch EC2 Instance**
```bash
# Launch Ubuntu 20.04 LTS instance
# Security groups: HTTP (80), HTTPS (443), SSH (22), Custom (8000)
```

**Step 2: Connect and Setup**
```bash
# Connect to instance
ssh -i key.pem ubuntu@ec2-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Step 3: Deploy Application**
```bash
# Clone repository
git clone <repository-url>
cd mlops-etl-pipeline-network-security

# Set environment variables
export MONGO_DB_URL="your-mongodb-url"
export MLFLOW_TRACKING_URI="your-mlflow-uri"

# Build and run
docker-compose up -d
```

#### 2. ECS Deployment

**Step 1: Create Task Definition**
```json
{
  "family": "network-security-pipeline",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "network-security-app",
      "image": "your-ecr-repo/network-security-pipeline:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "MONGO_DB_URL",
          "value": "your-mongodb-url"
        },
        {
          "name": "MLFLOW_TRACKING_URI",
          "value": "your-mlflow-uri"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/network-security-pipeline",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Step 2: Create Service**
```bash
aws ecs create-service \
  --cluster your-cluster \
  --service-name network-security-service \
  --task-definition network-security-pipeline:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

### Google Cloud Platform (GCP)

#### 1. Cloud Run Deployment

**Step 1: Build and Push Image**
```bash
# Build image
docker build -t gcr.io/your-project/network-security-pipeline .

# Push to Container Registry
docker push gcr.io/your-project/network-security-pipeline
```

**Step 2: Deploy to Cloud Run**
```bash
gcloud run deploy network-security-service \
  --image gcr.io/your-project/network-security-pipeline \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONGO_DB_URL=your-mongodb-url,MLFLOW_TRACKING_URI=your-mlflow-uri
```

#### 2. GKE Deployment

**Step 1: Create Cluster**
```bash
gcloud container clusters create network-security-cluster \
  --zone us-central1-a \
  --num-nodes 3
```

**Step 2: Deploy Application**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: network-security-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: network-security
  template:
    metadata:
      labels:
        app: network-security
    spec:
      containers:
      - name: network-security-app
        image: gcr.io/your-project/network-security-pipeline:latest
        ports:
        - containerPort: 8000
        env:
        - name: MONGO_DB_URL
          value: "your-mongodb-url"
        - name: MLFLOW_TRACKING_URI
          value: "your-mlflow-uri"
```

### Azure Deployment

#### 1. Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name network-security-container \
  --image your-registry/network-security-pipeline:latest \
  --dns-name-label network-security-app \
  --ports 8000 \
  --environment-variables MONGO_DB_URL=your-mongodb-url MLFLOW_TRACKING_URI=your-mlflow-uri
```

#### 2. App Service

```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name network-security-app \
  --deployment-container-image-name your-registry/network-security-pipeline:latest
```

## ⚙️ Kubernetes Deployment

### Complete Kubernetes Setup

#### 1. Namespace
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: network-security
```

#### 2. ConfigMap
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: network-security-config
  namespace: network-security
data:
  MONGO_DB_URL: "mongodb+srv://username:password@cluster.mongodb.net/"
  MLFLOW_TRACKING_URI: "https://dagshub.com/username/repository.mlflow"
```

#### 3. Secret
```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: network-security-secret
  namespace: network-security
type: Opaque
data:
  mongo-url: <base64-encoded-mongo-url>
  mlflow-uri: <base64-encoded-mlflow-uri>
```

#### 4. Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: network-security-deployment
  namespace: network-security
spec:
  replicas: 3
  selector:
    matchLabels:
      app: network-security
  template:
    metadata:
      labels:
        app: network-security
    spec:
      containers:
      - name: network-security-app
        image: network-security-pipeline:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: network-security-config
        - secretRef:
            name: network-security-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /docs
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /docs
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 5. Service
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: network-security-service
  namespace: network-security
spec:
  selector:
    app: network-security
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### 6. Ingress
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: network-security-ingress
  namespace: network-security
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: network-security.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: network-security-service
            port:
              number: 80
```

#### 7. Deploy to Kubernetes
```bash
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Network Security Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Lint code
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t network-security-pipeline:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push network-security-pipeline:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

### Jenkins Pipeline

Create `Jenkinsfile`:
```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'network-security-pipeline'
        REGISTRY = 'your-registry'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh 'python -m pytest tests/ -v'
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .'
            }
        }
        
        stage('Push') {
            steps {
                sh 'docker push ${REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'kubectl set image deployment/network-security-deployment network-security-app=${REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

## 🔐 Security Best Practices

### 1. Environment Variables
- Use secrets management systems
- Never commit sensitive data to version control
- Use encrypted environment variables

### 2. Network Security
- Use HTTPS/TLS for all communications
- Implement proper firewall rules
- Use VPC/private networks in cloud deployments

### 3. Container Security
- Use minimal base images
- Regularly update dependencies
- Scan images for vulnerabilities

### 4. Access Control
- Implement proper authentication
- Use role-based access control (RBAC)
- Regular access reviews

## 📊 Monitoring and Logging

### 1. Application Monitoring
```yaml
# monitoring.yaml
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
```

### 2. Logging Setup
```yaml
# logging.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
data:
  fluent-bit.conf: |
    [INPUT]
        Name tail
        Path /var/log/containers/*.log
        Parser json
    [OUTPUT]
        Name elasticsearch
        Match *
        Host elasticsearch.logging.svc.cluster.local
        Port 9200
```

## 🧪 Testing Deployment

### Health Check Script
```python
import requests
import sys

def health_check(base_url):
    try:
        # Test docs endpoint
        response = requests.get(f"{base_url}/docs")
        if response.status_code != 200:
            return False
        
        # Test training endpoint
        response = requests.get(f"{base_url}/train")
        if response.status_code != 200:
            return False
        
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    if health_check(base_url):
        print("Deployment successful!")
        sys.exit(0)
    else:
        print("Deployment failed!")
        sys.exit(1)
```

### Load Testing
```bash
# Using ab (Apache Bench)
ab -n 1000 -c 10 http://localhost:8000/docs

# Using wrk
wrk -t12 -c400 -d30s http://localhost:8000/docs
```

## 🔧 Troubleshooting

### Common Issues

1. **Container won't start**
   - Check logs: `docker logs container-name`
   - Verify environment variables
   - Check file permissions

2. **Database connection issues**
   - Verify MongoDB URL
   - Check network connectivity
   - Verify SSL certificates

3. **Memory/CPU issues**
   - Increase resource limits
   - Optimize code performance
   - Use horizontal scaling

### Debugging Commands

```bash
# Check container status
docker ps -a

# View logs
docker logs -f container-name

# Execute into container
docker exec -it container-name /bin/bash

# Check Kubernetes resources
kubectl get pods -n network-security
kubectl describe pod pod-name -n network-security
kubectl logs pod-name -n network-security
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Azure Container Instances](https://docs.microsoft.com/en-us/azure/container-instances/)

---

This deployment guide provides comprehensive instructions for deploying the Network Security MLOps Pipeline across various environments and platforms.
