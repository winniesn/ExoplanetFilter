import pandas as pd
import HITE as HT
import Exo.Duplicates as Dup

# index = rowid - 1
# rowid = row - 1

data = pd.read_csv('~/ASDRP/Data/DeDuped.csv', low_memory=False)

pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None


print('Total size: ', len(data))

data['pl_trandep'] = data['pl_trandep'] * 10000


for i, row in data.iterrows():
    try:
        pd.to_numeric(data['pl_imppar'][i])
        pd.to_numeric(data['pl_orbper'][i])
    except:
        data.drop([i], inplace=True)

data[['pl_imppar', 'pl_orbper', 'pl_ntranspec', 'pl_orbsmax', 'pl_trandur', 'st_rad', 'pl_rade', 'st_mass']] = \
    data[['pl_imppar', 'pl_orbper', 'pl_ntranspec', 'pl_orbsmax', 'pl_trandur', 'st_rad', 'pl_rade', 'st_mass']].apply(pd.to_numeric)

transpecs = data.loc[data['pl_ntranspec'] > 0]
print('How many of them have transmission spectroscopy measurements: ', len(transpecs))

# data = data.loc[data['hostname'] == 'Kepler-442']

data.reset_index(inplace = True, drop = True)

print(len(data))

hite_object = HT.HITE(data)

dataframe1 = hite_object.apply_calc()
dataframe1.dropna(subset=['max_Flux'])
# print(dataframe1.head(5))

# hite_object.tryPlot(dataframe1)
#
# dataframe2 = hite_object.apply_calc2()
# dataframe2.dropna(subset=['max_Flux'])
# print(dataframe2.head(5))

# hite_object.tryPlot(dataframe2)

# hite_object.compareRadii()

min_eccens = hite_object.min_eccen()
print('First 10 minimum eccentricities:')
# print(min_eccens['min_eccen'].head(10))

max_eccens = hite_object.GetEmax()
print('First 10 maximum eccentricities:')
# print(max_eccens['max_eccen'].head(10))

# temp1 = max_eccens.loc[max_eccens['max_eccen'] == -1]
# temp2 = max_eccens.loc[max_eccens['max_eccen'] == 0.8]
# print('How many actually have interesting max eccen: ', len(max_eccens) - len(temp1)- len(temp2))

compilation = hite_object.calc_HITE()
compilation = hite_object.make_leg()

kep442b = data.loc[data['pl_name'] == 'Kepler-442 b']
print('Kepler-442 b radius: ', kep442b['pl_rade'])
print('Kepler-442 b mass: ', kep442b['pl_mass'])
print('Kepler-442 b semia: ', kep442b['pl_semia'])
print('Kepler-442 b semia: ', kep442b['pl_semia'])
# Circular Duration [hour]: 6.179820
# Transit Duration Anomoly: 0.909573
# Minimum Eccentricity: 0.094497
# Planet's Gravity [m/s^2]: 21.752774
# Maximum Eccentricity: 0.800000
# Maximum Flux [W/m^2]: 322.641778
# Circular Instellation [Earth]: 0.811608
# Flux Constraint: Both
print('Kepler-442 b Scirc: ', kep442b['instellation'])

# compilation = compilation.dropna(subset=['sy_jmag'])
# # print('Theoretically the luminosity values')
# # print(compilation['calc_lum'].head(5))
#
# posHp = compilation.loc[compilation['Hp'] > 0]
# print(len(posHp))
# print(posHp[['pl_name', 'Hp']])