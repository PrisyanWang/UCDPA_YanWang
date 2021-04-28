# Import necessary tool package.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

airlinecode_df = pd.read_csv('airline_codes.csv')
stockcode_list = ['UAL','DAL','SAVE']
fig, ax = plt.subplots(3, 1)
i=0
for stockcode in stockcode_list:
    stockfile = stockcode + '.csv'
    iatacode = airlinecode_df[airlinecode_df['Stock Code'] == stockcode]['Airline Code']
    opsfile = iatacode.iloc[0] + '_ops.csv'

    # Import stock price from csv and set date as index
    airlinestock_df = pd.read_csv(stockfile, parse_dates=['Date'], index_col='Date')
    # Subset only the Close Price column
    airlineclose_df = airlinestock_df[['Close']]
    # Regroup on time-series data, downsampling the price to monthly basis
    airlineclosemon_df = airlineclose_df.resample('M').mean()
    # Calculate the monthly price percent change
    airlineclosemon_df['Diff'] = airlineclosemon_df.Close.pct_change().mul(100)
    airlineclosemon_df['year'] = pd.DatetimeIndex(airlineclosemon_df.index).year
    airlineclosemon_df['month'] = pd.DatetimeIndex(airlineclosemon_df.index).month

    # Import operation data from csv and set date as index
    airlineops_df = pd.read_csv(opsfile, parse_dates=['Date'], index_col='Date')
    airlineops_df['year'] = pd.DatetimeIndex(airlineops_df.index).year
    airlineops_df['month'] = pd.DatetimeIndex(airlineops_df.index).month

    # Merge the price with the operation data on the year and month
    price_ops_df = airlineclosemon_df.merge(airlineops_df, on=['year', 'month'])

    # Calculate PLF
    price_ops_df['RPM'] = price_ops_df['RPM_Domestic'] + price_ops_df['RPM_International']
    price_ops_df['ASM'] = price_ops_df['ASM_Domestic'] + price_ops_df['ASM_International']
    price_ops_df['PLF'] = price_ops_df['RPM'] / price_ops_df['ASM']
    # Re-calculate date
    price_ops_df['day'] = 1
    price_ops_df['Date'] = pd.to_datetime(price_ops_df[['year', 'month', 'day']])
    price_ops_df = price_ops_df.set_index(price_ops_df['Date'])
    price_ops_df['Diff_PLF'] = price_ops_df.PLF.pct_change().mul(100)
    price_ops_df = price_ops_df.dropna()
    print(price_ops_df)

    r, p = stats.pearsonr(price_ops_df['Diff_PLF'], price_ops_df['Diff'])
    print('Correlation of %s' % stockcode + ' r = %6.3f, p = %6.3f' % (r, p))

    ax[i].scatter(price_ops_df['Diff'], price_ops_df['Diff_PLF'])
    ax[i].set_ylabel(stockcode + ' Price Changes')
    i=i+1

ax[2].set_xlabel("PLF Changes")
plt.show()

