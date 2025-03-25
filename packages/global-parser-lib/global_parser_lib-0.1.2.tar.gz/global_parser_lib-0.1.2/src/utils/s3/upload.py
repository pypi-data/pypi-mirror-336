import boto3
import os
from dotenv import load_dotenv
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('VAIA_AWS_ACCESS_KEY_ID',"")
AWS_SECRET_ACCESS_KEY = os.getenv('VAIA_AWS_SECRET_ACCESS_KEY',"")
AWS_REGION = os.getenv('VAIA_AWS_REGION',"")
def upload_bytes_to_s3(file_bytes: bytes, bucket: str, object_name: str) -> str:
    """
    Upload bytes to S3 and return the URL.
    
    Args:
        file_bytes: Bytes to upload
        bucket: S3 bucket name
        object_name: Object name in S3
        
    Returns:
        str: URL of the uploaded file
    """
   
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        s3_client.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=file_bytes
        )
        
        url = f"https://{bucket}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
        return url
        
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None