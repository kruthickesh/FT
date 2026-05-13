from boto3 import client
from ..core.config import settings
import uuid
import os

def get_s3_client():
    if settings.AWS_ACCESS_KEY_ID:
        return client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name=settings.AWS_REGION)
    return None

def upload_file(file_data: bytes, filename: str, folder: str = "uploads") -> str:
    s3 = get_s3_client()
    if not s3:
        return None
    
    ext = os.path.splitext(filename)[1]
    key = f"{folder}/{uuid.uuid4()}{ext}"
    
    s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=file_data)
    return f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

def delete_file(key: str) -> bool:
    s3 = get_s3_client()
    if not s3:
        return False
    s3.delete_object(Bucket=settings.S3_BUCKET, Key=key)
    return True

def get_signed_url(key: str, expiration: int = 3600) -> str:
    s3 = get_s3_client()
    if not s3:
        return None
    return s3.generate_presigned_url('get_object', Params={'Bucket': settings.S3_BUCKET, 'Key': key}, ExpiresIn=expiration)