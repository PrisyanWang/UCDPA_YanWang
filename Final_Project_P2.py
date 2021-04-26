# Import necessary tool package.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

uaops_data = pd.read_csv("UA-all_airports.csv")
pd.to_datetime(uaops_data.Date)
uaops_data.set_index("Date",inplace=True)
print(uaops_data.head())
print(uaops_data.tail())

nkops_data = pd.read_csv("NK-all_airports.csv")
pd.to_datetime(nkops_data.Date)
nkops_data.set_index("Date",inplace=True)
print(nkops_data.tail())
