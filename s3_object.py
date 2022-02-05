"""Module object

   Contains routines for managing remote (cloud) object

"""
#import os
from lib2to3.pgen2.token import NUMBER
from pathlib import Path
from enum import Enum, Flag
from tkinter.messagebox import NO
from dotenv import dotenv_values
import boto3
from botocore.exceptions import NoCredentialsError

class outcome(Enum):
    NOEXIST = 1
    NOTARGET = 2
    SINGLETARGET = 3
    MULTITARGET = 4
    UNKNOWN = 9
    FILEUPLOADED = 100

class S3_object():
    """This cleass provides action methods on the S3 objects

    """
    _number_bytes_written = 0

    def __init__(self, test=False) -> None:
        self.test = test
        self.config = dotenv_values(".env")

    def _update_number_bytes_written(self, num : float):
        self._number_bytes_written += num

    def _upload_to_aws(self, local_file, bucket, s3_file):
        """private function to access S3

        :param local_file: a local asset to upload
        :type local_file: pathlib.PosixPath
        :param bucket: the S3 bucket
        :type bucket: str
        :param s3_file:  the remote key (fileame) including and pathing
        :type s3_file: str
        :return: number of bytes written
        :rtype: int

        """
        s3 = boto3.client('s3', aws_access_key_id=self.config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=self.config['AWS_SECRET_ACCESS_KEY'])
        try:
            self._number_bytes_written = 0
            s3.upload_file(local_file, bucket, s3_file, Callback=self._update_number_bytes_written )
            return self._number_bytes_written
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

    def _archive_s3_object(self, bucket, source_file, target_key):
        """private function to archive a file (copy)
        
        :param source_file: the source file to archive, including any pathing
        :type source_file: pathlib.PosixPath
        :param bucket: the S3 bucket
        :type bucket: str
        :param target_file: the target (inlcuding any pathing) in the bucket to copy the archive
        :type target_file: str
        :return: number of bytes written
        :rtype: int

        """        
        s3 = boto3.client('s3', aws_access_key_id=self.config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=self.config['AWS_SECRET_ACCESS_KEY'])
        try:
            self._number_bytes_written = 0
            copy_source = {
                'Bucket' : bucket,
                'Key' : source_file
            }
            s3.copy(copy_source, bucket, target_key, Callback=self._update_number_bytes_written )
            return self._number_bytes_written
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
    
    ## Public Functions

    def upload_s3(self, local_path, bucket, key_prefix=None, key=None, archive=False, mark_delete=False):
        """Public callable for object upload 
        
        :param local_asset: The specifier for the local asset; can be a singe file or a file spece (i.e. '*.csv')
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
        local_asset = Path(local_path).expanduser()
        target = Path(key_prefix).joinpath(local_asset.name)
        if local_asset.name.count('*') > 0 and local_asset.parent.exists():
            status = outcome.MULTITARGET
        elif not local_asset.exists(): 
            status = outcome.NOEXIST
        elif local_asset.is_dir():
            status = outcome.NOTARGET
        else:
            status = outcome.SINGLETARGET

        match status:
            case outcome.NOEXIST:
                raise FileNotFoundError(f"file {local_asset} note found")
            case outcome.NOTARGET:
                raise KeyError(f"no local asset specified")
            case outcome.SINGLETARGET:
                if self.test: return outcome.SINGLETARGET
                    return self._upload_to_aws(str(local_asset), bucket, str(target))
            case outcome.MULTITARGET:
                if self.test: return outcome.MULTITARGET
        
        
        #p = Path(os.path.expanduser('~/iCloud/Downloads/Weight History'))
        #for file in p.glob('*.csv'):
        #    print(f"Uploading {os.path.basename(file)}", end=' ... ')
        #   _upload_to_aws(str(file), os.environ['WEIGHT_HISTORY_BUCKET'], f"Data Sets/Weight History/{os.path.basename(file)}")