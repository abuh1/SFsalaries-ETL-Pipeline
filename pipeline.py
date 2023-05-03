from utils.extract_utils import load_data
from utils.transform_utils import clean_data
from src.SFsalaries_transform import transform
from src.SFsalaries_load import load

# extract input file
df = load_data('data/input/Salaries.csv')

# map columns to convert to the types to convert to
convert_dict = {
    'Id' : 'int',
    'Year' : 'int', 
    'BasePay' : 'float',
    'OvertimePay' : 'float',
    'OtherPay' : 'float',
    'Benefits' : 'float',
    'TotalPay' : 'float',
    'TotalPayBenefits' : 'float'
}

# clean data
df = clean_data(df, cols_to_drop=['Agency', 'Notes', 'Status'], dropna_subset=['BasePay'], remove_duplicates=True, convert_cols=convert_dict)

# transform data
df, agg_df = transform(df)

# load data
load(df, agg_df, 'data/output/salaries.sqlite')
