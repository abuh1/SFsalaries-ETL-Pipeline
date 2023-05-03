import pandas as pd
import re

def transform(salaries_df):
    # type check df
    if not isinstance(salaries_df, (pd.DataFrame, pd.Series)):
        raise TypeError("Passed parameter is not a pandas dataframe or series.")
    
    # make copy of df
    df = salaries_df.copy() 
    
    # fill benefits column nulls with 0
    df['Benefits'] = df['Benefits'].astype(float)
    df['Benefits'].fillna(0, inplace=True)
    
    # data aggregation step. (stats for basepay and totalpay grouped by job title)
    agg_df = df.groupby(['JobTitle']).agg({'BasePay': ['mean', 'median', 'min', 'max', 'std', 'count'], 'TotalPay': ['mean', 'median', 'min', 'max', 'std', 'count']}).reset_index()
    
    # data engineering step
    # define regex patterns for each category
    job_categories = {
    'Law Enforcement' : ['police', 'sheriff', 'crime', 'forensic(s)?', 'patrol', 'detective', 'mayor', 'sergeant', 'captain', 'officer', 'lieutenant'],
    'Safety & Security' : ['fire', 'safety', 'public', 'security', 'guard', 'protect(ive)?'],
    'Medical' : ['doctor', 'nurse', 'paramedic', 'medic(al)?', 'health(care)?', 'medicine', 'anesthetist'],
    'Education' : ['teacher', 'prof(essor)?', 'teacher(s)? assistant', 'education', 'eng(r)?'],
    'Administrative' : ['clerk', 'admin', 'secretary', 'assistant', 'library', 'librarian'],
    'Engineering' : ['engineer', 'architect', 'technician', 'physician', r'\belectr\w+'],
    'Construction' : ['construction', 'mechanic', 'laborer'], 
    'Information Technology' : ['programmer', 'developer', 'software', 'IT', 'computer', 'analyst'],
    'Management' : ['manager', 'director', 'CEO', 'owner', 'supervisor', 'head', 'leader'],
    'Finance' : ['accountant', 'economist', 'tax', 'finance', 'money'],
    'Legal' : ['law(yer)?', 'legal', 'attorney', 'judge'],
    'Maintenance' : ['custodian', 'porter', 'gardener'], 
    'Other' : []   
    }
    
    # function to assign job categories based on regex patterns
    def categorise_job_title(job_title):
        for category, patterns in job_categories.items():
            for pattern in patterns:
                if re.search(pattern, job_title, re.IGNORECASE):
                    return category
        return 'Other'

    # apply the categorise_job_title function to the JobTitle column and create new column
    df['JobCategory'] = df['JobTitle'].apply(categorise_job_title)
    
    # the second feature will compare TotalPay to the std for that job title and categorise it (low, medium, high)
    # create empty column
    df['SalaryRangeCategory'] = ''

    # merge the aggregated df and original df to compare salaries for job titles
    agg_df.columns = ['JobTitle', 'BasePay_mean', 'BasePay_median', 'BasePay_min', 'BasePay_max', 'BasePay_std', 'BasePay_count', 'TotalPay_mean', 'TotalPay_median', 'TotalPay_min', 'TotalPay_max', 'TotalPay_std', 'TotalPay_count']
    merged_df = df.merge(agg_df, on='JobTitle')
    
    # calculate the TotalPay salary range for each row, if pay is less than 1 std below mean, salary range will be low. Above will be high and within will be medium.
    for i, row in merged_df.iterrows():
        mean = row['TotalPay_mean']
        std = row['TotalPay_std']
        salary = row['TotalPay']
        if salary < mean - std:
            df.at[i, 'SalaryRangeCategory'] = 'low'
        elif salary > mean + std:
            df.at[i, 'SalaryRangeCategory'] = 'high'
        else:
            df.at[i, 'SalaryRangeCategory'] = 'medium'
            
    # fill in missing values (caused by std = NaN) with 'unknown'
    df['SalaryRangeCategory'] = df['SalaryRangeCategory'].fillna('unknown')
    
    # returns both df and agg_df ready to be loaded as seperate tables in sqlite db
    return df, agg_df