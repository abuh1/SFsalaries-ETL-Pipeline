import csv
import json
import sqlite3
import psycopg2
import mysql.connector

# extract the data from csv file
def extract_csv(input_file):
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# extract data from JSON file
def extract_json(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
    return data

# extract data from sqlite database
def extract_sqlite(db_file, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"SELCT * FROM {table_name}")
    data = [row for row in cursor]
    conn.close()
    return data

# extract data from mysql database
def extract_mysql(db_name, user, password, host, port, table_name):
    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=db_name
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = [row for row in cursor]
    conn.close()
    return data

# extract data from postgresql database
def extract_postgresql(db_name, user, password, host, port, table_name):
    conn = psycopg2.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=db_name
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = [row for row in cursor]
    conn.close()
    return data