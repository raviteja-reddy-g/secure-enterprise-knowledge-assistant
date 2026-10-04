import boto3
from botocore.exceptions import ClientError

from app.config import AWS_REGION, S3_BUCKET_NAME


def get_s3_client():
    """Create and return an Amazon S3 client."""
    return boto3.client(
        "s3",
        region_name=AWS_REGION
    )


def list_documents():
    """Return document keys available in the configured S3 bucket."""

    if not S3_BUCKET_NAME:
        raise ValueError(
            "S3_BUCKET_NAME is not configured."
        )

    s3 = get_s3_client()

    try:
        response = s3.list_objects_v2(
            Bucket=S3_BUCKET_NAME
        )
    except ClientError as error:
        raise RuntimeError(
            f"Unable to list documents from S3: {error}"
        ) from error

    documents = []

    for item in response.get("Contents", []):
        key = item["Key"]

        if key.lower().endswith(
            (".txt", ".md", ".json")
        ):
            documents.append(key)

    return documents


def load_document(key: str) -> str:
    """Load a text-based document from Amazon S3."""

    if not S3_BUCKET_NAME:
        raise ValueError(
            "S3_BUCKET_NAME is not configured."
        )

    s3 = get_s3_client()

    try:
        response = s3.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=key
        )

        content = response["Body"].read()

        return content.decode(
            "utf-8",
            errors="ignore"
        )

    except ClientError as error:
        raise RuntimeError(
            f"Unable to load document '{key}': {error}"
        ) from error
