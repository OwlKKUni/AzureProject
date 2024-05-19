import os
import pyodbc
import random
import datetime


class DBConnString:
    def __init__(self, server, database, username, password, driver):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver


class SQLQuery:
    def __init__(self, table_name, **kwargs):
        self.table_name = table_name
        self.columns = kwargs

    def add_column(self, column_name, column_type):
        self.columns[column_name] = column_type

    def generate_query(self):
        query = f"CREATE TABLE {self.table_name} ("
        column_definitions = [f"id INT PRIMARY KEY"]  # first column
        for column_name, column_type in self.columns.items():
            column_definitions.append(f"{column_name} {column_type}")
        query += ", ".join(column_definitions)
        query += ");"
        return query


# CONN STRING FOR SERVERS
Server1 = DBConnString(os.environ['AZURE_SERVER'], os.environ['AZURE_DATABASE'], os.environ['AZURE_SERVER_USERNAME'],
                       os.environ['AZURE_DB_PASSWORD'], '{ODBC Driver 18 for SQL Server}')

# QUERIES FOR CREATING EMPTY TABLES
tquery_objectives = SQLQuery(table_name='objectives_completed',
                             main_objectives='INT',
                             optional_objectives='INT',
                             helldivers_extracted='INT',
                             outposts_destroyed_light='INT',
                             outposts_destroyed_medium='INT',
                             outposts_destoryed_heavy='INT',
                             mission_time_remaining='TIME'
                             ).generate_query()

tquery_samples = SQLQuery(table_name='samples_gained',
                          green_samples='INT',
                          orange_samples='INT',
                          violet_samples='INT'
                          ).generate_query()

tquery_currency = SQLQuery(table_name='currency_gained',
                           requisition='INT',
                           medals='INT',
                           xp='INT'
                           ).generate_query()

tquery_combat = SQLQuery(table_name='combat',
                         kills='INT',
                         accuracy="DECIMAL(5,2)",
                         shots_fired='INT',
                         deaths='INT',
                         stims_used='INT',
                         accidentals='INT',
                         samples_extracted='INT',
                         stratagems_used='INT',
                         melee_kills='INT',
                         times_reinforcing='INT',
                         friendly_fire_damage='INT',
                         distance_travelled='INT',
                         ).generate_query()


def connect(conn_string):
    try:
        conn = pyodbc.connect(f'DRIVER={conn_string.driver};SERVER={conn_string.server};'
                              f'DATABASE={conn_string.database};UID={conn_string.username};PWD={conn_string.password}')
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


# CREATE TABLES ----------------------------
# WORKS
def query_create_tables(server_name: DBConnString, table_queries: list) -> None:
    try:
        if connect(server_name) is None:
            print("Failed to connect to the database.")
            return

        with connect(server_name).cursor() as cursor:
            for table_query in table_queries:
                cursor.execute(table_query)
                print(f'Table "{table_query.split(" ")[2]}" created')
            connect(server_name).commit()

    except pyodbc.Error as e:
        print(f"Error creating data: {e}")

    finally:
        if connect(server_name):
            connect(server_name).close()


# READ TABLES ----------------------------
def query_read_row(server_name: DBConnString, table: str, row_number: int) -> None:
    with connect(server_name).cursor as cursor:
        row = cursor.execute(f'SELECT * FROM {table} WHERE rowid = ?', (row_number,))
        print(row)
        connect(server_name).close()


def query_read_table(server_name: DBConnString, table: str) -> None:
    with connect(server_name).cursor as cursor:
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        connect(server_name).close()


# GET ----------------------------


# Works
def query_get_table_names(server_name: DBConnString):
    sql_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"

    try:
        with connect(server_name).cursor() as cursor:
            cursor.execute(sql_query)
            table_names = [row.TABLE_NAME for row in cursor.fetchall()]

        if table_names:
            return table_names

        else:
            print("No data found.")
            return []

    except pyodbc.Error as e:
        print(f"Error executing SQL query: {e}")
        return []

    finally:
        connect(server_name).close()

    # returns: [['id', 'kills', 'accuracy', 'shots_fired', 'deaths', 'stims_used',
    # 'accidentals', 'samples_extracted', 'stratagems_used', 'melee_kills',
    # 'times_reinforcing_', 'friendly_fire_damage', 'distance_travelled']]


# WORKS
def query_get_table_column_names(server_name: DBConnString, table: str) -> list:
    data = []
    with connect(server_name).cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table}')
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data.append(columns)
        for row in rows:
            data.append(list(row))
        connect(server_name).close()
    return data


def query_get_data_from_table(server_name: DBConnString, table: str) -> list:
    columns = query_get_table_column_names(server_name, table)
    with connect(server_name).cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        data = [columns] + [list(row) for row in rows]
        connect(server_name).close()
        return data


# UPDATE TABLES ----------------------------
# test this if it works

# added () in q_update_cell after execute sql_query
def query_update_cell(server_name: DBConnString, table_name: str,
                      column_name: str, row_number: int, value: any) -> None:
    sql_query = f"UPDATE {table_name} SET {column_name} = {value} WHERE {row_number} = ?"

    try:
        with connect(server_name).cursor as cursor:
            cursor.execute(sql_query, (value, row_number))
            connect(server_name).commit()
            connect(server_name).close()
        print(f'Table "{table_name}" updated')
    except pyodbc.Error as e:
        print(f"Error updating table '{table_name}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# DELETE --------------------------------
# WORKS
def query_delete_all_tables(server_name: DBConnString):
    try:
        table_names = query_get_table_names(server_name)
        if table_names:
            for table_name in table_names:
                query_delete_table(server_name, table_name)
        else:
            print("No data found to delete.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        connect(server_name).close()


# WORKS
def query_delete_table(server_name: DBConnString, table_name: str) -> None:
    sql_query = f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}"

    try:
        with connect(server_name).cursor() as cursor:
            cursor.execute(sql_query)
            connect(server_name).commit()
            connect(server_name).close()
        print(f'Table "{table_name}" deleted')
    except pyodbc.Error as e:
        print(f"Error deleting table '{table_name}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        connect(server_name).close()


def query_delete_row(server_name: DBConnString, table_name: str, row_number: int) -> None:
    sql_query = f"DELETE FROM {table_name} WHERE rowid = {row_number}"

    with connect(server_name).cursor() as cursor:
        cursor.execute(sql_query)
        connect(server_name).commit()
        connect(server_name).close()


# PUT ----------------------------
#

# Aux functions ------------------------


if __name__ == "__main__":
    print(query_get_data_from_table(Server1, 'combat'))
