import unittest
import csv
import sys
sys.path.insert(0, '../src')
from utils.extract_utils import extract_csv

class TestExtract(unittest.TestCase):
    
    def setUp(self):
        self.input_file = '../data/input/Salaries.csv'
        
    def test_extract_data(self):
        # execute the extract_data function
        data = extract_csv(self.input_file)
        # check that the data is a list
        self.assertIsInstance(data, list)
        # check that the first element of the data in the list is a dict
        self.assertIsInstance(data[0], dict)
        # check that the length of the data is greater than zero
        self.assertGreater(len(data), 0)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()