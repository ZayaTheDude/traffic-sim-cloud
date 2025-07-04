import boto3
import os

s3 = boto3.client('s3', region_name='us-east-2')

def upload_file(file_path, bucket_name="traffic-sim-logs-isaiah", object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"✅ Uploaded {file_path} to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
    