import sys
import pandas as pd

def transformations(df,
                    fillna_cols=[],
                    fillna_value=0,
                    groupby_col='',
                    agg_dict={}
                    ): 
    """
        Function to perform specific transformations (this was mainly following the transform.ipynb notebook for SF salaries dataset)
        
        Parameters:
            df (pandas.DataFrame): input data.
            fillna_cols (list): list of columns in the dataset that need filling null values.
            fillna_value (any): the value to fill the null data with for each column in fillna_cols.
            groupby_col (str): the column to perform groupby on for data aggregation.
            agg_dict (dict): dict to map columns wanting to aggregate. e.g. {'BasePay': ['mean', 'median', 'range']}

        Returns:
            df_copy (pd.DataFrame): transformed dataframe which was a copy of original dataframe at the start before any transformations.
    """
    
    
    # check if df is df or series
    if not isinstance(df, (pd.DataFrame, pd.Series)):
        raise TypeError("The 'df' parameter must be a pandas.DataFrame or pandas.Series object.")

    df_copy = df.copy()

    # fills all nulls in the columns/dataframe with the fillna_value
    for col in fillna_cols:
        df_copy[col].fillna(fillna_value, inplace=True)
    
    # data aggregation step: groups the df by groupby_col and creates a new agg_df with dict values from agg_dict for the columns stated in the keys of agg_dict
    agg_df = df.groupby([groupby_col].agg(agg_dict)).reset_index()

    