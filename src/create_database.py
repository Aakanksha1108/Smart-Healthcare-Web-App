import os
import logging
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
Base = declarative_base()


class pd_predictions(Base):
    """Creates a table with schema that will be used later in the pipeline for storing predictions"""
    __tablename__ = 'pd_predictions'
    age = Column(Integer,unique=False,nullable=False, primary_key=True)
    sex = Column(Integer,unique=False,nullable=False, primary_key=True)
    chest_pain = Column(Integer,unique=False,nullable=False, primary_key=True)
    fasting_blood_sugar = Column(Integer,unique=False,nullable=False, primary_key=True)
    electrocardiographic = Column(Integer,unique=False,nullable=False, primary_key=True)
    induced_angina = Column(Integer,unique=False,nullable=False, primary_key=True)
    thal = Column(Integer,unique=False,nullable=False, primary_key=True)
    y_prob = Column(String(10), unique=False, nullable=False)
    y_bin = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        pred_repr = "<pd_predictions(age='%d', sex='%d', chest_pain='%d', fasting_blood_sugar='%d',\
        electrocardiographic = '%d',induced_angina='%d',thal='%d',y_prob='%s',y_bin='%d')>"
        return pred_repr % (self.age, self.sex, self.chest_pain, self.fasting_blood_sugar, \
                            self.electrocardiographic,self.induced_angina,self.thal, self.y_prob,self.y_bin)


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
        logger.info("Database created successfully")
        logger.info("Tables created in database successfully")
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def create_engine_string(host=None, user=None, password=None, port=None, database=None, conn_type=None, \
                         SQLALCHEMY_DATABASE_URI=None):
    """ Creates the path to the location where the RDS or SQLITE database will be created
        Inputs:
            host, use, password, port, conn_type: details corresponding to the RDS connection
            SQLALCHEMY_DATABASE_URI: location where the local sqlite database will be created
            database: Name of the database
        Returns:
            SQLALCHEMY_DATABASE_URI : engine string
    """

    if ((SQLALCHEMY_DATABASE_URI is None) or (SQLALCHEMY_DATABASE_URI is "")) and ((host is None) or (host is '')):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423_db.db'
    elif (host is None) or (host is ""):
        pass
    else:
        SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)
    return SQLALCHEMY_DATABASE_URI


def get_session(engine_string=None):
    """
    Args:
        engine_string: SQLAlchemy connection string in the form of:

            "{sqltype}://{username}:{password}@{host}:{port}/{database}"

    Returns:
        SQLAlchemy session
    """
    engine = sql.create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_database_main(df,truncate_flag):
    """
        Function that takes dataframe amd truncate_flag as input to create a database and add records to it
        Returns: None
    """
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    database = os.environ.get("DATABASE_NAME")
    conn_type = "mysql+pymysql"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    engine_string = create_engine_string(host, user, password, port, database, conn_type,SQLALCHEMY_DATABASE_URI)
    if truncate_flag==1:
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
    add_records(df,engine_string)


def add_records(df,engine_string):
    """Add records to database
    Args: dataframe and engine string
    Returns: None
    """
    engine = sql.create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.bulk_insert_mappings(pd_predictions, df.to_dict(orient="records"))
        session.commit()
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    finally:
        session.close()
        return


