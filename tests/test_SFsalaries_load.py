import unittest
import pandas as pd
import sqlite3
import os
import sys
sys.path.insert(0, '../')
from src.SFsalaries_load import load

class TestLoadFunction(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            'Name': ['John', 'Jane', 'Adam', 'Eva'],
            'Salary': [50000, 60000, 55000, 70000],
            'Department': ['Marketing', 'Engineering', 'Marketing', 'Engineering']
        })
        
        self.agg_df = pd.DataFrame({
            'Department': ['Engineering', 'Marketing'],
            'Average Salary': [65000, 52500]
        })
        
        self.db_file = '../data/output/test_db.sqlite'
        
    def test_load_with_valid_args(self):
        load(self.df, self.agg_df, self.db_file)
        
        # check if tables exist
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        conn.close()
        
        expected_tables = [('salaries',), ('agg_salaries',)]
        
        self.assertEqual(len(tables), len(expected_tables))
        
        for expected_table in expected_tables:
            self.assertIn(expected_table, tables)
        
        # check if the data was loaded correctly
        conn = sqlite3.connect(self.db_file)
        df_from_db = pd.read_sql_query("SELECT * from salaries", conn)
        conn.close()
        
        self.assertTrue(df_from_db.equals(self.df))
    
    def test_load_with_invalid_args(self):
        with self.assertRaises(TypeError):
            load("not a df", self.agg_df, self.db_file)
        
        with self.assertRaises(TypeError):
            load(self.df, "not a df", self.db_file)
            
        with self.assertRaises(sqlite3.OperationalError):
            load(self.df, self.agg_df, "not_a_valid_path/test.sqlite")
            
    def tearDown(self):
        # check if file exists before deleting
        if os.path.isfile('../data/output/test_db.sqlite'):
            os.remove('../data/output/test_db.sqlite')
        
if __name__ == '__main__':
    unittest.main()