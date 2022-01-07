"""Module object

   Contains routines for managing remote (cloud) object

"""
import os
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError

def _upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def upload_s3(local_asset, bucket, key_prefix = None, key = None):
    """Uploads a local asset (file or files) to s3 
    
    :param local_asset: The specifier for the local asset
    :type local_asset: pathlib.PosixPath
    :param bucket: the AWS S3 bucket name
    :type bucket: str
    :param key_prefix: The prefix used for the key name in the bucket
    :type key_prefix: str
    :param key: the key name to use for the remote asset
    :type key: str

    The key_prefix and key are optional.  The key_prefix is used after the bucket name and before the key (as a folder structure).
    the key is used to have a different name of the assest. If the asset is to be named the same as the input, this can be excluded.

    Example:

    If the local file is "myfile.txt" and it is to go at the top level of the bucket, then the operation would be:


    """
    if not Path(local_asset).expanduser().exists():
        raise FileExistsError
    
    if (p := Path(local_asset).expanduser()).is_dir():
        return  p.glob('*.csv')

    elif Path(local_asset).expanduser().is_file():
        return 2
    return 3

    
    
    #p = Path(os.path.expanduser('~/iCloud/Downloads/Weight History'))
    #for file in p.glob('*.csv'):
    #    print(f"Uploading {os.path.basename(file)}", end=' ... ')
    #   _upload_to_aws(str(file), os.environ['WEIGHT_HISTORY_BUCKET'], f"Data Sets/Weight History/{os.path.basename(file)}")




