# Flipkart Product Recommender

A conversational AI chatbot that recommends Flipkart products based on user queries. Given a query about a product, the app provides related products with the same or lower price by leveraging product reviews and implementing Retrieval-Augmented Generation (RAG) using LangChain and AstraDB.

## Features

- **Conversational AI Interface**: Interactive chatbot UI for natural product queries
- **RAG-Based Recommendations**: Uses Retrieval-Augmented Generation to provide context-aware product suggestions
- **Vector Search**: Leverages AstraDB for efficient vector similarity search
- **Chat History**: Maintains conversation context for follow-up questions
- **Monitoring & Observability**: Integrated Prometheus metrics and Grafana dashboards
- **Production Ready**: Includes Docker and Kubernetes deployment configurations

## Technology Stack

- **Backend Framework**: Flask
- **AI/ML Stack**:
  - LangChain (RAG pipeline)
  - OpenAI GPT-3.5-turbo (LLM)
  - OpenAI text-embedding-3-large (embeddings)
  - AstraDB (vector database)
- **Frontend**: HTML/CSS/JavaScript with Bootstrap
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker, Kubernetes

## Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│   Flask Web Application     │
│  (app.py)                   │
└──────────┬──────────────────┘
           │
           ▼
┌──────────────────────────────┐
│   RAG Chain Builder          │
│  - History-aware retriever   │
│  - Question answering chain  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│   AstraDB Vector Store       │
│  - Product reviews           │
│  - Semantic search           │
└──────────────────────────────┘
```

## Project Structure

```
Flipkart-Product-Recommender/
├── app.py                          # Main Flask application
├── flipkart/
│   ├── __init__.py
│   ├── config.py                   # Configuration and environment variables
│   ├── data_converter.py           # Convert CSV to LangChain documents
│   ├── data_ingestion.py           # Ingest data into AstraDB
│   └── rag_chain.py                # RAG chain implementation
├── utils/
│   ├── __init__.py
│   ├── custom_exception.py         # Custom exception handling
│   └── logger.py                   # Logging configuration
├── data/
│   └── flipkart_product_review.csv # Product reviews dataset
├── templates/
│   └── index.html                  # Chatbot UI
├── static/
│   └── style.css                   # Chatbot styling
├── prometheus/
│   ├── prometheus-configmap.yaml   # Prometheus configuration
│   └── prometheus-deployment.yaml  # Prometheus Kubernetes deployment
├── grafana/
│   └── grafana-deployment.yaml     # Grafana Kubernetes deployment
├── Dockerfile                      # Docker container configuration
├── flask-deployment.yaml           # Kubernetes deployment manifest
├── requirements.txt                # Python dependencies
└── setup.py                        # Package installation script
```

## Prerequisites

- Python 3.10+
- OpenAI API key
- AstraDB account and credentials
- Docker (for containerized deployment)
- Kubernetes cluster (for K8s deployment)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
ASTRA_DB_KEYSPACE=your_keyspace
OPENAI_API_KEY=your_openai_api_key
```

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Flipkart-Product-Recommender
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up your `.env` file with required credentials

5. Run the application:
```bash
python app.py
```

6. Access the chatbot at `http://localhost:8000`

### Docker Setup

1. Build the Docker image:
```bash
docker build -t flask-app:latest .
```

2. Run the container:
```bash
docker run -p 8000:5000 --env-file .env flask-app:latest
```

### Kubernetes Deployment

1. Create a Kubernetes secret with your credentials:
```bash
kubectl create secret generic llmops-secrets \
  --from-literal=ASTRA_DB_API_ENDPOINT=your_endpoint \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN=your_token \
  --from-literal=ASTRA_DB_KEYSPACE=your_keyspace \
  --from-literal=OPENAI_API_KEY=your_key
```

2. Deploy the application:
```bash
kubectl apply -f flask-deployment.yaml
```

3. Deploy Prometheus and Grafana:
```bash
kubectl apply -f prometheus/prometheus-configmap.yaml
kubectl apply -f prometheus/prometheus-deployment.yaml
kubectl apply -f grafana/grafana-deployment.yaml
```

## Data Ingestion

To ingest the product review data into AstraDB:

```python
from flipkart.data_ingestion import DataIngestion

# Ingest data (first time)
ingestor = DataIngestion()
vector_store = ingestor.ingest(load_existing=False)
```

Or run the data ingestion script directly:
```bash
python flipkart/data_ingestion.py
```

Note: Set `load_existing=True` in production to use the existing vector store without re-ingesting data.

## API Endpoints

- `GET /` - Main chatbot interface
- `POST /get` - Get chatbot response
  - Request body: `{ "msg": "your question" }`
  - Response: Text response with product recommendations
- `GET /metrics` - Prometheus metrics endpoint

## How It Works

1. **Data Ingestion**: Product reviews from CSV are converted to LangChain documents and embedded using OpenAI's text-embedding-3-large model
2. **Vector Storage**: Embeddings are stored in AstraDB for efficient similarity search
3. **Query Processing**: User queries are processed through a history-aware retriever that maintains conversation context
4. **RAG Pipeline**:
   - Retrieves top 3 relevant product reviews based on semantic similarity
   - Passes context to GPT-3.5-turbo for generating personalized recommendations
   - Maintains chat history for follow-up questions
5. **Response**: Returns product recommendations to the user through the chatbot UI

## Monitoring

The application exposes Prometheus metrics at `/metrics` endpoint, including:
- HTTP request counts
- Custom application metrics

Access Grafana dashboards to visualize application performance and user interactions.

## Configuration

Key configuration options in `flipkart/config.py`:

- `EMBEDDING_MODEL`: text-embedding-3-large
- `RAG_MODEL`: gpt-3.5-turbo
- Vector store retrieval: Top 3 results (k=3)
- Model temperature: 0.1 (for consistent responses)

## Development

To modify the system prompts or behavior:

1. **Contextualization Prompt**: Edit in `flipkart/rag_chain.py:30-34` (converts questions to standalone format)
2. **QA Prompt**: Edit in `flipkart/rag_chain.py:36-41` (defines chatbot personality and response style)
3. **Retrieval Parameters**: Modify `search_kwargs` in `flipkart/rag_chain.py:28`

## Troubleshooting

- **AstraDB Connection Issues**: Verify your API endpoint and token in `.env`
- **OpenAI API Errors**: Check your API key and quota limits
- **Port Conflicts**: Default port is 8000, change in `app.py:45` if needed
- **Data Ingestion Fails**: Ensure the CSV file exists at `data/flipkart_product_review.csv`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available for educational and personal use.

## Author

Kartikeya

## Acknowledgments

- Built with LangChain framework
- Powered by OpenAI models
- Vector storage by DataStax AstraDB
