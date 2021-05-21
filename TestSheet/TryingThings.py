# Necessary Import Statements
import pandas as pd
import numpy as np

# Imports the datasets
data = pd.read_csv('~/ASDRP/Data/BetaData.csv', low_memory=False)
phl = pd.read_csv('~/ASDRP/Data/PHL_Dataset.csv', low_memory=False)

df1 = pd.DataFrame({'A': [1,1,1,1,1],
                    'B': [2,2,2,2,2],
                    'C': [3,3,3,3,3]})

df2 = pd.DataFrame(columns=list(df1.columns))
#
# # add rows to dataframe using append
# df_append = df1.append(df2, ignore_index=True)
# # print(dr_append)
#
# # add rows to dataframe using concat
# df_concat = pd.concat([df1,df2], ignore_index=True)
# # print(df_concat)
#
# # add row to dataframe using loc
# df3 = df1.copy()
# print(len(df3['A']))
#
# df3.loc[len(df3['A'])] = df2.iloc[1]
# print(df3)
# print(len(df3['A']))
#
# print(df1)

for index, row in df1.iterrows():
    df2.loc[len(df2['A'])] = df1.iloc[index]

# 10 20 30
# meh
# 1 2 3
# meh
print(df2)
