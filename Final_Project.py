# Import necessary tool package.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Airline IATA code data
iatacode_data = pd.read_csv("airline_codes.csv")

print(iatacode_data.head())