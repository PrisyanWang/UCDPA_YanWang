import pandas as pd
import numpy as np
import warnings
import os
warnings.filterwarnings('ignore')
import seaborn as sns
import matplotlib.pyplot as plt

# Dataframe import
df_trainset = pd.read_csv('train.csv')
print(df_trainset.columns)

# Check for distribution and missing values of the dependent variable, isDefault
print(df_trainset.head())
print(df_trainset['isDefault'].value_counts())

# Check the missing values of independent variables(eigenvalue)
# Form a dataframe to record the missing percentage of independent variables
missing_series = df_trainset.isnull().sum()/df_trainset.shape[0]
missing_df = pd.DataFrame(missing_series).reset_index()
missing_df = missing_df.rename(columns={'index': 'col', 0: 'missing_pct'})
print(missing_df)
threshold_feature = 0.8
missing_col_num = missing_df[missing_df.missing_pct >= threshold_feature].shape[0]
print('The number of eigenvalues of which missing value surpass {} is {}'.format(threshold_feature, missing_col_num))
# Plot the chart of the eigenvalue distribution
sns.set()
plt.figure(figsize=(25, 5))
sns.set_style('whitegrid')
sns.set_context('talk')
plt.rcParams['axes.unicode_minus'] = False
plt.title('Distribution of missing variables')
sns.barplot(data=missing_df[missing_df.missing_pct > 0], x='col', y='missing_pct')
plt.ylabel('Missing Percentage')
plt.show()

# Check the quality of samples
missing_series = df_trainset.isnull().sum(axis=1)
# .value is used to return only the value part of a dictionary
list_missing_num = sorted(list(missing_series.values))
plt.figure(figsize=(25, 5))
plt.title('Distribution of missing samples')
plt.plot(range(df_trainset.shape[0]), list_missing_num)
plt.xlabel('samples')
plt.ylabel('Number of missing variables')
plt.show()

# Identify the category of independent variables, continuous variables or categorical variables
numerical_fea = list(df_trainset.select_dtypes(exclude=['object']).columns)
# Define a function called get_serial_fea so to facilitate the judgement
def get_serial_fea(data, feas):
    numerical_serial_fea = []
    nonnumerical_serial_fea = []
    for fea in feas:
        # Distinguish continuous(numerical)variables or categorical variables by the number of unique values
        # If the number of unique value of a variable exceeds 10, it is considered as numerical variable
        temp = data[fea].nunique()
        if temp <= 10:
            nonnumerical_serial_fea.append(fea)
        else:
            numerical_serial_fea.append(fea)
    return numerical_serial_fea,nonnumerical_serial_fea

numerical_serial_fea, nonnumerical_serial_fea = get_serial_fea(df_trainset, numerical_fea)

print(numerical_serial_fea)
print(nonnumerical_serial_fea)

# Identify the constant independent variables, these are invalid variables
# list all the name of variables except the isDefault(dependent variable)
column_list = [x for x in df_trainset.columns if x != 'isDefault']
const_val = []
nonconst_col = []
# Loop: if the number of samples with the same value for a variable exceeds 95% of the total samples,
# then the variable is deeded to be invalid
threshold_const = 0.95
for col in column_list:
    # value_counts the value with the largest count
    max_samples_count = df_trainset[col].value_counts().iloc[0]
    # total non-null sample numbers
    sum_samples_count = df_trainset[df_trainset[col].notnull()].shape[0]
    const_val.append(max_samples_count / sum_samples_count)
    # Filter for the non-constant variables
    if max_samples_count / sum_samples_count < threshold_const:
        nonconst_col.append(col)

const_val = sorted(const_val)
print(const_val)
print(nonconst_col)
print('Number of valid variables is {}'.format(len(nonconst_col)))

# Further look into the distribution of the valid variables
fig,ax=plt.subplots()


for col in nonconst_col:
    if df_trainset[col].nunique() < 500:
        print(col, 'number of unique values：', df_trainset[col].nunique())
        df_pivot = df_trainset.groupby(col)['isDefault'].value_counts()
        print(df_pivot)






