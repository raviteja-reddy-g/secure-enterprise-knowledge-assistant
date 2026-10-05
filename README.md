# Secure Enterprise Knowledge Assistant

A secure Retrieval-Augmented Generation (RAG) application for querying enterprise knowledge using natural language.

The project demonstrates an end-to-end AI knowledge retrieval architecture using Python, FastAPI, AWS S3, Amazon Bedrock, semantic embeddings, FAISS vector search, Docker, automated testing, and GitHub Actions CI.

> This repository is a sanitized portfolio implementation built to demonstrate enterprise AI architecture patterns. It does not contain proprietary employer code, customer data, production credentials, or confidential documents.

---

## Overview

Enterprise teams often store large amounts of operational knowledge across documents, policies, procedures, technical notes, and internal documentation.

Finding the correct information manually can be slow and inconsistent.

This project demonstrates a RAG-based knowledge assistant that:

1. Loads enterprise documents from Amazon S3.
2. Cleans and splits documents into smaller chunks.
3. Converts document chunks into semantic embeddings.
4. Stores embeddings in a FAISS vector index.
5. Retrieves the most relevant document chunks for a user question.
6. Sends the retrieved context to an Amazon Bedrock LLM.
7. Generates a grounded response through a FastAPI API.
8. Restricts sensitive operations using API-key-based authorization.

---

## Architecture

text
                 ┌─────────────────────┐
                 │      Amazon S3      │
                 │ Enterprise Documents│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     S3 Loader       │
                 │   boto3 / Python    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Document Processor  │
                 │ Clean + Chunk Text  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Embedding Model     │
                 │ all-MiniLM-L6-v2    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    FAISS Index      │
                 │ Semantic Retrieval  │
                 └──────────┬──────────┘
                            │
                     User Question
                            │
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 │   /ask endpoint     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Similarity Search   │
                 │ Top-K Retrieval     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Amazon Bedrock    │
                 │        LLM          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Grounded Response   │
                 └─────────────────────┘


---

## Technology Stack

- Python 3.11
- FastAPI
- Pydantic
- Amazon S3
- boto3
- Amazon Bedrock
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- Docker
- Python unittest
- GitHub Actions

---

## Project Structure

text
secure-enterprise-knowledge-assistant/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── document_processor.py
│   ├── ingestion_service.py
│   ├── main.py
│   ├── models.py
│   ├── rag_service.py
│   ├── s3_loader.py
│   ├── security.py
│   └── vector_store.py
│
├── tests/
│   └── test_security.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt


---

## Document Ingestion Pipeline

The administrator can trigger ingestion through:

text
POST /admin/ingest


The ingestion pipeline performs the following steps:

text
S3 Documents
      ↓
Document Loading
      ↓
Text Cleaning
      ↓
Recursive Text Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Index
      ↓
Persistent Local Vector Store


The current implementation supports text-based files including:

text
.txt
.md
.json


---

## Retrieval-Augmented Generation Flow

When an authorized user submits a question:

text
Question
   ↓
Semantic Similarity Search
   ↓
Top-K Relevant Chunks
   ↓
Retrieved Enterprise Context
   ↓
Prompt Construction
   ↓
Amazon Bedrock LLM
   ↓
Grounded Answer


The prompt instructs the model to answer using the retrieved enterprise context and avoid inventing unsupported information.

The default number of retrieved chunks is:

text
TOP_K_RESULTS=5


This value can be configured through environment variables.

---

## API Endpoints

### Health Check

http
GET /health


Example response:

json
{
  "status": "healthy"
}


### Ask a Question

http
POST /ask


Requires the HTTP header:

text
X-API-Key: <reader-or-admin-key>


Example request body:

json
{
  "question": "What is the enterprise incident escalation process?"
}


Example response format:

json
{
  "question": "What is the enterprise incident escalation process?",
  "answer": "The answer generated from retrieved enterprise context."
}


### Rebuild the Knowledge Index

http
POST /admin/ingest


Requires an administrator API key.

This endpoint loads supported documents from Amazon S3, chunks the content, creates embeddings, and rebuilds the FAISS vector index.

---

## Security

The project demonstrates two logical access levels:

### Reader

Reader credentials can access the question-answering endpoint.

text
POST /ask


### Administrator

Administrator credentials can access the question-answering endpoint and protected ingestion operations.

text
POST /admin/ingest


API keys are supplied through the:

text
X-API-Key


HTTP header.

Key comparisons use Python's:

python
hmac.compare_digest()


Environment variables are used for configuration so credentials are not stored directly in application source code.

This API-key implementation is intentionally lightweight for a portfolio application. A production enterprise deployment would typically integrate centralized identity and authorization technologies such as IAM, OAuth 2.0, OpenID Connect, JWT-based authentication, Amazon Cognito, or another enterprise identity provider.

---

## Environment Configuration

Copy the example configuration:

bash
cp .env.example .env


Configure the environment variables:

text
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-enterprise-documents-bucket
BEDROCK_MODEL_ID=your-bedrock-model-id

VECTOR_STORE_PATH=data/vector_store
TOP_K_RESULTS=5

READER_API_KEY=replace-with-reader-api-key
ADMIN_API_KEY=replace-with-admin-api-key


Never commit real API keys, AWS credentials, or production secrets to the repository.

AWS authentication should use the standard AWS credential chain, such as an authenticated AWS CLI profile, IAM role, or workload identity appropriate for the deployment environment.

---

## Running Locally

Create a Python virtual environment:

bash
python -m venv .venv


Activate the environment.

macOS/Linux:

bash
source .venv/bin/activate


Windows:

bash
.venv\Scripts\activate


Install dependencies:

bash
pip install -r requirements.txt


Start the API:

bash
uvicorn app.main:app --reload


The API will normally be available at:

text
http://localhost:8000


FastAPI interactive documentation:

text
http://localhost:8000/docs


---

## Running with Docker

Build the image:

bash
docker build -t secure-enterprise-knowledge-assistant .


Run the container:

bash
docker run --env-file .env -p 8000:8000 secure-enterprise-knowledge-assistant


The API will be available on port 8000.

---

## Automated Testing

Run the unit tests locally with:

bash
python -m unittest discover -s tests -p "test_*.py" -v


Current security tests validate:

- Matching API keys.
- Invalid API keys.
- Missing expected credentials.
- Reader authorization.
- Administrator authorization.
- Rejection of unauthorized reader requests.
- Rejection of unauthorized administrator requests.

---

## Continuous Integration

GitHub Actions automatically runs the CI workflow for pushes and pull requests targeting the main branch.

The pipeline performs:

text
Checkout Repository
        ↓
Set Up Python 3.11
        ↓
Upgrade pip
        ↓
Install Dependencies
        ↓
Compile / Syntax Validation
        ↓
Run Unit Tests


This helps detect syntax errors and test failures before changes are integrated.

---

## Design Decisions

### Why RAG Instead of Fine-Tuning?

RAG allows enterprise knowledge to remain outside the model while still providing relevant information at query time.

This makes it easier to update the knowledge base without retraining the underlying language model.

### Why FAISS?

FAISS provides efficient similarity search and is appropriate for demonstrating local semantic retrieval.

For larger production environments, the vector layer could be replaced by a managed or distributed vector-search platform.

### Why Amazon Bedrock?

Amazon Bedrock provides managed access to foundation models while integrating naturally with AWS-based enterprise architectures.

### Why FastAPI?

FastAPI provides request validation, automatic API documentation, dependency injection, and a lightweight Python API framework suitable for AI services.

---

## Current Limitations

This repository is a portfolio/reference implementation rather than a complete production platform.

Current limitations include:

- API-key-based authorization rather than enterprise identity federation.
- Local FAISS persistence.
- Text-based document ingestion only.
- Limited document metadata and source citation support.
- Limited automated test coverage.
- No production monitoring or observability stack.
- No automated production deployment pipeline.
- No multi-tenant authorization model.

FAISS indexes loaded by this application are expected to be trusted artifacts generated by this application. Untrusted serialized vector-store files should never be loaded.

---

## Future Improvements

Potential production enhancements include:

- PDF and DOCX document processing.
- Document-level metadata and source citations.
- IAM/Cognito/OIDC authentication.
- Fine-grained role and document authorization.
- Managed vector search.
- Retrieval evaluation metrics.
- Prompt-injection defenses.
- Rate limiting.
- Audit logging.
- Structured application logging.
- Cloud monitoring and alerting.
- End-to-end integration testing.
- Infrastructure as Code.
- Automated deployment pipeline.

---

## CI Status

The GitHub Actions Python CI workflow validates the application by installing dependencies, compiling the Python source, and running automated unit tests on repository changes.

---

## Disclaimer

This project is intended for educational and portfolio demonstration purposes.

The repository contains no proprietary enterprise data, customer documents, production secrets, or employer source code.
