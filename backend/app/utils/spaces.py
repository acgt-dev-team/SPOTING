import boto3
import os
from dotenv import load_dotenv

load_dotenv()


def get_spaces_client():
    return boto3.client(
        "s3",
        region_name="sgp1",
        endpoint_url="https://sgp1.digitaloceanspaces.com",
        aws_access_key_id=os.getenv("DO_SPACES_KEY"),
        aws_secret_access_key=os.getenv("DO_SPACES_SECRET"),
    )


def upload_text_file(filename: str, content: str):
    client = get_spaces_client()

    bucket = os.getenv("DO_SPACES_BUCKET")

    if not bucket:
        raise ValueError("DO_SPACES_BUCKET is not set")

    client.put_object(
        Bucket=bucket,
        Key=filename,
        Body=content.encode("utf-8"),
        ACL="public-read"
    )

    return f"https://{bucket}.sgp1.digitaloceanspaces.com/{filename}"