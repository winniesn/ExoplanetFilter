import pandas as pd
import numpy as np
from scipy.constants import pi
import math

# We have: stellar mass and radius, planet radius, but not planet mass
# sy_pnum = 3
R_e = 6378100
M_e = 5.972186e24
R_s = 6.957e8
M_s = 1.988416e30
L_s = 3.828e26
ppm = 1e-6
hrsec = 3600
daysec = 86400

G = 6.67428e-11
B = 0.7344
o = 5.67037e-8
l = 2.425e6
R = 461.5
k = 0.055
P_0 = 10 ** 4

trandep = 137.6 * ppm
logg = 4.74
st_rad = 0.5 * R_s
st_temp = 3846
pl_period = 10.31282204 * daysec
pl_dur = 48.3312 * hrsec
pl_impact = 0.061



def get_radius(trandep, st_rad):
    pl_rad = math.sqrt(trandep) * st_rad
    return pl_rad

pl_rad = get_radius(trandep, st_rad)

print('pl_rad (should be 0.639566): ', pl_rad / R_e)

def get_pl_mass(pl_rad):
    if pl_rad / R_e < 1:
        pl_mass = (pl_rad / R_e) ** 3.268 * M_e
    elif pl_rad / R_e >= 1 and pl_rad / R_e < 2.5:
        pl_mass = (pl_rad / R_e) ** 3.65 * M_e
    else:
        pl_mass = (4 * pi / 3) * 1000 * (pl_rad ** 3)
    return pl_mass


def get_st_mass(logg, st_rad):
    st_mass = 10 ** logg * st_rad * st_rad / G / 100
    return st_mass

pl_mass = get_pl_mass(pl_rad)
st_mass = get_st_mass(logg, st_rad)

scaled_P = 610.616 * math.exp(l / (R * 273.13))
grav = G * pl_mass / (pl_rad ** 2)
quad = l / (R * np.log(scaled_P * math.sqrt(k / (2 * P_0 * grav))))  # github version
# quad = (l / R) / (np.log(scaled_P / ((2 * P_0 * g / k) ** (1 / 2)))) # book version
# quad = l / (2 * R * (np.log(scaled_P * P_0 * g * math.sqrt(k)))) # paper version
f_max = B * o * (quad ** 4)
print('pl_mass (should be 0.232077): ', pl_mass / M_e)
print('grav (should be 5.560072): ', grav)
print('f_max (should be 277.381143):', f_max)


# min eccentricity

def getSemis(st_mass, pl_mass, pl_period):
  dSemi = (G*(st_mass + pl_mass)/(4*pi*pi)*pl_period*pl_period)**(1.0/3)
  return dSemi

pl_dSemi = getSemis(st_mass, pl_mass, pl_period)

def getTDAs(st_radius, pl_radius, pl_dSemi, pl_duration):
    dCircDur = math.sqrt((1 - pl_impact**2)*((st_radius+pl_radius)**2))*pl_period/(pi*pl_dSemi)
    dTDA = pl_duration / dCircDur
    return dTDA

dTDA = getTDAs(st_rad, pl_rad, pl_dSemi, pl_dur)

emin = abs((dTDA**2 - 1)/(dTDA**2 + 1))

print('emin (should be 0.994613): ', emin)

# data = pd.read_csv('~/ASDRP/Data/DeDuped.csv', low_memory=False)
# sortedData = data.sort_values(by=['pl_pubdate'], ascending= False, inplace=False, na_position='last')
# print(sortedData['pl_pubdate'].head(100))