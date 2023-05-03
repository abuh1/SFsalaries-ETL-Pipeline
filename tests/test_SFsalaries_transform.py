import sys
import pandas as pd
import unittest
sys.path.insert(0, '../')
from utils.extract_utils import load_data
from src.SFsalaries_transform import transform

class TestTransform(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            'JobTitle': ['Doctor', 'Nurse', 'Police Officer', 'Teacher'],
            'BasePay': [100000.0, 75000.0, 80000.0, 50000.0],
            'TotalPay': [150000.0, 90000.0, 100000.0, 60000.0],
            'Benefits': [20000.0, 10000.0, None, 5000.0]
        })
        
    def test_transform_returns_tuple(self):
        result = transform(self.df)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        
    def test_transform_returns_dataframes(self):
        result = transform(self.df)
        self.assertIsInstance(result[0], pd.DataFrame)
        self.assertIsInstance(result[1], pd.DataFrame)
        
    def test_transform_raises_exception_for_non_dataframe_input(self):
        with self.assertRaises(TypeError):
            transform('invalid input')
    
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)