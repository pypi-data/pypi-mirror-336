# import os
# import sys
# import shutil
# from datetime import datetime
# import cx_Oracle
# import psycopg2
# from psycopg2.extras import execute_values
# import csv

# # Oracle connection
# oracle_conn = cx_Oracle.connect(
#     'MIGCONV', 'MIGCONV', 'incemob002:1521/ATLGM3DV')
# oracle_cursor = oracle_conn.cursor()

# # PostgreSQL connection
# postgres_conn = psycopg2.connect(
#     dbname='paaspg', user='env17o', password='env17o', host='incetru119.corp.amdocs.com', port='5432')
# postgres_cursor = postgres_conn.cursor()

# def clean_data(data):
#     """Remove NUL characters from data."""
#     return [(str(item).replace('\x00', '') if isinstance(item, str) else item) for item in data]

# def export_to_csv(table_name, csv_file_path):
#     """Export data from Oracle table to CSV file."""
#     oracle_cursor.execute(f'SELECT * FROM {table_name}')
#     data = [tuple(row) for row in oracle_cursor.fetchall()]
#     columns = [desc[0] for desc in oracle_cursor.description]

#     with open(csv_file_path, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(columns)
#         for row in data:
#             writer.writerow(clean_data(row))

# # Function to copy table data
# def copy_table(table_name, pg_table_name):
#     # Fetch data from Oracle
#     oracle_cursor.execute(f'SELECT * FROM {table_name}')
#     data = [tuple(row) for row in oracle_cursor.fetchall()]
#     columns = [desc[0] for desc in oracle_cursor.description]

#     # Print the first 10 rows of data
#     for row in data[:1]:
#         print(row)

#     # Clean data to remove NUL characters
#     cleaned_data = [clean_data(row) for row in data]
        
#     # Insert data into PostgreSQL
#     insert_query = f'INSERT INTO {pg_table_name} ({", ".join(columns)}) VALUES %s'
#     execute_values(postgres_cursor, insert_query, cleaned_data)
#     postgres_conn.commit()

# # List of tables to copy
# tables_to_copy = ['br_charge', 'br_bill', 'br_payment', 'br_adjustment']
# pg_table_names = ['br_charge_leg', 'br_bill_leg', 'br_payment_leg' ,'br_adjustment_leg']

# for oracle_table, pg_table in zip(tables_to_copy, pg_table_names):
#     csv_file = f'{pg_table}.csv'
#     export_to_csv(oracle_table, csv_file)
#     # copy_table(oracle_table, pg_table)

# # Close connections
# oracle_cursor.close()
# oracle_conn.close()
# postgres_cursor.close()
# postgres_conn.close()

import os
import cx_Oracle
import psycopg2
import csv

def clean_data(data):
    """Remove NUL characters from data."""
    return [(str(item).replace('\x00', '') if isinstance(item, str) else item) for item in data]

def export_to_csv(cursor, table_name, csv_file_path):
    """Export data from a table to CSV file."""
    cursor.execute(f'SELECT * FROM {table_name}')
    data = [tuple(row) for row in cursor.fetchall()]
    columns = [desc[0] for desc in cursor.description]

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for row in data:
            writer.writerow(clean_data(row))

def get_db_connection(db_type):
    """Get database connection based on user input."""
    if db_type == 'oracle':
        user = input("Enter Oracle username: ")
        password = input("Enter Oracle password: ")
        dsn = input("Enter Oracle DSN (host:port/service_name): ")
        return cx_Oracle.connect(user, password, dsn)
    elif db_type == 'postgres':
        dbname = input("Enter PostgreSQL database name: ")
        user = input("Enter PostgreSQL username: ")
        password = input("Enter PostgreSQL password: ")
        host = input("Enter PostgreSQL host: ")
        port = input("Enter PostgreSQL port: ")
        return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    else:
        raise ValueError("Unsupported database type")

def db_to_csv(db_type):
    """Export tables from specified database to CSV files."""
    conn = get_db_connection(db_type)
    cursor = conn.cursor()

    while True:
        table_name = input("Enter table name to export (or 'done' to finish): ")
        if table_name.lower() == 'done':
            break

        csv_file_path = f"{table_name}.csv"
        try:
            export_to_csv(cursor, table_name, csv_file_path)
            print(f"Exported {table_name} to {csv_file_path}")
        except Exception as e:
            print(f"Error exporting {table_name}: {str(e)}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Select database type:")
    print("1. Oracle")
    print("2. PostgreSQL")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        db_to_csv('oracle')
    elif choice == '2':
        db_to_csv('postgres')
    else:
        print("Invalid choice. Exiting.")