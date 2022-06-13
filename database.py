import csv
from psycopg2.extras import RealDictCursor, DictCursor, DictRow
from typing import Tuple
from contextlib import contextmanager

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS {} (id SERIAL PRIMARY KEY, {});" #variety TEXT, sepal length NUMERIC(2, 1), sepal width, petal length, petal width

SELECT_ALL = "SELECT * FROM {};"

VIEW_AVERAGE = ""

INSERT_POSITION = "INSERT INTO {} ({}) VALUES ({});"  #we can choose the column to be returned to create a feedback like "{name} has been successfully inserted into database with id of {number}"

SELECT_COLUMNS_NAMES = """SELECT 
                        column_name
                        FROM 
                        information_schema.columns
                        WHERE 
                        table_name = %s;"""

SELECT_TABLES_NAMES = """SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema='public'
                        AND table_type='BASE TABLE';"""

SELECT_ALL_TABLES = """SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema='public';"""



@contextmanager
def get_cursor(connection, todict: bool):
    with connection:
        if todict:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                yield cursor
        else:
            with connection.cursor() as cursor:
                yield cursor


#i could make every query being called directly by menu, but i will make separate function for every word just in case there would be more queries in the future


def select_tables_names(connection, x: bool) -> list[list]:
    with get_cursor(connection, x) as cursor:
        cursor.execute(SELECT_TABLES_NAMES)
        return cursor.fetchall()  #what if there will be thousands of tables? using list is bad for efficiency

def create_table(connection, table_name: str, columns: str):
    query = CREATE_TABLE.format(table_name, columns)  #we make it possible to create table with as many columns as needed
    with get_cursor(connection, False) as cursor:
        cursor.execute(query)

def add_data(connection, table_name: str, data: list[list]):
    with get_cursor(connection, True) as cursor:
        cursor.execute(SELECT_COLUMNS_NAMES, (table_name, ))
        columns = cursor.fetchall()
        query_columns = ', '.join(column[0] for column in columns if column[0] != 'id')
        if data[0][0] == columns[1][0]:     #we check if accidentally first row in data isn't meant to be column, it will always happen in case of creating new table
            data.pop(0)
        for row in data:
            s_percents = tuple(['%s' for column in row])   #we will add percents instead of values to avoid dropping tables with injection attack
            query = INSERT_POSITION.format(table_name, query_columns, ', '.join(s_percents))
            cursor.execute(query, tuple(row))
        print("All data has been inserted successfully")   #-----need to write some code to inform user in case some lines has been not inserted successfully

def all_tables(connection) -> list:
    with get_cursor(connection, True) as cursor:
        cursor.execute(SELECT_ALL_TABLES)
        return cursor.fetchall()

