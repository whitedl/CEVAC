import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import seaborn as sns

# read in the data
df = pd.read_csv('WAP_WATT_HOURLY.csv')

# fix the date column so that we omit the year
def fix(date):
    fixedDate = date[0:5]

# apply the fix
df['time'].apply(fix)

# get the correlation between our columns
corr = df.corr()

# # make the heatmap
# sns.heatmap(corr,
#         xticklabels=corr.columns,
#         yticklabels=corr.columns)
#
# # display the heatmap
# plt.show()
