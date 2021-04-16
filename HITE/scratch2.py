import pandas as pd
import Exo.Duplicates as Dup

# index = rowid - 1
# rowid = row - 1
# row = index + 2

data = pd.read_csv('~/ASDRP/Data/Exoplanet_Data.csv', low_memory=False)

pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None


print('Total size: ', len(data))
data = data.dropna(
    subset=['pl_orbper', 'pl_trandep', 'pl_trandur', 'st_logg', 'st_teff', 'pl_imppar'])
data = data.loc[data['pl_rade'] <= 100]
data.reset_index(drop=True, inplace=True)

data['pl_trandep'] = data['pl_trandep'] * 10000
data['pl_trandur'] = data['pl_trandur'] * 24

for i, row in data.iterrows():
    try:
        pd.to_numeric(data['pl_imppar'][i])
        pd.to_numeric(data['pl_orbper'][i])
    except:
        data.drop([i], inplace=True)
data.reset_index(inplace = True)

data[['pl_ntranspec', 'pl_orbsmax', 'pl_trandur', 'st_rad', 'pl_rade', 'st_mass']] = \
    data[['pl_ntranspec', 'pl_orbsmax', 'pl_trandur', 'st_rad', 'pl_rade', 'st_mass']].apply(pd.to_numeric)

print('New size: ', len(data))

transpecs = data.loc[data['pl_ntranspec'] > 0]
print('How many of them have transmission spectroscopy measurements: ', len(transpecs))

dup_object = Dup.DeDupe(data)
dataframe = dup_object.remove_dupes()
print('After removing dupes: ', len(dataframe))

keprow1 = dataframe.loc[dataframe['pl_name'] == 'Kepler-138 b']
print(keprow1.index)
print('Length keprow1: ', len(keprow1))
keprow2 = dataframe.loc[dataframe['pl_name'] == 'Kepler-138 c']
print('Length keprow2: ', len(keprow2))
keprow3 = dataframe.loc[dataframe['pl_name'] == 'Kepler-138 d']
print('Length keprow3: ', len(keprow3))

# print(keprow1)

print('Planet name: ', keprow2['pl_name'][675])

print('Stellar logg: ', keprow2['st_logg'][675])
print('Stellar Radius: ', keprow2['st_rad'][675])
print('Stellar Temp: ', keprow2['st_teff'][675])

print('Interior planet: ')
print('Transit Depth 1: ', keprow1['pl_trandep'][674])
print('Orbital Period 1: ', keprow1['pl_orbper'][674])
print('Transit Duration 1: ', keprow1['pl_trandur'][674])
print('Impact Parameter 1: ', keprow1['pl_imppar'][674])

print('Planet being looked at:')
print('Transit Depth 2: ', keprow2['pl_trandep'][675])
print('Orbital Period 2: ', keprow2['pl_orbper'][675])
print('Transit Duration 2: ', keprow2['pl_trandur'][675])
print('Impact Parameter 2: ', keprow2['pl_imppar'][675])

print('Exterior planet: ')
print('Transit Depth 3: ', keprow3['pl_trandep'][676])
print('Orbital Period 3: ', keprow3['pl_orbper'][676])
print('Transit Duration 3: ', keprow3['pl_trandur'][676])
print('Impact Parameter 3: ', keprow3['pl_imppar'][676])

# 242
non_kepler_observations = dataframe.loc[data['disc_telescope'] != '0.95 m Kepler Telescope']
print(len(non_kepler_observations))

# THIS CAN BE FILTERED FOR OBSERVATIONS PAST 2015
kepler_observations = dataframe.loc[data['disc_telescope'] == '0.95 m Kepler Telescope']
print(len(kepler_observations))

print('Should be same as after removing dupes: ', len(non_kepler_observations) + len(kepler_observations))

no_major_axis = dataframe.dropna(subset=['pl_orbsmax'])
print(len(no_major_axis))

print(dataframe['pl_name'].head(30))
