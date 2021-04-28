import pandas as pd
import numpy as np
import warnings
import os
warnings.filterwarnings('ignore')
import seaborn as sns
import matplotlib.pyplot as plt

# Dataframe import
df_trainset = pd.read_csv('train.csv')


df_pivot = df_trainset.groupby('homeOwnership')['isDefault'].value_counts()
print(df_pivot)
