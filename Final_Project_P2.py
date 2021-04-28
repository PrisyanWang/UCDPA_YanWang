# Import necessary tool package.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

airline_list = ['UAL','AAL','DAL','SAVE']
For airline in airline_list:

# Import stock price from csv and set date as index
airlinestock_df = pd.read_csv("UAL.csv",parse_dates=['Date'],index_col='Date')
print(airlinestock_df.info())
# Subset only the Close Price column
airlineclose_df = airlinestock_df[['Close']]
print(airlineclose_df.head())
# Regroup on time-series data, downsampling the price to monthly basis
airlineclosemon_df = airlineclose_df.resample('M').mean()
# Calculate the monthly price percent change
airlineclosemon_df['Diff'] = airlineclosemon_df.Close.pct_change().mul(100)
airlineclosemon_df['year'] = pd.DatetimeIndex(airlineclosemon_df.index).year
airlineclosemon_df['month'] = pd.DatetimeIndex(airlineclosemon_df.index).month
print(airlineclosemon_df.head())

# Import operation data from csv and set date as index
airlineops_df = pd.read_csv("UA-all_airports.csv",parse_dates=['Date'],index_col='Date')
airlineops_df['year'] = pd.DatetimeIndex(airlineops_df.index).year
airlineops_df['month'] = pd.DatetimeIndex(airlineops_df.index).month
print(airlineops_df.head())

# Merge the price with the operation data on the year and month
price_ops_df = airlineclosemon_df.merge(airlineops_df, on=['year','month'])
print(price_ops_df.columns)
# Calculate PLF
price_ops_df['RPM'] = price_ops_df['RPM_Domestic']+price_ops_df['RPM_International']
price_ops_df['ASM'] = price_ops_df['ASM_Domestic']+price_ops_df['ASM_International']
price_ops_df['PLF'] = price_ops_df['RPM']/price_ops_df['ASM']
# Re-calculate date
price_ops_df['day'] = 1
price_ops_df['Date'] = pd.to_datetime(price_ops_df[['year','month','day']])
price_ops_df=price_ops_df.set_index(price_ops_df['Date'])
price_ops_df['Diff_PLF'] = price_ops_df.PLF.pct_change().mul(100)
price_ops_df=price_ops_df.dropna()
print(price_ops_df.head())

fig,ax = plt.subplots()
ax.scatter(price_ops_df['Diff'],price_ops_df['Diff_PLF'])
ax.set_xlabel("Stock Price Changes")
ax.set_ylabel("PLF Changes")
plt.show()

r,p = stats.pearsonr(price_ops_df['Diff'],price_ops_df['Diff_PLF'])
print('Correlation r = %6.3f, p = %6.3f'%(r,p))













