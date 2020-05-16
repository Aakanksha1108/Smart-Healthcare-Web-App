import datetime
import yaml
import os

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker

def create_engine_string(db_choice, host, user, password, port, database, conn_type, sqlite_path):
    """ Creates the path to the location where the RDS or SQLITE database will be created
        Inputs:
            db_choice: can be RDS or SQLITE based on the preference of the user
            host, use, password, port, conn_type: details corresponding to the RDS connection
            sqlite_path: location where the local sqlite database will be created
            database: Name of the database
        Returns:
            conn: Connection to the engine
    """
    if db_choice == 'RDS':
        # This part runs if the user selects to create an RDS database
        if host is None:
            # If the user hasn't provided a host, then a local sqlite database will be created in the ~/data folder
            engine_string = 'sqlite:///data/msia423_db.db'
        else:
            # This section created the engine_string for RDS
            engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)
    else:
        # This part runs if the user selects to create a local sqlite database.
        if sqlite_path is None:
            engine_string = 'sqlite:///data/msia423_db.db'
        else:
            engine_string = sqlite_path

    return engine_string

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
