import pandas as pd
import numpy as np

url = 'https://raw.githubusercontent.com/allench36/NASA-Caltech-Exoplanet-Archive/master/updatedexoplanet.csv'

exo = pd.read_csv(url)

pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None

# Variables needed for K2-18b
K2orbperiod = exo['pl_orbper'][1093]
K2eccentricity = exo['pl_orbeccen'][1093]
K2dist = exo['st_dist'][1093]

# create new dataframe for planets with jupiter radii value, mass value, and no density value
new_exo_mass = exo.loc[(exo['pl_dens'].isnull()) & (exo['pl_radj'].notnull()) & (exo['pl_massj'].notnull())]

# filter original dataframe for planets with density value
exo = exo.loc[exo['pl_dens'].notnull()]

# calculate densities for child dataframe
new_exo_mass['pl_dens'] = (new_exo_mass['pl_massj'] * (1.898 * (10 ** 27) * 1000)) \
                          / (4 * np.pi * ((new_exo_mass['pl_radj'] * 43441 * 160934) ** 3) / 3)

# append everything into 'total_dens'
total_dens = exo.append(new_exo_mass, ignore_index=True)

# create child with 'pl_orbper' value
total_y_orbper = total_dens.loc[total_dens['pl_orbper'].notnull()]
# create child with no 'pl_orbper' and 'pl_ratdor' but with 'pl_orbsmax'
total_n_orbper = total_dens.loc[
    (total_dens['pl_orbper'].isnull()) & (total_dens['pl_ratdor'].isnull()) & (total_dens['pl_orbsmax'].notnull())]

# calculate 'pl_orbper' for planets without it
total_n_orbper['pl_orbper'] = np.sqrt(total_n_orbper['pl_orbsmax'] ** 3) * 365

# append all child dataframes into 'total_orbper'
total_orbper = total_y_orbper.append(total_n_orbper, ignore_index=True)

# filter out planets without 'pl_orbeccen' value
total = total_orbper.loc[total_orbper['pl_orbeccen'].notnull()]

# filter by matching K2-18b (M-type host star, density between 4 and 7 g/cm^3, no controversy
# discovered via transit, eccentricity 0.2 or less, orbital period +-12)
total = total.loc[(total['st_spstr'].str.startswith('M', na=False)) & (total['pl_dens'] >= 4) & (total['pl_dens'] <= 7)
                  & (total['pl_controvflag'] == 0) & (total['pl_discmethod'].str.contains('Transit', na=False)) & (
                              total['pl_orbeccen'] <= 0.2)
                  & (np.abs(total['pl_orbper'] - K2orbperiod) <= 12)]

total.reset_index(drop=True, inplace=True)

# print out planets matching the criteria excluding K2-18 b
total = total.loc[total['pl_name'] != 'K2-18 b']
print(total['pl_name'])
print(total['pl_orbeccen'])
print(total['pl_orbper'])


# Variables needed for K2-18b
orbperiodK2 = exo['pl_orbper'][1093]
K2Eccentricity = exo['pl_orbeccen'][1093]

# Drops any planets that are not M-type stars
star_type = exo['st_spstr']
for i in range(len(exo)):
    s = star_type[i]
    if pd.isna(star_type[i]):
        exo = exo.drop([i])
    else:
        if not s[0:1] == "M":
            exo = exo.drop([i])

# Drops any rows that cannot have orbital period calculated
exo = exo.reset_index(drop=True)
for i in range(len(exo['pl_ratdor'])):
    if pd.isna(exo['pl_orbsmax'][i]) and (pd.isna(exo['pl_ratdor'][i]) or pd.isna(exo['st_rad'][i])):
        exo = exo.drop([i])
exo = exo.reset_index(drop=True)

# Calculates orbital period in days
for i in range(len(exo['pl_ratdor'])):
    if pd.isna(exo['pl_orbper'][i]):
        if pd.isna(exo['pl_ratdor'][i]):
            exo['pl_orbper'][i] = np.sqrt(exo['pl_orbsmax'][i] ** 3) * 365
        elif not pd.isna(exo['st_rad'][i]):
            exo['pl_orbper'][i] = np.sqrt((exo['pl_ratdor'][i] * exo['st_rad'][i]) ** 3) * 365
        else:
            exo = exo.drop([i])

exo = exo.reset_index(drop=True)

orbperiod = exo['pl_orbper']

for i in range(len(orbperiod)):  # Loops through values in orbperiod
    if np.abs(orbperiod[i] - orbperiodK2) > 20:  # Checks if value is 20 units away from K2-18b value
        exo = exo.drop([i])  # If it is more than 20 units away, it removes that planet

exo = exo.reset_index(drop=True)

for i in range(len(exo['pl_orbeccen'])):
    if pd.isna(exo['pl_orbeccen'][i]):  # If eccentricity is empty, drop it
        exo = exo.drop([i])
    elif np.abs(exo['pl_orbeccen'][i] - K2Eccentricity) > 0.25:  # If eccentricity is 0.25 away from K2-18b, drop it
        exo = exo.drop([i])
exo = exo.reset_index(drop=True)

print(exo['pl_hostname'] + " " + exo['pl_letter'])

df = pd.read_csv(url)

for row in df.index:
    st_dist = df.loc[row, 'st_dist']
    st_optmag = df.loc[row, 'st_optmag']
    absolute_magnitude = st_optmag - 5 * np.log10(st_dist / 10)
    if df.loc[row, 'st_teff'] >= 2400 and df.loc[row, 'st_teff'] <= 3700:
        BC = -2.0
    elif df.loc[row, 'st_teff'] >= 3700 and df.loc[row, 'st_teff'] <= 5200:
        BC = -0.8
    elif df.loc[row, 'st_teff'] >= 5200 and df.loc[row, 'st_teff'] <= 6000:
        BC = -0.4
    elif df.loc[row, 'st_teff'] >= 6000 and df.loc[row, 'st_teff'] <= 7500:
        BC = -0.15
    elif df.loc[row, 'st_teff'] >= 7500 and df.loc[row, 'st_teff'] <= 10000:
        BC = -0.3
    elif df.loc[row, 'st_teff'] >= 10000 and df.loc[row, 'st_teff'] <= 30000:
        BC = -2.0
    bolometric_magnitude = absolute_magnitude + BC
    absolute_luminosity = 10 ** ((bolometric_magnitude - 4.72) / -2.5)
    inner_bound = np.sqrt(absolute_luminosity / 1.1)
    outer_bound = np.sqrt(absolute_luminosity / 0.53)
    axis = df.loc[row, 'pl_orbsmax']
    if axis > inner_bound and axis < outer_bound:
        print(df.loc[row, 'pl_name'])