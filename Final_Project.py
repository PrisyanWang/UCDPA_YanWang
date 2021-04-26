# Import necessary tool package.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Stock Price data from csv and initiate the dataframe airlinestock_data
airlinestock_data = pd.read_csv("DAL.csv")
airlineprice_data = airlinestock_data[["Date","Close"]]
airlineprice_data.Date = pd.to_datetime(airlineprice_data.Date)


airlinestock_data = pd.read_csv("SAVE.csv")
saveprice_data = airlinestock_data[["Date","Close"]]
saveprice_data.Date = pd.to_datetime(saveprice_data.Date)
airlineprice_data = airlineprice_data.merge(saveprice_data,on="Date",suffixes=["_DAL","_SAVE"])
print(airlineprice_data.head())

airlineprice_monthly = airlineprice_data.resample("1m", on='Date')['Close_SAVE','Close_DAL'].mean()
print(airlineprice_monthly.head())

fig,ax=plt.subplots(2,1)
ax[0].plot(airlineprice_data['Date'],airlineprice_data["Close_DAL"],label='DAL')
ax[0].plot(airlineprice_data['Date'],airlineprice_data["Close_SAVE"],label='SAVE')
ax[1].plot(airlineprice_monthly.index,airlineprice_monthly["Close_DAL"],label='DAL_monthly')
ax[1].plot(airlineprice_monthly.index,airlineprice_monthly["Close_SAVE"],label="SAVE_monthly")
plt.legend()
plt.show()







