import pandas as pd
from extract_utils import extract_csv

# load data into pandas dataframe
data = extract_csv('data/input/Salaries.csv')
df = pd.DataFrame(data)

print(df.head())