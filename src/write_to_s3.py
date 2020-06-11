import logging
import os
import boto3
import sys
import botocore

logger = logging.getLogger(__name__)

def write_to_s3(FILE_LOCATION=None, S3_BUCKET_NAME=None):
    """Function that takes the data - heart.csv from the ~/data location and uploads it into a given S3 bucket
    Inputs:
        S3_BUCKET: AWS credentials
        FILE_LOCATION: Location of the raw data file that needs to be uploaded to S3
    Returns:
        None
    """
    S3_PUBLIC_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    S3_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    try:
        s3 = boto3.client('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)
        s3.upload_file(FILE_LOCATION, S3_BUCKET_NAME, "heart.csv")
        logger.info("Raw data uploaded to S3 bucket")
    except botocore.exceptions.NoCredentialsError as e:
        logger.error("Invalid S3 credentials")
        sys.exit(1)
