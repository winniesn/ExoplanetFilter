# The necessary import statements
import pandas as pd
import Exo.Duplicates as DU
import Exo.HZCalculation as HZ
import Exo.MTypeHabitable as MT

# Reading the data
data = pd.read_csv('~/ASDRP/Data/AllConfirmed_(29398).csv', low_memory=False)
print('Length of data: ', len(data))
# widerdata = pd.read_csv('~/ASDRP/Data/data.csv', low_memory=False)
# widerdata.rename(columns={'st_dist':'sy_dist', 'st_spstr':'st_spectype'}, inplace=True)
# data = pd.read_csv('~/ASDRP/Data/GammaData.csv', low_memory=False)
# weirddata = pd.read_csv('~/ASDRP/Data/Exoplanet_Data.csv', low_memory=False)
# beta_data = pd.read_csv('~/ASDRP/Data/BetaData.csv', low_memory=False)
# phl = pd.read_csv('~/ASDRP/Data/PHL_Dataset.csv', low_memory=False)
# print('The first five rows of the raw dataset: ')
# print(data[['pl_name', 'pl_pubdate']][0:5])
# print('The size of the whole dataset:', len(data['pl_name']))
# print('')

# # Removing the duplicates from the data
de_duped_data = DU.DeDupe(data)
de_duped_data = de_duped_data.remove_dupes()
print('The first five rows of the dataset with all duplicates removed: ')
print(de_duped_data[['pl_name', 'pl_pubdate']][0:5])
print('The size of the dataset without duplicates:', len(de_duped_data['pl_name']))
print('')
de_duped_data.to_csv('~/ASDRP/Data/DeDuped.csv', index=False)

# print('Size of BetaData:', len(beta_data))

# # Calculating the habitable zone, and extracting those planets in it
# hz_planets = HZ.HabitableZone(de_duped_data)
# hz_planets = hz_planets.calculate()
# print('The first five rows of the dataset of planets that are within their habitable zone: ')
# print(hz_planets['pl_name'][0:5])
# print('The size of the dataset of HZ planets: ', len(hz_planets['pl_name']))
#
# # Looking at M-type stars and planets
# m_types = MT.MTypes(de_duped_data, phl)
# m_types = m_types.sort()
# print('The M-type planets: ')
# print(m_types['pl_name'])
# print('')

# print(weirddata.columns)