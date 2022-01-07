import os
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

if __name__ == '__main__':
    p = Path(os.path.expanduser('~/iCloud/Downloads/Weight History'))
    for file in p.glob('*.csv'):
        print(f"Uploading {os.path.basename(file)}", end=' ... ')
        upload_to_aws(str(file), os.environ['WEIGHT_HISTORY_BUCKET'], f"Data Sets/Weight History/{os.path.basename(file)}")




