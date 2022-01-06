import os
import boto3
from botocore.exceptions import NoCredentialsError

datafile = os.path.expanduser('~/iCloud/Downloads/Budget Input.csv')

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

if __name__ == '__main__':
    uploaded = upload_to_aws(datafile, os.environ['DATA_SET_BUCKET'],
	os.environ['BUDGET_INPUT_KEY'])



