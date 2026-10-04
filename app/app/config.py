import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID")

VECTOR_STORE_PATH = os.getenv(
    "VECTOR_STORE_PATH",
    "data/vector_store"
)

TOP_K_RESULTS = int(
    os.getenv("TOP_K_RESULTS", "5")
)
