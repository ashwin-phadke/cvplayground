# BASED ON https://www.sqlitetutorial.net/sqlite-python/create-tables/

import sqlite3
from sqlite3 import Error
from os import chdir
from pathlib import Path
import os
import logging

logger = logging.getLogger('db_logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    logger.info("Creating the database for you..")
    database_name = 'cvplayground.sqlite'
    path = Path('..')
    chdir(path)
    database = os.path.join(os.getcwd(), 'db/', database_name)
    logger.info("Database created, creating required tables..")

    sqlite_create_cvp_table = """  CREATE TABLE IF NOT EXISTS uploads (
                                        id	TEXT UNIQUE,
                                        status	NUMERIC,
                                        isUploaded	INTEGER,
                                        isProcessed	INTEGER,
                                        location	TEXT,
                                        datetime	TEXT,
                                        model_name	TEXT
                                        );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sqlite_create_cvp_table)
    else:
        logger.info("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
    logger.info("Task successful")
