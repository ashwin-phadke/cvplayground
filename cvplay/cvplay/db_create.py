import logging
import sqlite3
from sqlite3 import Error
import os


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
        logging.error(e)

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
        logging.error(e)


def main():
    """
    Execute the database creation flow
    """
    if not os.path.exists('db'):
        os.mkdir('db')
    database = 'db/cvplayground.db'

    sqlite_create_cvp_table = """  CREATE TABLE IF NOT EXISTS uploads (
                                        id	TEXT UNIQUE,
                                        status	NUMERIC,
                                        isUploaded	INTEGER,
                                        isProcessed	INTEGER,
                                        location	TEXT,
                                        datetime	TEXT,
                                        model_name	TEXT,
                                        pbtxt_name TEXT
                                        );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sqlite_create_cvp_table)

    else:
        logging.error("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()