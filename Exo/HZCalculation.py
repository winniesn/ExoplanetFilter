# The necessary import statements
import pandas as pd
import numpy as np
from scipy.constants import pi


class HabitableZone:

    # Constructor, takes a dataframe as input
    def __init__(self, dataframe):
        self.data = dataframe

    # Here is where the HZ calculations happen, returning a dataframe with the output
    def calculate(self):

        exo = self.data

        # Disables zero division warnings
        np.seterr(divide='ignore')

        # Checks for the presence of a stellar luminosity value for each entry, and dropping the entry if there isn't
        for i in range(len(exo['st_lum'])):
            if pd.isna(exo['st_lum'][i]) or str(exo['st_lum'][i])[0:1] == "[" or str(exo['st_lum'][i])[0:1] == "<" or str(exo['st_lum'][i])[0].isalpha():
                exo = exo.drop([i])
        # Resets the index after dropping rows
        exo = exo.reset_index(drop=True)

        # Converts it to numeric type to be used later
        exo['st_lum'] = pd.to_numeric(exo['st_lum'])

        # Unit conversion
        exo['st_lum'] = exo['st_lum'] * (3.828 * (10 ** 26))

        # Checking that the distance is readable, and dropping it if it isn't, then making it numeric
        for i in range(len(exo['sy_dist'])):
            if pd.isna(exo['sy_dist'][i]) or str(exo['sy_dist'][i])[0:1] == "[" or str(exo['sy_dist'][i])[0:1] == "<" or \
                    str(exo['sy_dist'][i])[0].isalpha():
                exo = exo.drop([i])
        exo = exo.reset_index(drop=True)
        exo['sy_dist'] = pd.to_numeric(exo['sy_dist'])

        # Calculating bolometric luminosity based on stellar luminosity and distance to its sun
        bolometric_luminosity = exo['st_lum'] / (4 * pi * exo['sy_dist'] * exo['sy_dist'])

        # Setting a range for bolometric luminosity, and dropping it if the planets falls outside the range
        for i in range(len(bolometric_luminosity)):
            if bolometric_luminosity[i] <= 0:
                exo = exo.drop([i])
        exo = exo.reset_index(drop=True)

        # Calculating bolometric magnitude based of bolometric luminosity
        with np.errstate(all='ignore'):
            bolometric_mag = -2.5 * np.log10(bolometric_luminosity)

        # Checking for a stellar effective temperature, and dropping the row if there isn't
        for i in range(len(exo['st_teff'])):
            if pd.isna(exo['st_teff'][i]):
                exo = exo.drop([i])
        exo = exo.reset_index(drop=True)
        exo['st_teff'] = pd.to_numeric(exo['st_teff'])

        # Making the spectral type of a row a string
        exo['st_spectype'] = exo['st_spectype'].astype(str)

        # BC = Bolometric Correction Constant
        # Defined by the stellar effective temperature (st_teff) or the stellar type (st_spectype)
        for i in range(len(exo['st_teff'])):
            BC = 0
            if (2400 <= exo['st_teff'][i] <= 3700) or exo['st_spectype'][i][0] == 'M':
                BC = -2.0
            elif (3700 <= exo['st_teff'][i] <= 5200) or exo['st_spectype'][i][0] == 'K':
                BC = -0.8
            elif (5200 <= exo['st_teff'][i] <= 6000) or exo['st_spectype'][i][0] == 'G':
                BC = -0.4
            elif (6000 <= exo['st_teff'][i] <= 7500) or exo['st_spectype'][i][0] == 'F':
                BC = -0.15
            elif (7500 <= exo['st_teff'][i] <= 10000) or exo['st_spectype'][i][0] == 'A':
                BC = -0.3
            elif (10000 <= exo['st_teff'][i] <= 30000) or exo['st_spectype'][i][0] == 'B':
                BC = -2.0
            # Correcting the bolometric magnitude calculated earlier based off the bolometric correction constant
            bolometric_mag[i] = bolometric_mag[i] + BC

        # Calculating absolute luminosity based of bolometric magnitude
        abs_lum = 10 ** ((bolometric_mag - 4.72) / -2.5)

        # Calculations of the boundaries of the HZ based on the absolute luminosity
        inner_boundary = np.sqrt(abs_lum / 1.1)
        outer_boundary = np.sqrt(abs_lum / 0.53)

        # Converting the orbit semi-minor axis to a number (used in checking the boundaries of the HZ)
        exo['pl_orbsmax'] = pd.to_numeric(exo['pl_orbsmax'])

        # Checking if the planet is within the boundaries, and dropping it if it isn't
        for i in range(len(exo['pl_orbsmax'])):
            axis = exo['pl_orbsmax'][i]
            if (axis < inner_boundary[i]) | (axis > outer_boundary[i]):
                exo = exo.drop([i])

        # Resetting the index
        exo = exo.reset_index(drop=True)

        # Return the final dataframe
        return exo
