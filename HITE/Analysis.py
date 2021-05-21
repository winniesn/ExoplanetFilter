import pandas as pd
import math
import Exo.HZCalculation as HZ
import matplotlib.pyplot as plt
import MeanFlux.InclinInvest as OF
import matplotlib
import matplotlib.colors
from scipy.constants import pi


# INITIAL LEGIBILITY CONSTANTS
R_e = 6378100
M_e = 5.972186e24
R_s = 6.957e8
M_s = 1.988416e30
L_s = 3.828e26
ppm = 1e-6
hrsec = 3600
daysec = 86400
aum = 1.49598e11
so_con = 1362
G = 6.67428e-11

# INITIAL LEGIBILITY METHOD
def make_leg(data):
    data[['pl_circdur', 'instellation']] = data[['pl_circdur', 'instellation']].apply(pd.to_numeric)
    data['st_rad'] = data['st_rad'] / R_s
    data['st_mass'] = data['st_mass'] / M_s
    data['calc_lum'] = data['calc_lum'] / L_s
    data['pl_trandep'] = data['pl_trandep'] / ppm
    data['pl_trandur'] = data['pl_trandur'] / hrsec
    data['pl_circdur'] = data['pl_circdur'] / hrsec
    data['pl_orbper'] = data['pl_orbper'] / daysec
    data['calc_rad'] = data['calc_rad'] / R_e
    data['pl_mass'] = data['pl_mass'] / M_e
    data['pl_semia'] = data['pl_semia'] / aum
    data['instellation'] = data['instellation'] / so_con

    return data


# READING FUNDAMENTAL DATA
AllConfirmed = pd.read_csv('~/ASDRP/Data/AllConfirmed_(29398).csv', low_memory=False)
TESSConfirmed = pd.read_csv('~/ASDRP/Data/TESSConfirmed_(125).csv', low_memory=False)
DeDuped = pd.read_csv('~/ASDRP/Data/DeDuped.csv', low_memory=False)
# print('Length of DeDuped: ', len(DeDuped))
compilation = pd.read_csv('~/ASDRP/Data/compilation.csv', low_memory=False)
# print('Length of Compilation: ', len(compilation))

# READING H AND H' DATA
    # H'
ACHP = pd.read_csv('~/ASDRP/Data/Hp Values/AllConfirmedHp.csv', low_memory=False)
TCHP = ACHP.loc[ACHP['disc_facility'] == 'Transiting Exoplanet Survey Satellite (TESS)']
KHP = pd.read_csv('~/ASDRP/Data/Hp Values/KOIsHp.csv', low_memory=False)
THP = pd.read_csv('~/ASDRP/Data/Hp Values/TOIsHp.csv', low_memory=False)

    # H
ACH = pd.read_csv('~/ASDRP/Data/H Values/AllConfirmedH.csv', low_memory=False)
TCH = ACH.loc[ACHP['disc_facility'] == 'Transiting Exoplanet Survey Satellite (TESS)']
KH = pd.read_csv('~/ASDRP/Data/H Values/KOIsH.csv', low_memory=False)

# SORTING THE H AND H' DATA
    # H'
ACHP = ACHP.loc[ACHP['Hp'] > 0]
ACHP.reset_index(inplace = True, drop = True)
print('Number of non-zero Hp in AllConfirmed: ', len(ACHP))

TCHP = TCHP.loc[TCHP['Hp'] > 0]
TCHP.reset_index(inplace = True, drop = True)
print('Number of non-zero Hp in TESSConfirmed: ', len(TCHP))
KHP = KHP.loc[KHP['Hp'] > 0]
KHP.reset_index(inplace = True, drop = True)
print('Number of non-zero Hp in KOIs: ', len(KHP['Hp']>0))
THP = THP.loc[THP['Hp'] > 0]
THP.reset_index(inplace = True, drop = True)
print('Number of non-zero Hp in TOIs: ', len(THP['Hp']>0))

    # H
ACH = ACH.loc[ACH['H'] > 0]
ACH.reset_index(inplace = True, drop = True)
print('Number of non-zero H in AllConfirmed: ', len(ACH['H']>0))
ACH.sort_values(by=['H'], ascending= False, inplace=True, na_position='last')
print(ACH[['pl_name', 'H']][0:5])
TCH = TCH.loc[TCH['H'] > 0]
TCH.reset_index(inplace = True, drop = True)
print('Number of non-zero H in TESSConfirmed: ', len(TCH['H']>0))
KH = KH.loc[KH['H'] > 0]
KH.reset_index(inplace = True, drop = True)
print('Number of non-zero H in KOIs: ', len(KH['H']>0))

# MAKING DATASET WITH H, H', AND NO H - DONE
# compilation = ACH.copy()
# for i, row in ACHP.iterrows():
#     planet = row['pl_name']
#     row = pd.DataFrame([row])
#     if planet not in compilation['pl_name'].values:
#         compilation = pd.concat([row, compilation], ignore_index=True)
# print('Second length of comp: ', len(compilation))
# for i, row in DeDuped.iterrows():
#     planet = row['pl_name']
#     row = pd.DataFrame([row])
#     if planet not in compilation['pl_name'].values:
#         compilation = pd.concat([row, compilation], ignore_index=True)
# compilation.to_csv('~/ASDRP/Data/compilation.csv', index=False)

# FINAL DATA SETS:
#   AllConfirmed, TESSConfirmed, DeDuped, Compilation
#   ACHP, TCHP, KHP, THP
#   ACH, TCH, KH    (TOIs had no impact parameter, hence no H set)




# TESS TRAIT ANALYSIS
# print('Length of TESS planets: ', len(TESSConfirmed))
# map = {}
# for i, row in TESSConfirmed.iterrows():
#     spec_type = row['st_spectype']
#     spec_letter = str(spec_type)[0:1]
#     if spec_letter in map.keys():
#         map[spec_letter] = map[spec_letter] + 1
#     else:
#         map.update({spec_letter:1})
# print(map)


# METHODS WRITTEN HERE

counter = 0
def get_radius(data):
    data['pl_trandep'] = data['pl_trandep'] * 10000

    data['st_rad'] = data['st_rad'] * R_s
    data['pl_rade'] = data['pl_rade'] * R_e
    data['pl_trandep'] = data['pl_trandep'] * ppm
    data['pl_trandur'] = data['pl_trandur'] * hrsec
    data['pl_orbper'] = data['pl_orbper'] * daysec

    for i in range(len(data)):
        try:
            data['calc_rad'][i] = math.sqrt(data['pl_trandep'][i]) * data['st_rad'][i]
            print(data['calc_rad'][i])
        except:
            data['calc_rad'][i] = float('nan')
    return data

def get_pl_mass(data):
    for i in range(len(data)):
        try:
            pl_rad = data['calc_rad'][i]
            if pl_rad / R_e < 1:
                pl_mass = (pl_rad / R_e) ** 3.268 * M_e
            elif pl_rad / R_e >= 1 and pl_rad / R_e < 2.5:
                pl_mass = (pl_rad / R_e) ** 3.65 * M_e
            else:
                pl_mass = (4 * pi / 3) * 1000 * (pl_rad ** 3)
            data['pl_mass'][i] = pl_mass
        except:
            data['pl_mass'][i] = float('nan')
    return data

def get_st_mass(data):
    for i in range(len(data)):
        try:
            logg = data['st_logg'][i]
            st_rad = data['st_rad'][i]
            st_mass = 10 ** logg * st_rad * st_rad / G / 100
            data['st_mass'][i] = st_mass
        except:
            data['st_mass'][i] = float('nan')
    return data

def semia(data):
    for i in range(len(data)):
        try:
            st_mass = data['st_mass'][i]
            pl_mass = data['pl_mass'][i]
            pl_period = data['pl_orbper'][i]
            dSemi = pow(G * (st_mass + pl_mass) / (4 * pi * pi) * pl_period * pl_period, (1 / 3))
            data['pl_semia'][i] = dSemi
        except:
            data['pl_semia'][i] = float('nan')
    return data

# compilation = get_radius(compilation)
# print('Counter: ', counter)
# compilation = get_pl_mass(compilation)
# compilation = get_st_mass(compilation)
# compilation = semia(compilation)
# compilation = compilation.loc[compilation['pl_semia'] > 0]
# print('How many actually turning out ugh: ', len(compilation))
# compilation.to_csv('~/ASDRP/Data/compilation.csv', index=False)

def plot_methods(data):
    # Color scheme: HZ == True -> green (0), Hp > 0 -> red (1), neither -> black (2), both -> blue (3)
    colors = ['green', 'red', 'black', 'blue']
    color_indices = data['HZ']
    colormap = matplotlib.colors.ListedColormap(colors)
    data.plot.scatter(x='pl_semia', y='st_mass', c=color_indices, cmap=colormap)
    plt.title('Habitable Zone')
    plt.xlabel("Planet Semi-major Axis")
    plt.ylabel("Stellar Mass")
    plt.show()

def calc_HZ(data):
    HZ_object = HZ.HabitableZone(data)
    hz_planets = HZ_object.calculate()
    return hz_planets

def apply_methodologies(input_data, input_hz_planets):
    input_data.rename(columns={'st_dist': 'sy_dist'}, inplace=True)
    # Color scheme: HZ == True -> green (0), Hp > 0 -> red (1), neither -> black (2), both -> blue (3)
    input_data['HZ'] = ''
    for i, row in input_data.iterrows():
        planet = row['pl_name']
        if row['Hp'] > 0:
            if planet in input_hz_planets['pl_name'].values:
                input_data['HZ'][i] = 3
            else:
                input_data['HZ'][i] = 1
        else:
            if planet in input_hz_planets['pl_name'].values:
                input_data['HZ'][i] = 0
            else:
                input_data['HZ'][i] = 2
    return input_data


def plot_RvFlux(data):
    data.plot.scatter(x='calc_rad', y='max_Flux1')
    plt.title('Radius vs. Flux')
    plt.xlabel("Planet Radius")
    plt.ylabel("Limiting Flux")
    plt.show()

def plot_S_Hp(data):
    data.plot.scatter(x='instellation', y='Hp')
    plt.title('S vs. H\'')
    plt.xlabel("Intellation")
    plt.ylabel("HITE Prime")
    plt.show()

def plot_J_Hp(data):
    # Color scheme: Teff >= 3800 -> black, 3400 < Teff < 3800 -> orange, Teff <= 3400 -> red
    # Size scheme: calc_rad >= 2.5 -> big, 1 < calc_rad < 2.5 -> medium, calc_rad <= 1 -> small
    data = data.dropna(subset=['sy_jmag'])
    data['color code'] = 0 # orange
    for i in range(len(data)):
        temp = data['st_teff'][i]
        if temp >= 3800:
            data['color code'][i] = 1 # red
        elif temp <= 3400:
            data['color code'][i] = 2 # yellow
    size = data['calc_rad']
    sizevalues = [i * 10 ** 1.2 for i in size]
    colors = ['orange', 'red', 'yellow']
    color_indices = data['color code']
    colormap = matplotlib.colors.ListedColormap(colors)
    data.plot.scatter(x='sy_jmag', y='Hp', s=sizevalues, c=color_indices, cmap=colormap)
    plt.title('J mag vs. H\'')
    plt.xlabel("J Magnitude")
    plt.ylabel("HITE Prime")
    plt.show()

def M_exception(data, hz_planets):
    fluxstuff = OF.FluxInvestigation(data, hz_planets)
    flux_set = fluxstuff.sort_flux(data)
    flux_set = fluxstuff.apply_limits(flux_set)
    for i in range(len(data)):
        if str(data['st_spectype'][i]) != 'nan':
            star_letter = str(data['st_spectype'][i])[0:1]
            star_num = int(str(data['st_spectype'][i])[1:2])
            star_class = str(data['st_spectype'][i])[3:4]
            planet = data['pl_name'][i]
            if star_letter == 'M' and star_num > 4 and star_class == 'V':
                if planet not in flux_set['pl_name'].values:
                    data['H'][i] = 0
                    data['Hp'][i] = 0
    return data



# OVERALL ANALYSIS BEGINS HERE
# data = ACHP.copy()
#
# hz_planets = calc_HZ(data)
# data = apply_methodologies(data, hz_planets)
# expanded_method = M_exception(data, hz_planets)
#
# comp_hz_planets = calc_HZ(compilation)
# comp_data = apply_methodologies(compilation, comp_hz_planets)
#
# data = make_leg(data)

ACHP.sort_values(by=['Hp', 'pl_orbper'], ascending= [0,0], inplace=True, na_position='last')
ACHP = make_leg(ACHP)
print(ACHP[['pl_name', 'Hp', 'pl_orbper', 'sy_jmag']][0:5])
top_planet = ACHP.iloc[0]
print('Top Planet: ')
print(top_planet[['pl_name', 'hostname', 'pl_orbper', 'calc_rad', 'sy_jmag', 'st_spectype', 'Hp', 'H', 'st_teff', 'pl_mass']])

# plot_RvFlux(data)
# plot_methods(data)
# plot_methods(comp_data)
# plot_S_Hp(data)
# plot_J_Hp(data)
