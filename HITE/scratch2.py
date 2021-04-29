import pandas as pd
import Exo.Duplicates as Dup

# index = rowid - 1
# rowid = row - 1
# row = index + 2

data = pd.read_csv('~/ASDRP/Data/DeDuped.csv', low_memory=False)

pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None

data['pl_trandep'] = data['pl_trandep'] * 10000

#
#
# print('Total size: ', len(data))
# data = data.dropna(
#     subset=['pl_orbper', 'pl_trandep', 'pl_trandur', 'st_logg', 'st_teff', 'pl_imppar'])
# data = data.loc[data['pl_rade'] <= 100]
# data.reset_index(drop=True, inplace=True)
#
# data['pl_trandep'] = data['pl_trandep'] * 10000
#
# for i, row in data.iterrows():
#     try:
#         pd.to_numeric(data['pl_imppar'][i])
#         pd.to_numeric(data['pl_orbper'][i])
#     except:
#         data.drop([i], inplace=True)
# data.reset_index(inplace = True)
#
# data[['pl_ntranspec', 'pl_orbsmax', 'pl_trandur', 'st_rad', 'pl_rade', 'st_mass']] = \
#     data[['pl_ntranspec', 'pl_orbsmax', 'pl_trandur', 'st_rad', 'pl_rade', 'st_mass']].apply(pd.to_numeric)
#
# print('New size: ', len(data))
#
# transpecs = data.loc[data['pl_ntranspec'] > 0]
# print('How many of them have transmission spectroscopy measurements: ', len(transpecs))
#
# dup_object = Dup.DeDupe(data)
# dataframe = dup_object.remove_dupes()
# print('After removing dupes: ', len(dataframe))

keprow1 = data.loc[data['pl_name'] == 'TOI-1266 b']
keprow2 = data.loc[data['pl_name'] == 'TOI-1266 c']
print(keprow1.index)

# print(dataframe.iloc[38])

# print('Length keprow1: ', len(keprow1))
# keprow2 = dataframe.loc[dataframe['pl_name'] == 'Kepler-138 c']
# print('Length keprow2: ', len(keprow2))
# keprow3 = dataframe.loc[dataframe['pl_name'] == 'Kepler-138 d']
# print('Length keprow3: ', len(keprow3))

# print(keprow1)

print('Planet name: ', keprow2['pl_name'][2559])

print('')

print('Stellar logg: ', keprow2['st_logg'][2559])
print('Stellar Radius: ', keprow2['st_rad'][2559])                              # make sure to change which keprow is being referenced
print('Stellar Temp: ', keprow2['st_teff'][2559])

print('')

print('Interior planet: ')
print('Transit Depth 1: ', keprow1['pl_trandep'][2558])
print('Orbital Period 1: ', keprow1['pl_orbper'][2558])
print('Transit Duration 1: ', keprow1['pl_trandur'][2558])
print('Impact Parameter 1: ', keprow1['pl_imppar'][2558])
# print('Postion: ', keprow1['position'][2558])

print('')

print('Planet being looked at:')
print('Transit Depth 2: ', keprow2['pl_trandep'][2559])
print('Orbital Period 2: ', keprow2['pl_orbper'][2559])
print('Transit Duration 2: ', keprow2['pl_trandur'][2559])
print('Impact Parameter 2: ', keprow2['pl_imppar'][2559])
# print('Postion: ', keprow2['position'][2559])

# print('Exterior planet: ')
# print('Transit Depth 3: ', keprow3['pl_trandep'][676])
# print('Orbital Period 3: ', keprow3['pl_orbper'][676])
# print('Transit Duration 3: ', keprow3['pl_trandur'][676])
# print('Impact Parameter 3: ', keprow3['pl_imppar'][676])

# 242
# non_kepler_observations = dataframe.loc[data['disc_telescope'] != '0.95 m Kepler Telescope']
# print(len(non_kepler_observations))
#
# # THIS CAN BE FILTERED FOR OBSERVATIONS PAST 2015
# kepler_observations = dataframe.loc[data['disc_telescope'] == '0.95 m Kepler Telescope']
# print(len(kepler_observations))
#
# print('Should be same as after removing dupes: ', len(non_kepler_observations) + len(kepler_observations))
#
# no_major_axis = dataframe.dropna(subset=['pl_orbsmax'])
# print(len(no_major_axis))
#
# print(dataframe['pl_name'].head(30))
