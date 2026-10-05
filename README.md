# Secure Enterprise Knowledge Assistant

![Python CI](https://github.com/raviteja-reddy-g/secure-enterprise-knowledge-assistant/actions/workflows/ci.yml/badge.svg)

A secure Retrieval-Augmented Generation (RAG) application for querying enterprise knowledge using natural language.

This project demonstrates an end-to-end AI knowledge retrieval architecture using *Python, FastAPI, AWS S3, Amazon Bedrock, LangChain, Hugging Face embeddings, FAISS, Docker, automated testing, and GitHub Actions CI*.

> This repository is a sanitized portfolio implementation designed to demonstrate enterprise AI architecture patterns. It does not contain proprietary employer code, customer data, production credentials, or confidential documents.

---

## Overview

Enterprise organizations often store large amounts of operational knowledge across policies, procedures, technical documentation, support information, and internal knowledge repositories.

Finding accurate information manually can be slow and inconsistent.

This project demonstrates a RAG-based enterprise knowledge assistant that:

1. Loads enterprise documents from Amazon S3.
2. Cleans and splits document content into smaller chunks.
3. Converts document chunks into semantic embeddings.
4. Stores the embeddings in a FAISS vector index.
5. Retrieves relevant document chunks for a user's question.
6. Sends the retrieved context to an Amazon Bedrock language model.
7. Generates a grounded answer through a FastAPI service.
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

An administrator can trigger knowledge-base ingestion through:

http
POST /admin/ingest


The ingestion workflow performs the following steps:

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


The current implementation supports text-based files including:

text
.txt
.md
.json


The ingestion process returns the number of documents processed and the number of chunks created.

---

## Document Processing

Documents are cleaned before indexing.

Extra whitespace and line breaks are normalized, after which the content is divided into smaller overlapping chunks using RecursiveCharacterTextSplitter.

Default chunk configuration:

text
Chunk Size:     1000
Chunk Overlap:  150


Chunk overlap helps preserve contextual continuity between adjacent sections of a document.

---

## Embeddings and Vector Search

The project uses the following sentence-transformer embedding model:

text
sentence-transformers/all-MiniLM-L6-v2


Document chunks are converted into vector embeddings and stored using FAISS.

When a question is submitted, semantic similarity search retrieves the most relevant chunks from the vector index.

The default retrieval configuration is:

text
TOP_K_RESULTS=5


This value can be changed using environment configuration.

---

## Retrieval-Augmented Generation Flow

When an authorized user asks a question:

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


The model is instructed to answer using only the retrieved enterprise context.

If the retrieved information does not support an answer, the prompt instructs the model not to invent information.

The Bedrock model is configurable through:

text
BEDROCK_MODEL_ID


This allows the application to use an appropriate supported Amazon Bedrock model without hard-coding one specific model into the application.

---

## API Endpoints

### Root Endpoint

http
GET /


Example response:

json
{
  "message": "Secure Enterprise Knowledge Assistant API is running"
}


---

### Health Check

http
GET /health


Example response:

json
{
  "status": "healthy"
}


---

### Ask a Question

http
POST /ask


Requires:

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


---

### Rebuild the Knowledge Index

http
POST /admin/ingest


Requires:

text
X-API-Key: <admin-key>


This endpoint:

1. Lists supported documents in Amazon S3.
2. Loads document content.
3. Cleans the text.
4. Splits documents into chunks.
5. Generates embeddings.
6. Creates the FAISS vector index.
7. Saves the vector store.

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


Authentication is supplied through the HTTP header:

text
X-API-Key


API-key comparisons use:

python
hmac.compare_digest()


rather than a normal string comparison.

Configuration values and API keys are loaded through environment variables instead of being hard-coded in application source code.

### Production Considerations

The current security model is intentionally lightweight for a portfolio/reference implementation.

A production enterprise deployment would normally use technologies such as:

- AWS IAM
- Amazon Cognito
- OAuth 2.0
- OpenID Connect
- JWT authentication
- Enterprise identity providers
- Secret rotation
- Fine-grained authorization policies
- Audit logging

The current reader/admin implementation demonstrates role-separated authorization but is not intended to represent a complete enterprise identity-management platform.

---

## Environment Configuration

Create a local environment file from the example:

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


Never commit real API keys, AWS credentials, tokens, or production secrets to the repository.

AWS authentication should use the standard AWS credential chain, such as:

- AWS CLI credentials
- IAM roles
- Workload identity
- Other approved AWS authentication mechanisms

---

## Running Locally

### 1. Clone the Repository

bash
git clone https://github.com/raviteja-reddy-g/secure-enterprise-knowledge-assistant.git


Move into the project directory:

bash
cd secure-enterprise-knowledge-assistant


### 2. Create a Virtual Environment

bash
python -m venv .venv


Activate it.

macOS/Linux:

bash
source .venv/bin/activate


Windows:

bash
.venv\Scripts\activate


### 3. Install Dependencies

bash
pip install -r requirements.txt


### 4. Configure Environment Variables

bash
cp .env.example .env


Update .env with your local configuration.

### 5. Start the API

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

Build the Docker image:

bash
docker build -t secure-enterprise-knowledge-assistant .


Run the container:

bash
docker run --env-file .env -p 8000:8000 secure-enterprise-knowledge-assistant


The application will be exposed on:

text
http://localhost:8000


The .dockerignore file prevents unnecessary local development files, caches, environment files, tests, and repository metadata from being copied into the Docker build context.

---

## Automated Testing

The project uses Python's built-in unittest framework.

Run all tests with:

bash
python -m unittest discover -s tests -p "test_*.py" -v


### Security Tests

tests/test_security.py validates:

- Matching API keys
- Non-matching API keys
- Missing expected credentials
- Reader authorization
- Administrator authorization
- Administrator access to reader operations
- Unauthorized reader requests
- Unauthorized administrator requests

### Document Processing Tests

tests/test_document_processor.py validates:

- Removal of extra whitespace
- Removal of leading and trailing spaces
- Document splitting into multiple chunks
- Preservation of important content during chunking

---

## Continuous Integration

The project uses GitHub Actions for automated continuous integration.

The workflow runs for:

text
Pushes to main
Pull requests targeting main


The CI pipeline performs:

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


This helps detect syntax errors, dependency problems, and test failures before changes are integrated.

---

## Docker Architecture

The application uses:

dockerfile
FROM python:3.11-slim


The Docker image:

1. Uses Python 3.11.
2. Creates /app as the working directory.
3. Installs dependencies from requirements.txt.
4. Copies the application into the image.
5. Exposes port 8000.
6. Starts FastAPI using Uvicorn.

Application startup command:

bash
uvicorn app.main:app --host 0.0.0.0 --port 8000


---

## Design Decisions

### Why RAG Instead of Fine-Tuning?

RAG allows enterprise knowledge to remain outside the language model while still providing relevant information at query time.

This makes it easier to update enterprise knowledge without retraining the underlying model.

---

### Why FAISS?

FAISS provides efficient vector similarity search and works well for demonstrating semantic retrieval in a local portfolio environment.

For larger production deployments, the vector layer could be replaced with a scalable managed or distributed vector-search system.

---

### Why Amazon Bedrock?

Amazon Bedrock provides managed access to foundation models and integrates naturally with AWS-based enterprise architectures.

The application keeps the model configurable through an environment variable rather than permanently tying the implementation to one specific model.

---

### Why Amazon S3?

Amazon S3 provides durable object storage and is commonly used for enterprise documents, data pipelines, and application assets.

It also integrates directly with the AWS SDK for Python through boto3.

---

### Why FastAPI?

FastAPI provides:

- Request validation
- Response models
- Dependency injection
- Automatic OpenAPI documentation
- Interactive API documentation
- A lightweight Python API framework suitable for AI services

---

### Why Docker?

Docker creates a consistent runtime environment that can be reproduced across development, testing, and deployment environments.

---

### Why GitHub Actions?

GitHub Actions automatically validates repository changes by installing dependencies, compiling the Python source, and running automated unit tests.

---

## Error Handling

The API returns controlled error responses rather than exposing internal exception details.

For example, failures in question processing return a generic server response:

text
Unable to process the question.


Similarly, ingestion failures return:

text
Unable to ingest documents.


This avoids directly exposing internal application errors to API consumers.

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
- No full prompt-injection defense layer

FAISS indexes loaded by this application are expected to be trusted artifacts generated by the application itself.

The current implementation uses:

python
allow_dangerous_deserialization=True


when loading the local FAISS index. Untrusted serialized vector-store files should never be loaded. A production implementation should enforce a stronger trusted-artifact and storage strategy.

---

## Future Improvements

Potential enhancements include:

- PDF document ingestion
- DOCX document ingestion
- S3 pagination for large document collections
- Source metadata preservation
- Document citations in generated answers
- Fine-grained document authorization
- IAM/Cognito/OIDC authentication
- Managed vector search
- Retrieval-quality evaluation
- Prompt-injection defenses
- Rate limiting
- Audit logging
- Structured application logging
- Cloud monitoring and alerting
- API endpoint integration tests
- Bedrock mock testing
- S3 integration testing
- Infrastructure as Code
- Automated deployment pipeline
- Production secrets management
- Horizontal scaling
- Multi-tenant access control

---

## Portfolio Scope

This repository demonstrates the architecture and engineering concepts behind a secure enterprise RAG application.

It is designed to showcase experience with:

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
CI


It should not be interpreted as production employer source code or as containing any confidential enterprise implementation.

---

## Disclaimer

This project is intended for educational, engineering demonstration, and portfolio purposes.

The repository contains no proprietary employer code, customer documents, production credentials, private datasets, or confidential enterprise information.
