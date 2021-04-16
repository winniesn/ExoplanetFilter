import pandas as pd
import Exo.Duplicates as Dup


ogdata = pd.read_csv('~/ASDRP/Data/Exoplanet_Data.csv', low_memory=False)

print('Length of ogdata: ', len(ogdata))
pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None

data = ogdata.dropna(
    subset=['pl_orbper', 'pl_trandep', 'pl_trandur', 'st_logg', 'st_teff', 'pl_imppar', 'pl_orbsmax'])
data.reset_index(drop=True, inplace=True)

print('Dropping null parameters: ', len(data))

data['sy_numPlanets'] = 1
data['position'] = 1

dup_object = Dup.DeDupe(data)
data = dup_object.remove_dupes()
print('After removing dupes: ', len(data))

map = {}

for i, row in data.iterrows():
    new_row = pd.DataFrame(index=range(0, 1), columns=list(data.columns))
    new_row.iloc[0] = row
    star = row['hostname']
    name = row['pl_name']
    if star in map.keys():
        pos = len(map[star])
        map[star] = pd.concat([map[star], new_row], ignore_index=True)
        map[star]['sy_numPlanets'][:] = map[star]['sy_numPlanets'][0] + 1
        map[star]['position'][pos] = map[star]['sy_numPlanets'][0]
    else:
        map.update({star:new_row})

print(len(map.keys()))

finaldf = pd.DataFrame(columns = list(data.columns))

for system in map:
    finaldf = pd.concat([finaldf, map[system]], ignore_index = True)


finaldf.reset_index(inplace = True)

print(len(finaldf))

finaldf.to_csv('~/ASDRP/Data/DeDuped.csv', index=False)