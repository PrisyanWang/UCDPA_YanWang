# Import necessary tool package.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Airline IATA code data from csv
iatacode_data = pd.read_csv("airline_codes.csv")
print(iatacode_data.head())

# Import Stock Price data from csv and initiate the dataframe airlinestock_data
airlinestock_data = pd.read_csv("DAL.csv")
airlinestock_data["Stock_Code"] = "DAL"
# Using looping to append airlinestock_data to include stock price of other airlines
airlinecodelist=["AAL","LUV","SAVE","UAL"]
for airline in airlinecodelist:
    filename = airline + ".csv"
    airlinestock_con = pd.read_csv(filename)
    airlinestock_con["Stock_Code"] = airline
    airlinestock_data = airlinestock_data.append(airlinestock_con,ignore_index=True)
    print(airlinestock_data.head())
    print(airlinestock_data.shape)








