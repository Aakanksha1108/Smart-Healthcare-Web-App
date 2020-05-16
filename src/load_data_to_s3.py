import os
import config
import logging.config
import boto3
import sys
import botocore

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('create_database')

S3_PUBLIC_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
S3_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

def write_to_s3(S3_PUBLIC_KEY, S3_SECRET_KEY, FILE_LOCATION, S3_BUCKET):
    """Function that takes the data - heart.csv from the ~/data location and uploads it into a given S3 bucket
    Inputs:
        S3_PUBLIC_KEY, S3_SECRET_KEY, S3_BUCKET: AWS credentials
        FILE_LOCATION: Location of the raw data file that needs to be uploaded to S3
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)
        s3.upload_file(FILE_LOCATION, S3_BUCKET, "heart.csv")
        logger.info("Raw data uploaded to S3 bucket")
    except botocore.exceptions.NoCredentialsError as e:
        logger.error("Invalid S3 credentials")
        sys.exit(1)

# Call the function created above to write data into S3 bucket
write_to_s3(S3_PUBLIC_KEY, S3_SECRET_KEY, config.FILE_LOCATION, config.S3_BUCKET)