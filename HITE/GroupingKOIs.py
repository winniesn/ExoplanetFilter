import pandas as pd
import Exo.Duplicates as Dup
import matplotlib.pyplot as plt


ogdata = pd.read_csv('~/ASDRP/Data/KOIs_(9564).csv', low_memory=False)
ogdata.rename({'koi_vet_date': 'pl_pubdate', 'koi_prad': 'pl_rade', 'kepoi_name': 'pl_name', 'koi_period': 'pl_orbper', 'koi_depth': 'pl_trandep', 'koi_slogg': 'st_logg',
             'koi_steff': 'st_teff', 'koi_srad': 'st_rad', 'koi_impact': 'pl_imppar', 'koi_duration': 'pl_trandur'}, axis=1, inplace=True)

print('Length of ogdata: ', len(ogdata))
pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None


ogdata['hostname'] = ''
for i in range(len(ogdata)):
    ogdata['hostname'][i] = ogdata['pl_name'][i][0:6]
print(ogdata['hostname'].head(10))
ogdata['sy_numPlanets'] = 1
ogdata['position'] = 1

# data = ogdata.dropna(
#     subset=['pl_orbper', 'pl_trandep', 'pl_trandur', 'st_logg', 'st_teff', 'pl_imppar', 'st_rad'])
# data.reset_index(drop=True, inplace=True)

data = ogdata.dropna(
    subset=['pl_orbper', 'pl_trandep', 'st_logg', 'st_teff', 'st_rad'])
data.reset_index(drop=True, inplace=True)

print('Size after dropping first set: ',  len(data))



dup_object = Dup.DeDupe(data)
data = dup_object.remove_dupes()
print('After removing dupes: ', len(data))




# graph ogdata and data here
# datanames = ['Original Dataset', 'Non-Duplicates']
# sizes = [len(ogdata), len(data)]
# plt.bar(datanames, sizes, width=[0.6, 0.6])
# plt.title('Dataset Size Comparison')
# plt.xlabel('Dataset')
# plt.ylabel('Number of planets')
# plt.show()
#
map = {}
for i, row in data.iterrows():
    new_row = pd.DataFrame(index=range(0, 1), columns=list(data.columns))
    new_row.iloc[0] = row
    star = row['hostname']
    name = row['pl_name']
    if star in map.keys():
        map[star] = pd.concat([map[star], new_row])
    else:
        map.update({star:new_row})

finaldf = pd.DataFrame(columns = list(data.columns))

for system in map:
    leng = len(map[system])
    map[system] = map[system].sort_values(by=['pl_orbper'], ascending=True, inplace=False, na_position='last')
    map[system].reset_index(inplace = True)
    map[system]['sy_numPlanets'][:] = leng
    if leng > 1:
        for i in range(leng):
            map[system]['position'][i] = i + 1
        # print(map[system][['pl_name', 'hostname', 'sy_numPlanets', 'position']])
    finaldf = pd.concat([finaldf, map[system]], ignore_index = True)


# finaldf.reset_index(inplace = True)

print(len(finaldf))

finaldf.to_csv('~/ASDRP/Data/Grouped/GroupedKOIs.csv', index=False)