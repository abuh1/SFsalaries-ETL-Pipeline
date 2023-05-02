import os
import pandas as pd
import csv
import json
import sqlite3

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
    cursor.execute(f"SELECT * FROM {table_name}")
    data = [row for row in cursor]
    conn.close()
    return data

# dictionary to map file extensions to extract functions
extract_functions = {
    '.csv' : extract_csv,
    '.json' : extract_json,
    '.sqlite' : extract_sqlite,
    '.db' : extract_sqlite,
    '.db3' : extract_sqlite,
}

def load_data(input_file, table_name=''):
    """
    Load data from a file into a pandas dataframe.
    
    Args:
        input_file (str): Path to the input file.
        table_name (str): Used for sqlite db only. Specify the table name by including 'table_name={table_name}' when calling this function.
        
    Returns:
        pandas.DataFrame: Loaded data.
    """
    # get the file extension
    _, ext = os.path.splitext(input_file)
    
    # check if extension type is supported
    if ext not in extract_functions:
        raise ValueError(f"File type {ext} is not supported.")
    
    # extract the data
    extract_func = extract_functions[ext]
    # raises error if table_name is not specified for sqlite db
    if extract_func == extract_sqlite:
        if table_name == '':
            raise ValueError("Table name must be specified for SQLite database.")
        else:
            data = extract_func(input_file, table_name)
    else:
        data = extract_func(input_file)

    # load data into pandas dataframe
    df = pd.DataFrame(data)
    return df