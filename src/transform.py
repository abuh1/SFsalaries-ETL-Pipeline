import pandas as pd
from extract import extract_data

# load data into pandas dataframe
data = extract_data('data/input/Salaries.csv')
df = pd.DataFrame(data)

print(df.head())