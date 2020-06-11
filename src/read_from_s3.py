import os
import boto3
import sys
import logging
import botocore

logger = logging.getLogger(__name__)

def read_from_s3(S3_BUCKET_NAME=None, RAW_CSV_PATH=None):
    """Function that pulls the raw data from S3 and places it in the specified location
        Inputs:
            S3_BUCKET: Name of S3 bucket
            RAW_CSV_PATH: Location of the raw data file where the data needs to be placed
    """

    S3_PUBLIC_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    S3_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    RAW_CSV_PATH = RAW_CSV_PATH + '/heart.csv'

    try:
        s3 = boto3.client('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)
        s3.download_file(S3_BUCKET_NAME, 'heart.csv', RAW_CSV_PATH)
        logger.info("Raw data downloaded from S3 bucket successfully")
    except Exception as e:
        logger.error(e)
        sys.exit(1)