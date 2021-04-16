import pandas as pd

map = {}

list1 = [1,2,3,4,5]
list2 = [6,7,8,9,10]
list3 = [11,12,13,14,15]


set = [list1,list2,list3]

map.update({'set1':set})

list4 = ['word1', 'word2', 'word3']
list5 = ['word4', 'word5', 'word6']
list6 = ['word7', 'word8', 'word9']

set2 = [list4, list5, list6]

map.update({'set2':set2})

print(map['set2'][1][1])

print(map.keys())

data = pd.read_csv('~/ASDRP/Data/Exoplanet_Data.csv', low_memory=False)
new_row = pd.DataFrame(index=range(0, 1), columns=list(data.columns))
print('Length: ', len(new_row))

print(data.iloc[1])

#
# for i, row in data.iterrows():
#     new_row.iloc[0] = row
#     print(new_row.type)
#     if i == 10:
#         break