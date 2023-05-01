import os
import pandas as pd
from src.utils.extract_utils import extract_csv, extract_json, extract_sqlite

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

def clean_data(df,
               drop_null_columns=False,
               drop_null_rows=False,
               cols_to_drop=[],
               rows_to_drop=[],
               remove_duplicates=False,
               convert_cols={}):
    """
    Performs cleaning operations on a pandas DataFrame.
    
    Args:
        df (pandas.DataFrame): The DataFrame to clean.
        drop_null_columns (bool): Whether to drop columns that contain null values or not.
        drop_null_rows (bool): Whether to drop rows that contain null values or not.
        cols_to_drop (list): Optional columns to drop.
        rows_to_drop (list): Optional rows to drop.
        remove_duplicates (bool): Removes any duplicate entries if set to True.
        convert_cols (dict): Column (key) and dtype to convert the column into (value) to convert columns' data types.
        
    Returns:
        df (pandas.DataFrame): Cleaned data.
    """
    # type check df
    if not isinstance(df, (pd.DataFrame, pd.Series)):
        raise TypeError("The 'df' parameter must be a pandas DataFrame or Series.")
    
    df_copy = df.copy()
    
    # drop null columns and rows
    if drop_null_columns:
        df_copy.dropna(axis=1, inplace=True)
    if drop_null_rows:
        df_copy.dropna(axis=0, inplace=True)
    
    # drops columns and rows specified
    df_copy.drop(cols_to_drop, axis=1, inplace=True)
    df_copy.drop(rows_to_drop, axis=0, inplace=True)
    
    # remove duplicates
    if remove_duplicates:
        df_copy.drop_duplicates(inplace=True)
    
    # convert specified columns to target dtype
    for col, dtype in convert_cols.items():
        if dtype == "int" or dtype == "float":
            df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
        df_copy[col] = df_copy[col].astype(dtype)
    
    return df_copy