import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi
import Exo.HZCalculation as HZ

class FluxInvestigation:

    def __init__(self, largerset, hzset):
        self.exo = largerset
        self.hz_planets = hzset

    def calc_flux(self, lum, rad, eccen):
        rad = rad * rad * 3.086 * (10**16)
        denominator = 4 * pi * rad * ((1 - eccen**2)**(1/2))
        flux = lum / denominator
        return flux

# http://brendans-island.com/blogsource/Documents/eccentricorbitplanets.pdf
# Earth-like Worlds on Eccentric Orbits: Excursions beyond the Habitable Zone
    def sort_flux(self, dataset):
        dataset.dropna(subset=['st_lum', 'sy_dist', 'pl_orbeccen'])
        if dataset['st_lum'].mean() < 1 * (10**10):
            dataset['st_lum'] = dataset['st_lum'] * (3.828 * (10 ** 26))

        dataset['calc_flux'] = ''
        for i in range(len(dataset)):
            lum = dataset.at[i, 'st_lum']
            rad = dataset.at[i, 'sy_dist']
            eccen = dataset.at[i, 'pl_orbeccen']
            try:
                dataset.at[i, 'calc_flux'] = self.calc_flux(lum, rad, eccen)
            except:
                dataset.at[i, 'calc_flux'] = float('nan')

        # self.compare_flux_types(dataset)

        Q = 1370 # W m^-2
        innerbound = 1.1 * Q
        # print('Innerbound flux: ', innerbound)
        outerbound = 0.51 * Q
        # print('Outerbound flux: ', outerbound)
        in_range = dataset.loc[(dataset['calc_flux'] >= outerbound) & (dataset['calc_flux'] <= innerbound)]
        return in_range

# https://www.aanda.org/articles/aa/pdf/2016/07/aa28073-16.pdf
# Habitability of Planets on Eccentric Orbits: Limits of the Mean Flux Approximation
    def apply_limits(self, dataset):
        if dataset['st_lum'].mean() > 1 * 10**10:
            dataset['st_lum'] = dataset['st_lum'] / (3.828 * (10 ** 26))
        limit1 = dataset.loc[dataset['pl_orbeccen'] < 0.6]
        limit2 = dataset.loc[(dataset['st_lum'] < 10**(-2)) & (dataset['pl_orbeccen'] < 0.8)]
        limit3 = dataset.loc[(dataset['st_lum'] < 10**(-4)) & (dataset['pl_orbeccen'] < 0.9)]
        frames = [limit1, limit2, limit3]
        limited = pd.concat(frames)
        return limited

    def compare_fluxes(self, s1, s2):
        map = {}
        for i in range(len(s1)):
            map.update({s1[i]:[1,0]})
        for i in range(len(s2)):
            if s2[i] in map:
                map.update({s2[i]:[1,1]})
            else:
                map.update({s2[i]:[0,1]})
        return map

    def compare_flux_types(self, dataset):
        # new dataframe whose planets have both an original flux and a new flux
        has_both = dataset.dropna(subset=['calc_flux', 'pl_insol'])
        print('Entries with both a calculated flux and an original insolation flux value entered:')
        print('Length:', len(has_both))
        print(has_both[['pl_name', 'st_lum', 'pl_orbeccen', 'pl_insol', 'calc_flux']])
        average1 = has_both['pl_insol'].mean()
        print('Average value of original fluxes: ', average1)
        average2 = has_both['calc_flux'].mean()
        print('Average value of calculated fluxes: ', average2)

    def prelim(self):
        exo = self.exo

        # filter dataframe for planets discovered using transit method
        transits = exo.loc[exo['pl_discmethod'].str.contains('Transit', na=False)]
        print('Planets discovered using Transit method: ', len(transits))
        # filter dataframe for planets discovered using RV method
        rv_planets = exo.loc[exo['pl_discmethod'].str.contains('Radial Velocity', na=False)]
        print('Planets discovered using RV method: ', len(rv_planets))
        # filter dataframe for planets with inclination value
        has_inc = exo.loc[exo['pl_orbincl'].notnull()]
        print('Planets that have the inclination value: ', len(has_inc))
        # filter dataframe for planets with mass value
        has_mass = exo.loc[exo['pl_massj'].notnull()]
        print('Planets that have the mass value: ', len(has_mass))

        # First overlap (planets that were discovered using RV method, and have an inclination value)
        RV_inc = exo.loc[(exo['pl_orbincl'].notnull()) & (exo['pl_discmethod'].str.contains('Radial Velocity', na=False))]
        print('RV Method + inclination value: ', len(RV_inc))
        # Second overlap (planets that were discovered using Transit method, and have an inclination value)
        Transit_inc = exo.loc[(exo['pl_orbincl'].notnull()) & (exo['pl_discmethod'].str.contains('Transit', na=False))]
        print('Transit Method + inclination value: ', len(Transit_inc))

        # Other first overlap (planets that were discovered using RV method, and have a mass value)
        RV_mass = exo.loc[(exo['pl_massj'].notnull()) & (exo['pl_discmethod'].str.contains('Radial Velocity', na=False))]
        print('RV Method + mass value: ', len(RV_mass))
        # Other second overlap (planets that were discovered using Transit method, and have a mass value)
        Transit_mass = exo.loc[(exo['pl_massj'].notnull()) & (exo['pl_discmethod'].str.contains('Transit', na=False))]
        print('Transit Method + mass value: ', len(Transit_mass))

        # Percent of transits with inclination value
        fraction1 = len(Transit_inc) / len(transits) * 100
        print('Percent of Transits with inclination value: ' + str(fraction1) + '%')
        # Percent of transits with mass value
        otherfraction1 = len(Transit_mass) / len(transits) * 100
        print('Percent of Transits with mass value: ' + str(otherfraction1) + '%')
        # Percent of RVs with inclination value
        fraction2 = len(RV_inc) / len(rv_planets) * 100
        print('Percent of RV planets with inclination value: ' + str(fraction2) + '%')
        # Percent of RVs with mass value
        otherfraction2 = len(RV_mass) / len(rv_planets) * 100
        print('Percent of RV planets with mass value: ' + str(otherfraction2) + '%')
        # Stable orbital configuration: inclination > 10 degrees
        unstable = has_inc.loc[has_inc['pl_orbincl'] < 10]
        print('The unstable planet: ', unstable[['pl_name', 'pl_orbper', 'pl_orbeccen', 'pl_discmethod', 'pl_massj', 'pl_orbincl']])
        # Only 1
    def tryPlot(self):
        exo = self.exo
        exo = exo.loc[(exo['pl_orbincl'].notnull()) & (exo['pl_discmethod'].str.contains('Transit', na=False))]
        exo = exo.loc[(exo['pl_massj'].notnull()) & (exo['pl_discmethod'].str.contains('Transit', na=False))]
        exo.plot.scatter(x="pl_orbincl", y="pl_massj")
        plt.show()

    def moreRandom(self):
        hz_planets = self.hz_planets

        HZ_eccens = hz_planets['pl_orbeccen'].copy()
        HZ_eccens.dropna(inplace = True)
        HZ_eccens.sort_values(ascending= False, inplace=True, na_position='last')
        print('Length of eccentricities: ', len(HZ_eccens), '(', len(hz_planets['pl_name']) - len(HZ_eccens), 'were missing)')
        print('The average: ', HZ_eccens.mean())
        print('The max value: ', HZ_eccens.max())
        print(HZ_eccens)

        # Planets in the HZ with a flux variable
        flux_planets = hz_planets['pl_insol'].copy()
        flux_planets.dropna(inplace = True)
        HZ_eccens.sort_values(ascending= False, inplace=True, na_position='last')
        print('Number of planets with an insolation flux entry: ', len(flux_planets))
        print(flux_planets)
