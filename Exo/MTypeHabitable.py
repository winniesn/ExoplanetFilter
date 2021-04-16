# The necessary import statements
import pandas as pd
import numpy as np

# This class extracts the planets whose host stars are of the M Spectral Type (from both datasets)
class MTypes:

    # Constructor, takes two datasets as input and initializes one to hold the output
    def __init__(self, dataframe, reference):
        self.data = dataframe
        self.refdata = reference
        self.m_type_habitable = pd.DataFrame(columns=list(dataframe.columns))

    # This method will do the calculations and extracting
    def sort(self):

        data = self.data
        phl = self.refdata

        # Removes any planets that have an NA eccentricity value
        data = data[data['pl_orbeccen'].notna()]
        data = data[data['pl_rade'].notna()]

        # Resets the data row index
        data = data.reset_index(drop=True)

        # Makes an empty m_type dataframe with same column headers
        m_type = pd.DataFrame(columns=list(data.columns))

        # Fills the m_type dataframe with M-type host stars' planets
        m_type = data.loc[(data['st_spectype'].str.startswith('M', na=False))]

        # Resets the m_type row index
        m_type = m_type.reset_index(drop=True)

        # Takes out planets that have no planet radius and eccentricity
        phl = phl[phl['pl_rade'].notna()]
        phl = phl[phl['pl_orbeccen'].notna()]

        # Resets index
        phl = phl.reset_index(drop=True)

        # Makes a new empty dataframe for the m-type planets in the PHL dataset
        phl_m_type = pd.DataFrame(columns=list(phl.columns))

        # Fills the empty dataframe with m-type planets from the PHL dataset
        phl_m_type = phl.loc[(phl['st_spectype'].str.startswith('M', na=False))]

        # Resets index
        phl_m_type = phl_m_type.reset_index(drop=True)

        # Constants to be used
        closest_distance_away = 10000
        index = -1

        # Comparing radii between entries of the phl dataset and exoplanet dataset
        for i in range(len(m_type['pl_rade'])):
            current_dist = np.abs(phl_m_type['pl_rade'][0] - m_type['pl_rade'][i])
            if current_dist < 10:
                closest_distance_away = current_dist
                index = 0

            current_dist = np.abs(phl_m_type['pl_rade'][1] - m_type['pl_rade'][i])
            if current_dist < 10:
                if closest_distance_away > current_dist:
                    closest_distance_away = current_dist
                    index = 1

            current_dist = np.abs(phl_m_type['pl_rade'][2] - m_type['pl_rade'][i])
            if current_dist < 10:
                if closest_distance_away > current_dist:
                    closest_distance_away = current_dist
                    index = 2

            if index == -1 or closest_distance_away == 10000:
                continue

            planet = m_type.loc[i].copy()
            control_planet = phl_m_type.loc[index].copy()

            self.check_match(planet, control_planet)
            closest_distance_away = 10000
            index = -1

        return self.m_type_habitable

    # Compares phl planet to NASA dataset planet
    def check_match(self, planet, control_planet):
        if pd.isna(planet['pl_dens']):
            if (not pd.isna(planet['pl_radj'])) & (not pd.isna(planet['pl_massj'])):
                planet['pl_dens'] = (planet['pl_massj'] * (1.898 * (10 ** 27) * 1000)) \
                                    / (4 * np.pi * ((planet['pl_radj'] * 43441 * 160934) ** 3) / 3)
            else:
                return

        if pd.isna(planet['pl_orbsmax']) and (pd.isna(planet['pl_ratdor']) or pd.isna(planet['st_rad'])):
            return

        # Calculates orbital period in days for main planet (for those that can)
        if pd.isna(planet['pl_orbper']):
            if pd.isna(planet['pl_ratdor']):
                planet['pl_orbper'] = np.sqrt(planet['pl_orbsmax'] ** 3) * 365
            elif not pd.isna(planet['st_rad']):
                planet['pl_orbper'] = np.sqrt((planet['pl_ratdor'] * planet['st_rad']) ** 3) * 365
            if pd.isna(planet['pl_orbper']):
                return

        if pd.isna(control_planet['pl_orbsmax']) and (
                pd.isna(control_planet['pl_ratdor']) or pd.isna(control_planet['st_rad'])):
            return

        # Calculates orbital period in days for phl planet
        if pd.isna(control_planet['pl_orbper']):
            if pd.isna(control_planet['pl_ratdor']):
                control_planet['pl_orbper'] = np.sqrt(control_planet['pl_orbsmax'] ** 3) * 365
            elif not pd.isna(control_planet['st_rad']):
                control_planet['pl_orbper'] = np.sqrt(
                    (control_planet['pl_ratdor'] * control_planet['st_rad']) ** 3) * 365
            if pd.isna(control_planet['pl_orbper']):
                return

        if pd.isna(planet['pl_orbeccen']):
            return

        # Checking the correct range for density, no controversial flag, transit discovery method, and orbital period
        if (float(planet['pl_dens']) >= 4) & (float(planet['pl_dens']) <= 7):
            if planet['pl_controv_flag'] == '0':
                if 'Transit' in planet['discoverymethod']:
                    if planet['pl_orbeccen'] <= 0.2:
                        if np.abs(float(planet['pl_orbper']) - float(control_planet['pl_orbper'])) <= 50:
                            self.m_type_habitable = self.m_type_habitable.append(planet, ignore_index=True)
