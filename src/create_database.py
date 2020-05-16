import os
import logging.config
import config
import sqlalchemy as sql
import sys
from helpers import create_engine_string, get_session
from sqlalchemy.orm import sessionmaker
import argparse
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('create_database')

user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = 'msia423_db'
conn_type = "mysql+pymysql"

Base = declarative_base()

class pd_predictions(Base):
    """Creates a table with scema for holding predictions that will be used later in the process"""
    __tablename__ = 'pd_predictions'
    age = Column(Integer, primary_key=True)
    sex = Column(String(100), unique=False, nullable=False)
    cp = Column(Integer, primary_key=True)
    chol = Column(Integer, primary_key=True)
    target = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        pred_repr = "<pd_predictions(age='%d', sex='%s', cp='%d', chol='%d',target='%s',)>"
        return pred_repr % (self.age, self.sex. self.cp, self.chol, self.target)

def _truncate_pd_predictions(session):
    """Deletes pd_predictions if rerunning and run into unique key error."""

    session.execute('''DELETE FROM pd_predictions''')

def create_db(engine_string):
    """Creates a database with the data models inherited from `Base` (pd_predictions).

    Args:
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`.
    Returns:
        None
    """
    try:
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database: msia423_db.db created successfully")
        logger.info("Table: pd_predictions created in database successfully")
    except Exception as e:
        logger.error(e)
        sys.exit(1)

if __name__ == "__main__":
    engine_string = create_engine_string(config.DB_CHOICE, host, user, password, port, database, conn_type,
                                         config.SQLITE_DB_PATH)
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from pd_predictions table before create_all "
                             "so that table can be recreated without unique id issues ")
    args = parser.parse_args()

    # If "truncate" is given as an argument (i.e. python create_database.py --truncate), then empty the pd_predictions table)
    if args.truncate:
        session = get_session(engine_string=engine_string)
        try:
            logger.info("Attempting to truncate pd_predictions table.")
            _truncate_pd_predictions(session)
            session.commit()
            logger.info("pd_predictions truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate pd_predictions table.")
            logger.error(e)
        finally:
            session.close()

    # Call the functions to create the database and table
    create_db(engine_string)


