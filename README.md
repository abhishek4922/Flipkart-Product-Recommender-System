# Flipkart Product Recommendation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent product recommendation system that leverages a Retrieval-Augmented Generation (RAG) pipeline to provide context-aware suggestions based on real Flipkart product reviews. This project moves beyond traditional keyword-based search to understand the semantic meaning behind a user's query and match it with the most relevant products.

The application is built with a full-stack architecture, containerized for portability, and includes a complete MLOps monitoring stack for production-readiness.

## Features

- **Intelligent Semantic Search:** Utilizes a RAG pipeline with Groq and Llama-3.1 to understand user intent and provide nuanced recommendations.
- **Full-Stack Web Interface:** A user-friendly web UI built with Flask for easy interaction with the recommendation engine.
- **Containerized & Cloud-Ready:** Dockerized application with Kubernetes manifests for scalable and reproducible deployments.
- **Real-time Monitoring:** Integrated with Prometheus for metrics collection and Grafana for performance visualization and system health monitoring.
- **AstraDB Integration:** Uses AstraDB as a scalable vector store for efficient similarity searches on product review embeddings.

## System Architecture

```
+-----------------+      +---------------------+      +----------------------+
|   User via      |----->|    Flask Web App    |----->|      RAG Pipeline    |
|   Web Browser   |      | (app.py)            |      |   (rag_chain.py)     |
+-----------------+      +---------------------+      +----------+-----------+
                                |      ^                      |
                                |      | (Recommendations)    | (User Query)
                                v      |                      v
+----------------------+      +---------------------+      +----------------------+
| Prometheus           |<-----| Metrics Endpoint    |      |   Groq LLM API       |
| (Metrics Collection) |      | (/metrics)          |      | (llama-3.1-8b-instant) |
+----------------------+      +---------------------+      +----------------------+
       |                                                        ^
       v                                                        | (Context + Query)
+----------------------+                                        |
| Grafana              |      +----------------------+      +----------------------+
| (Visualization)      |      |   AstraDB            |<-----| Embedding Model      |
+----------------------+      | (Vector Store)       |      | (BAAI/bge-base-en-v1.5)|
                              +----------------------+      +----------------------+
```

## Tech Stack

- **Backend:** Python, Flask
- **ML/RAG:** LangChain, Groq, HuggingFace Transformers
- **Vector Database:** AstraDB
- **Frontend:** HTML, CSS
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **Monitoring:** Prometheus, Grafana
- **Data Handling:** Pandas, python-dotenv

## Setup and Local Installation

### Prerequisites

- Git
- Python 3.9+
- An account with [AstraDB](https://astra.datastax.com/) and [Groq](https://groq.com/) to get API keys.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd flipkart_product_recommendation
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Set Up Environment Variables

Create a file named `.env` in the root of the project directory and add the following credentials.

```env
ASTRA_DB_API_ENDPOINT="YOUR_ASTRA_DB_API_ENDPOINT"
ASTRA_DB_APPLICATION_TOKEN="YOUR_ASTRA_DB_APPLICATION_TOKEN"
ASTRA_DB_KEYSPACE="YOUR_ASTRA_DB_KEYSPACE"
GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## Deployment (Docker & Kubernetes)

This application is ready for a cloud-native deployment.

### 1. Build the Docker Image

```bash
docker build -t flipkart-recommender:latest .
```

### 2. Deploy to Kubernetes

Ensure you have a Kubernetes cluster running (e.g., Minikube, Kind, or a cloud provider's cluster) and `kubectl` is configured.

```bash
# Deploy the main application
kubectl apply -f flask-deployment.yaml

# Deploy the monitoring stack
kubectl apply -f prometheus/prometheus-configmap.yaml
kubectl apply -f prometheus/prometheus-deployment.yaml
kubectl apply -f grafana/grafana-deployment.yaml
```

## Monitoring

- **Prometheus:** To access the Prometheus UI, you can port-forward the service:
  ```bash
  kubectl port-forward svc/prometheus 9090:9090
  ```
  Access it at `http://localhost:9090`.

- **Grafana:** To access the Grafana dashboard:
  ```bash
  kubectl port-forward svc/grafana 3000:3000
  ```
  Access it at `http://localhost:3000`.

## Project Structure

```
.
├───app.py                  # Main Flask application
├───Dockerfile              # Docker configuration for the app
├───flask-deployment.yaml   # Kubernetes deployment for Flask app
├───requirements.txt        # Python dependencies
├───data/
│   └───flipkart_product_review.csv # Dataset
├───flipkart/               # Core application logic
│   ├───config.py           # Handles environment variables
│   ├───data_ingestion.py   # Logic for ingesting and processing data
│   └───rag_chain.py        # The RAG implementation
├───prometheus/             # Kubernetes configs for Prometheus
├───grafana/                # Kubernetes configs for Grafana
├───templates/
│   └───index.html          # Frontend HTML
└───static/
    └───style.css           # Frontend CSS
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
