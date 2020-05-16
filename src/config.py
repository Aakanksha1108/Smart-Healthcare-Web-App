from os import path

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))
FILE_LOCATION = path.join(PROJECT_HOME,'data/external/heart.csv')
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/local.conf')

# Enter the name of your S3 bucket here within double quotes
S3_BUCKET = "nw-aakanksha-sah-s3"

# Enter 'RDS' for creating a RDS Database and 'SQLITE' for creating a local sqlite database
DB_CHOICE = 'RDS'

# Do not change this. By default, the local sqlite database will be created in ~/data folder
SQLITE_DB_PATH = None
