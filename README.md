# Secure Enterprise Knowledge Assistant

![Python CI](https://github.com/raviteja-reddy-g/secure-enterprise-knowledge-assistant/actions/workflows/ci.yml/badge.svg)

A secure Retrieval-Augmented Generation (RAG) application for querying enterprise knowledge using natural language.

This project demonstrates an end-to-end AI knowledge retrieval architecture using *Python, FastAPI, AWS S3, Amazon Bedrock, LangChain, Hugging Face embeddings, FAISS, Docker, automated testing, and GitHub Actions CI*.

> This repository is a sanitized portfolio implementation designed to demonstrate enterprise AI architecture patterns. It does not contain proprietary employer code, customer data, production credentials, or confidential documents.

---

## Overview

Enterprise organizations often store operational knowledge across policies, procedures, technical documentation, support information, and internal knowledge repositories.

This project demonstrates a RAG-based knowledge assistant that:

1. Loads enterprise documents from Amazon S3.
2. Cleans and splits document content into smaller chunks.
3. Converts document chunks into semantic embeddings.
4. Stores embeddings in a FAISS vector index.
5. Retrieves relevant chunks for a user's question.
6. Sends the retrieved context to an Amazon Bedrock language model.
7. Returns a grounded answer through a FastAPI service.
8. Protects query and administrative operations using role-separated API-key authorization.
9. Uses Docker for containerization.
10. Uses GitHub Actions for automated syntax checks and unit testing.

---

## Architecture

text
                 ┌──────────────────────┐
                 │      Amazon S3       │
                 │ Enterprise Documents │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      S3 Loader       │
                 │    boto3 / Python    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Document Processor   │
                 │ Clean + Chunk Text   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Embedding Model    │
                 │ all-MiniLM-L6-v2     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     FAISS Index      │
                 │  Semantic Retrieval  │
                 └──────────┬───────────┘
                            │
                      User Question
                            │
                            ▼
                 ┌──────────────────────┐
                 │       FastAPI        │
                 │    /ask endpoint     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Similarity Search    │
                 │   Top-K Retrieval    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Amazon Bedrock     │
                 │ Configurable LLM     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Grounded Response   │
                 └──────────────────────┘


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
│   ├── test_document_processor.py
│   └── test_security.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt


---

## Document Ingestion Pipeline

An administrator can trigger ingestion through:

http
POST /admin/ingest


The ingestion workflow is:

text
Amazon S3 Documents
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
Local Vector Store


The current implementation supports:

text
.txt
.md
.json


Default document-processing configuration:

text
Chunk Size:     1000
Chunk Overlap:  150


Chunk overlap helps preserve context across neighboring chunks.

---

## Embeddings and Vector Search

The project uses:

text
sentence-transformers/all-MiniLM-L6-v2


Document chunks are converted into embeddings and stored in FAISS. At query time, semantic similarity search retrieves the most relevant chunks.

The default retrieval setting is:

text
TOP_K_RESULTS=5


---

## Retrieval-Augmented Generation Flow

text
User Question
      ↓
Semantic Similarity Search
      ↓
Top-K Relevant Chunks
      ↓
Enterprise Context
      ↓
Prompt Construction
      ↓
Amazon Bedrock LLM
      ↓
Grounded Answer


The model is instructed to answer using the retrieved enterprise context and to avoid inventing unsupported information.

The Bedrock model is configurable through:

text
BEDROCK_MODEL_ID


---

## API Endpoints

### Root

http
GET /


Example response:

json
{
  "message": "Secure Enterprise Knowledge Assistant API is running"
}


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


Required header:

text
X-API-Key: <reader-or-admin-key>


Example request:

json
{
  "question": "What is the enterprise incident escalation process?"
}


Example response structure:

json
{
  "question": "What is the enterprise incident escalation process?",
  "answer": "The answer generated from retrieved enterprise context."
}


### Rebuild the Knowledge Index

http
POST /admin/ingest


Required header:

text
X-API-Key: <admin-key>


The endpoint loads supported documents from S3, cleans and chunks the content, generates embeddings, creates the FAISS index, and saves the vector store.

Example response structure:

json
{
  "documents_processed": 5,
  "chunks_created": 42
}


---

## Security Model

The application demonstrates two logical access levels.

### Reader

Reader credentials can access:

http
POST /ask


### Administrator

Administrator credentials can access:

http
POST /ask
POST /admin/ingest


Authentication is supplied through:

text
X-API-Key


API-key comparisons use:

python
hmac.compare_digest()


Configuration values and API keys are loaded from environment variables rather than hard-coded in source code.

This is a lightweight portfolio security model, not a complete enterprise identity platform. A production deployment would typically use IAM, Cognito, OAuth 2.0, OpenID Connect, JWT-based authentication, secret rotation, audit logging, and fine-grained authorization.

---

## Environment Configuration

Create a local environment file:

bash
cp .env.example .env


Example configuration:

text
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-enterprise-documents-bucket
BEDROCK_MODEL_ID=your-bedrock-model-id

VECTOR_STORE_PATH=data/vector_store
TOP_K_RESULTS=5

READER_API_KEY=replace-with-reader-api-key
ADMIN_API_KEY=replace-with-admin-api-key


Never commit real API keys, AWS credentials, tokens, or production secrets.

AWS authentication should use the standard AWS credential chain, such as an authenticated AWS CLI profile, IAM role, or workload identity.

---

## Running Locally

Clone the repository:

bash
git clone https://github.com/raviteja-reddy-g/secure-enterprise-knowledge-assistant.git
cd secure-enterprise-knowledge-assistant


Create and activate a virtual environment:

bash
python -m venv .venv


macOS/Linux:

bash
source .venv/bin/activate


Windows:

bash
.venv\Scripts\activate


Install dependencies:

bash
pip install -r requirements.txt


Create the local environment file:

bash
cp .env.example .env


Start the API:

bash
uvicorn app.main:app --reload


API URL:

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


The .dockerignore file keeps local environment files, caches, tests, repository metadata, and other unnecessary development files out of the Docker build context.

---

## Automated Testing

The project uses Python's built-in unittest framework.

Run all tests with:

bash
python -m unittest discover -s tests -p "test_*.py" -v


### Security Tests

tests/test_security.py validates:

- Matching and non-matching API keys
- Missing expected credentials
- Reader authorization
- Administrator authorization
- Administrator access to reader operations
- Rejection of unauthorized requests

### Document Processing Tests

tests/test_document_processor.py validates:

- Whitespace cleanup
- Leading and trailing whitespace removal
- Document splitting into multiple chunks
- Preservation of important content during chunking

---

## Continuous Integration

GitHub Actions runs on pushes to main and pull requests targeting main.

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


The CI workflow catches syntax errors, dependency-installation issues, and unit-test failures.

---

## Docker Runtime

The application uses:

dockerfile
FROM python:3.11-slim


Startup command:

bash
uvicorn app.main:app --host 0.0.0.0 --port 8000


---

## Key Design Decisions

### Why RAG Instead of Fine-Tuning?

RAG keeps enterprise knowledge outside the underlying model and injects relevant context at query time. This makes the knowledge base easier to update without retraining the model.

### Why FAISS?

FAISS provides efficient local vector similarity search and works well for a portfolio/reference implementation. A larger production deployment could replace it with a managed or distributed vector-search platform.

### Why Amazon Bedrock?

Amazon Bedrock provides managed access to foundation models and fits naturally into AWS-based enterprise architectures.

### Why Amazon S3?

Amazon S3 provides durable object storage and integrates directly with Python through boto3.

### Why FastAPI?

FastAPI provides request validation, response models, dependency injection, automatic OpenAPI documentation, and interactive API documentation.

### Why Docker?

Docker provides a consistent runtime environment across development and deployment environments.

---

## Current Limitations

This repository is a portfolio/reference implementation rather than a complete production platform.

Current limitations include:

- API-key-based authorization rather than enterprise identity federation
- Local FAISS persistence
- Text-based document ingestion only
- Limited document metadata
- No source citations in generated responses
- Limited integration and end-to-end test coverage
- No production observability stack
- No automated production deployment pipeline
- No multi-tenant authorization model
- No retrieval-quality evaluation framework
- No rate limiting
- No complete prompt-injection defense layer
- S3 listing does not yet paginate large object collections

The local FAISS index is expected to be a trusted artifact generated by this application. The current implementation uses:

python
allow_dangerous_deserialization=True


Untrusted serialized vector-store files must never be loaded.

---

## Future Improvements

Potential enhancements include:

- PDF and DOCX ingestion
- S3 pagination
- Source metadata and answer citations
- Fine-grained document authorization
- IAM/Cognito/OIDC authentication
- Managed vector search
- Retrieval-quality evaluation
- Prompt-injection defenses
- Rate limiting
- Audit logging
- Structured application logging
- Cloud monitoring and alerting
- API integration tests
- Bedrock mock testing
- S3 integration testing
- Infrastructure as Code
- Automated deployment
- Production secrets management
- Horizontal scaling
- Multi-tenant access control

---

## Portfolio Scope

This repository demonstrates engineering concepts across:

text
Generative AI
Retrieval-Augmented Generation
AWS
Amazon Bedrock
Amazon S3
Python
FastAPI
LangChain
Embeddings
Vector Search
FAISS
API Security
Docker
Automated Testing
GitHub Actions
Continuous Integration


It should not be interpreted as production employer source code or as containing confidential enterprise implementation details.

---

## Disclaimer

This project is intended for educational, engineering demonstration, and portfolio purposes.

The repository contains no proprietary employer code, customer documents, production credentials, private datasets, or confidential enterprise information.
