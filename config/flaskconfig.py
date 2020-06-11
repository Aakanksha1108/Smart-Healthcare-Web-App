import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "pseudo-doctor"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 10

MYSQL_USER=os.environ.get("MYSQL_USER")
MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST=os.environ.get("MYSQL_HOST")
MYSQL_PORT=os.environ.get("MYSQL_PORT")
DATABASE_NAME=os.environ.get("DATABASE_NAME")
SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
conn_type = "mysql+pymysql"

if ((SQLALCHEMY_DATABASE_URI is None) or (SQLALCHEMY_DATABASE_URI is "")) and ((MYSQL_HOST is None) or (MYSQL_HOST is '')):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423_db.db'
elif (host is None) or (host is ""):
    pass
else:
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, DATABASE_NAME)