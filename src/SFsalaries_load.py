import sqlite3
import pandas as pd

def load(df, agg_df, db_file):
    # type check df and agg_df
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be pandas dataframe.")
    
    if not isinstance(agg_df, pd.DataFrame):
        raise TypeError("agg_df must be pandas dataframe.")
    
    # connect to SQLite db
    conn = sqlite3.connect(db_file)

    # write the df's to seperate tables in db file
    df.to_sql(name='salaries', con=conn, if_exists='replace', index=False)
    agg_df.to_sql(name='agg_salaries', con=conn, if_exists='replace', index=False)
    
    # close connection
    conn.close()