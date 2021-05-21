import pandas as pd
import HITE as HT
import Exo.Duplicates as Dup

# index = rowid - 1
# rowid = row - 1

data = pd.read_csv('~/ASDRP/Data/Grouped/GroupedAllConfirmed.csv', low_memory=False)


# KOI Configuration:
# data.rename({'koi_prad': 'pl_rade', 'kepoi_name': 'pl_name', 'koi_period': 'pl_orbper', 'koi_depth': 'pl_trandep', 'koi_slogg': 'st_logg',
#              'koi_steff': 'st_teff', 'koi_srad': 'st_rad', 'koi_impact': 'pl_imppar', 'koi_duration': 'pl_trandur'}, axis=1, inplace=True)

# data.rename({'toi_created': 'pl_pubdate', 'toi': 'pl_name', 'toipfx': 'hostname', 'pl_trandurh': 'pl_trandur'}, axis=1, inplace=True)

pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None

# data = data.loc[data['pl_name']=='Kepler-1652 b']

print('Total size: ', len(data))

data = data.dropna(
    subset=['pl_orbper', 'pl_trandep', 'st_logg', 'st_teff', 'st_rad'])
data.reset_index(drop=True, inplace=True)

data['pl_trandep'] = data['pl_trandep'] * 10000

for i, row in data.iterrows():
    try:
        pd.to_numeric(data['st_rad'][i])
        pd.to_numeric(data['st_teff'][i])
        pd.to_numeric(data['pl_trandep'][i])
        pd.to_numeric(data['pl_orbper'][i])
        pd.to_numeric(data['st_logg'][i])
    except:
        data.drop([i], inplace=True)

data.reset_index(drop=True, inplace=True)

data[['st_rad', 'st_teff', 'pl_trandep', 'pl_orbper', 'st_logg']] = \
    data[['st_rad', 'st_teff', 'pl_trandep', 'pl_orbper', 'st_logg']].apply(pd.to_numeric)

print('Size after dropping non-numbers first section: ', len(data))


hite_object = HT.HITE(data)


dataframe1 = hite_object.apply_calc()
dataframe1.dropna(subset=['max_Flux'])
print(dataframe1.head(5))

hite_object.tryPlot(dataframe1)

dataframe2 = hite_object.apply_calc2()
dataframe2.dropna(subset=['max_Flux'])
print(dataframe2.head(5))

hite_object.tryPlot(dataframe2)

hite_object.compareRadii()

HpComp = hite_object.calc_Hp()
print('Size of HpComp: ', len(HpComp))

# HpComp.to_csv('~/ASDRP/Data/Hp Values/TOIsHp.csv', index=False)

data.dropna(subset=['pl_imppar', 'pl_trandur'], inplace=True)
data.reset_index(drop=True, inplace=True)

for i, row in data.iterrows():
    try:
        pd.to_numeric(data['pl_imppar'][i])
        pd.to_numeric(data['pl_trandur'][i])
    except:
        data.drop([i], inplace=True)
data.reset_index(drop=True, inplace=True)

data[['pl_imppar', 'pl_trandur']] = \
    data[['pl_imppar', 'pl_trandur']].apply(pd.to_numeric)


print('Size after dropping second null section: ', len(data))

min_eccens = hite_object.min_eccen()
print('First 10 minimum eccentricities:')
print(min_eccens['min_eccen'].head(10))

max_eccens = hite_object.GetEmax()
print('First 20 maximum eccentricities:')
print(max_eccens['max_eccen'].head(20))

temp1 = max_eccens.loc[max_eccens['max_eccen'] == -1]
temp2 = max_eccens.loc[max_eccens['max_eccen'] == 0.8]
print('How many actually have interesting max eccen: ', len(max_eccens) - len(temp1)- len(temp2))

HComp = hite_object.calc_H()

# HComp = hite_object.make_leg()

# better, clearly
posHp = HpComp.loc[HpComp['Hp'] > 0]
print(len(posHp))
# print(posHp[['pl_name', 'Hp', 'pl_pubdate', 'pl_ntranspec']])

posH = HComp.loc[HComp['H'] > 0]
print(len(posH))
# print(posH[['pl_name', 'H']])


posHp.sort_values(by=['Hp'], ascending=False, inplace=True, na_position='last')
# posHp.reset_index(inplace = True)

posH.sort_values(by=['H'], ascending=False, inplace=True, na_position='last')
# posH.reset_index(inplace = True)

# print('Highest Hp planet: ', posHp[['pl_name', 'Hp', 'pl_ntranspec','disc_facility']])
#
# print('Highest H planet: ', posH[['pl_name', 'H', 'pl_ntranspec','disc_facility']])

# HComp.to_csv('~/ASDRP/Data/H Values/KOIsH.csv', index=False)

# hite_object.plot_HZ(compilation)
#
# hite_object.plot_S_Hp(posHp)
#
# hite_object.plot_J_Hp(final)

# hite_object.plot_albflux()