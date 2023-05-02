import unittest
import pandas as pd
import sys
sys.path.insert(0, '../src')
from utils.extract_utils import load_data

class TestExtract(unittest.TestCase):
    
    def setUp(self):
        pass
    
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
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()