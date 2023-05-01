import sys
import pandas as pd
sys.path.insert(0, '../')
from utils.extract_utils import extract_csv

def transformations(df):
    # check if df is df or series
    if not isinstance(df, (pd.DataFrame, pd.Series)):
        raise TypeError("The 'df' parameter must be a pandas.DataFrame or pandas.Series object.")

    