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
output_location = 'data/output/salaries.sqlite'
load(df, agg_df, output_location)
print(f"Load complete. Output file location: {output_location}")
print("Dataframe head:\n", df.head())
