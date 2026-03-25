import boto3
import os

def get_spaces_client():
    return boto3.client(
        "s3",
        region_name="sgp1",
        endpoint_url=os.getenv("SPACES_ENDPOINT"),
        aws_access_key_id=os.getenv("SPACES_KEY"),
        aws_secret_access_key=os.getenv("SPACES_SECRET"),
    )


def upload_text_file(filename: str, content: str):
    client = get_spaces_client()

    client.put_object(
        Bucket=os.getenv("SPACES_BUCKET"),
        Key=filename,
        Body=content,
        ACL="private"
    )

    return f"{os.getenv('SPACES_ENDPOINT')}/{os.getenv('SPACES_BUCKET')}/{filename}"