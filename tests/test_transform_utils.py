import unittest
import pandas as pd
import sys
sys.path.insert(0, '../')
from src.utils.transform_utils import load_data, clean_data

class TestTransformUtils(unittest.TestCase):

    def setUp(self):
        # sample dataframe for testing
        data = {'Name': ['John', 'Jane', 'Jim', 'Jake', 'Jill', 'Jill'],
                'Age': [25, 30, 35, 40, None, None],
                'Gender': ['M', 'F', 'M', 'M', 'F', 'F'],
                'Salary': [50000.0, 60000.0, None, 70000.0, 80000.0, 80000.0]}
        self.df = pd.DataFrame(data)
    
    def test_csv_loading(self):
        # test loading csv file
        input_file = 'test_files/test_example.csv'
        df = load_data(input_file)
        self.assertIsInstance(df, pd.DataFrame)
        
    def test_json_loading(self):
        # test loading json file
        input_file = 'test_files/test_example.json'
        df = load_data(input_file)
        self.assertIsInstance(df, pd.DataFrame)
        
    def test_sqlite_loading(self):
        # test loading sqlite file
        input_file = 'test_files/test_example.db'
        df = load_data(input_file, table_name='person')
        self.assertIsInstance(df, pd.DataFrame)
    
    def test_clean_data(self):
        # test that the function removes null columns and rows
        cleaned_cols_df = clean_data(self.df, drop_null_columns=True)
        self.assertEqual(cleaned_cols_df.shape, (6, 2))
        cleaned_rows_df = clean_data(self.df, drop_null_rows=True)
        self.assertEqual(cleaned_rows_df.shape, (3,4))
        
        # test dropping specified columns and rows
        dropped_rows_cols_df = clean_data(self.df, cols_to_drop=['Salary'], rows_to_drop=[3])
        self.assertEqual(dropped_rows_cols_df.shape, (5, 3))
        
        # test remove duplicates
        remove_dupes_df = clean_data(self.df, remove_duplicates=True)
        self.assertEqual(remove_dupes_df.shape, (5, 4))
        
        # test converting columns
        converted_df = clean_data(self.df, convert_cols={'Age': 'float'})
        self.assertEqual(converted_df.dtypes['Age'], 'float64')
        
    def tearDown(self):
        pass
    
if __name__ == '__main__':
    unittest.main()