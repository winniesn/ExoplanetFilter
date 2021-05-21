# The necessary import statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi
import math
import Exo.Duplicates as Dup

pd.options.mode.chained_assignment = None

class HITE:

    def __init__(self, dataframe):
        self.data = dataframe
        self.flux_radius = pd.DataFrame(columns=['radius', 'max_Flux'])
        self.real_fr = pd.DataFrame(columns=['radius', 'max_Flux'])
        self.alb_flux_relat = pd.DataFrame(columns=['albedo', 'flux'])
        self.R_e = 6378100
        self.M_e = 5.972186e24
        self.R_s = 6.957e8
        self.M_s = 1.988416e30
        self.L_s = 3.828e26
        self.ppm = 1e-6
        self.hrsec = 3600
        self.daysec = 86400
        self.aum = 1.49598e11
        self.so_con = 1362

        self.G = 6.67428e-11
        self.B = 0.7344
        self.o = 5.67037e-8
        self.l = 2.425e6
        self.R = 461.5
        self.k = 0.055
        self.P_0 = 10 ** 4

        self.maxeccen = 0.8
        self.mineccen = 0
        self.minflux = 67
        self.albmin = 0.05
        self.albmax = 0.8

        self.data['st_rad'] = self.data['st_rad'] * self.R_s
        self.data['pl_rade'] = self.data['pl_rade'] * self.R_e
        self.data['pl_trandep'] = self.data['pl_trandep'] * self.ppm
        self.data['pl_trandur'] = self.data['pl_trandur'] * self.hrsec
        self.data['pl_orbper'] = self.data['pl_orbper'] * self.daysec

        self.data['calc_rad'] = ''
        self.data['pl_mass'] = ''
        self.data['max_Flux1'] = ''
        self.data['pl_grav'] = ''
        self.data['min_eccen'] = ''
        self.data['st_mass'] = ''
        self.data['pl_semia'] = ''
        self.data['pl_circdur'] = ''
        self.data['pl_tdanomaly'] = ''
        self.data['max_eccen'] = ''
        self.data['sy_mass'] = ''
        self.data['rocky'] = ''
        self.data['constraint'] = ''
        self.data['instellation'] = ''
        self.data['calc_lum'] = ''
        self.data['H'] = ''
        self.data['Hp'] = ''
        self.data['eccen_dist'] = ''

    # applied in this class
    def get_radius(self, trandep, st_rad):
        pl_rad = math.sqrt(trandep) * st_rad
        return pl_rad

    # applied in this class
    def get_pl_mass(self, pl_rad):
        if pl_rad / self.R_e < 1:
            pl_mass = (pl_rad / self.R_e) ** 3.268 * self.M_e
        elif pl_rad / self.R_e >= 1 and pl_rad / self.R_e < 2.5:
            pl_mass = (pl_rad / self.R_e) ** 3.65 * self.M_e
        else:
            pl_mass = (4 * pi / 3) * 1000 * (pl_rad ** 3)
        return pl_mass

    # applied in this class
    def get_st_mass(self, logg, st_rad):
        st_mass = 10 ** logg * st_rad * st_rad / self.G / 100
        return st_mass

    # applied in this class
    def get_lum(self, st_rad, st_temp):
        lum = 4 * pi * st_rad * st_rad * self.o * pow(st_temp, 4)
        return lum

    # applied in this class
    def get_instell(self, st_lum, pl_semia):
        instellation = st_lum / (4 * pi * pl_semia**2)
        return instellation

    def tryPlot(self, dataframe):
        dataframe['radius'] = dataframe['radius'] / self.R_e
        dataframe.plot.scatter(x='radius', y='max_Flux')
        plt.show()

    def compareRadii(self):
        d = {'calculated_radii': self.flux_radius['radius'],
             'original_radii': self.real_fr['radius']}
        df = pd.DataFrame(d)
        df.plot(style=['o', 'rx'])
        plt.show()

    # applied in this class
    def calc_flux(self, trandep, st_rad, i):
        pl_rad = self.get_radius(trandep, st_rad)
        pl_mass = self.get_pl_mass(pl_rad)

        scaled_P = 610.616 * math.exp(self.l / (self.R * 273.13))
        grav = self.G * pl_mass / (pl_rad ** 2)
        self.data['pl_grav'][i] = grav
        quad = self.l / (self.R * np.log(scaled_P * math.sqrt(self.k / (2 * self.P_0 * grav))))  # github version
        # quad = (l / R) / (np.log(scaled_P / ((2 * P_0 * g / k) ** (1 / 2)))) # book version
        # quad = l / (2 * R * (np.log(scaled_P * P_0 * g * math.sqrt(k)))) # paper version
        f_max = self.B * self.o * (quad ** 4)
        return f_max

    def apply_calc(self):
        for i in range(len(self.data)):
            t_d = self.data['pl_trandep'][i]
            s_r = self.data['st_rad'][i]
            logg = self.data['st_logg'][i]
            o_p = self.data['pl_orbper'][i]
            p_r = self.get_radius(t_d, s_r)
            p_m = self.get_pl_mass(p_r)
            st_mass = self.get_st_mass(logg, s_r)
            m_a = self.semia(st_mass, p_m, o_p)
            try:
                flux = self.calc_flux(t_d, s_r, i)
            except:
                flux = float('nan')
            self.data['pl_mass'][i] = p_m
            self.data['calc_rad'][i] = p_r
            self.data['max_Flux1'][i] = flux
            self.data['st_mass'][i] = st_mass
            self.data['pl_semia'][i] = m_a
            if flux < 10000:
                new_row = pd.DataFrame(index = range(0,1), columns=list(self.flux_radius.columns))
                new_row.iloc[0] = [p_r, flux]
                self.flux_radius = pd.concat([self.flux_radius, new_row], ignore_index=True)
        return self.flux_radius

    # applied in this class
    def calc_flux2(self, pl_rad):
        pl_mass = self.get_pl_mass(pl_rad)

        scaled_P = 610.616 * math.exp(self.l / (self.R * 273.13))
        grav = self.G * pl_mass / (pl_rad ** 2)
        quad = self.l / (self.R * np.log(scaled_P * math.sqrt(self.k / (2 * self.P_0 * grav))))  # github version
        # quad = (l / R) / (np.log(scaled_P / ((2 * P_0 * g / k) ** (1 / 2)))) # book version
        # quad = l / (2 * R * (np.log(scaled_P * P_0 * g * math.sqrt(k)))) # paper version
        f_max = self.B * self.o * (quad ** 4)
        return f_max

    def apply_calc2(self):
        self.data['max_Flux2'] = ''
        for i in range(len(self.data)):
            try:
                p_r = self.data['pl_rade'][i]
                flux = self.calc_flux2(p_r)
            except:
                flux = float('nan')
            self.data['max_Flux2'][i] = flux
            if flux < 10000:
                new_row = pd.DataFrame(index = range(0,1), columns=list(self.real_fr.columns))
                new_row.iloc[0] = [p_r, flux]
                self.real_fr = pd.concat([self.real_fr, new_row], ignore_index=True)
        return self.real_fr

    # applied in this class
    def semia(self, st_mass, pl_mass, pl_period):
        dSemi = pow(self.G * (st_mass + pl_mass) / (4 * pi * pi) * pl_period * pl_period, (1/3))
        return dSemi

    # applied in this class
    def anomoly(self, st_radius, pl_radius, pl_dSemi, pl_duration, pl_impact, pl_period, i):
        dCircDur = math.sqrt((1 - pl_impact ** 2) * ((st_radius + pl_radius) ** 2)) * pl_period / (pi * pl_dSemi)
        self.data['pl_circdur'][i] = dCircDur
        dTDA = pl_duration / dCircDur
        self.data['pl_tdanomaly'][i] = dTDA
        return dTDA

    # applied in this class
    def emin(self, st_rad, pl_rad, pl_semi, pl_dur, pl_imp, pl_per, i):
        dTDA = self.anomoly(st_rad, pl_rad, pl_semi, pl_dur, pl_imp, pl_per, i)
        emin = abs((dTDA ** 2 - 1) / (dTDA ** 2 + 1))
        return emin

    def min_eccen(self):

        for i in range(len(self.data)):
            p_r = self.data['calc_rad'][i]
            s_r = self.data['st_rad'][i]
            i_p = self.data['pl_imppar'][i]
            m_a = self.data['pl_semia'][i]
            o_p = self.data['pl_orbper'][i]
            t_d = self.data['pl_trandur'][i]
            try:
                eccen = self.emin(s_r, p_r, m_a, t_d, i_p, o_p, i)
            except:
                eccen = float('nan')
            self.data['min_eccen'][i] = eccen
        return self.data

    # applied in this class
    def dHillEmax(self, gamma, lambd, mu, zeta):
        dArg1 = 1 + pow(3, (4. / 3)) * (mu[0] * mu[1] / pow(zeta, (4. / 3)))
        dArg2 = pow(zeta, 3) / (mu[0] + (mu[1] / (lambd * lambd )))
        dArg3 = mu[1] * gamma[1] * lambd

        gamma[0] = (1 / mu[0]) * (math.sqrt(dArg1 * dArg2) - dArg3)

        if abs(gamma[0]) > 1: # System is Hill unstable
            return -1
        else:
            return math.sqrt(1 - gamma[0] ** 2)

    def GetEmax(self):
        i = 0
        mu = [0, 0]
        gamma = [0, 0]
        while i < len(self.data):
            iNumPl = self.data['sy_numPlanets'][i]
            position = self.data['position'][i]
            if iNumPl > 1:
                if position < iNumPl:
                    j = i + 1
                    sy_mass = self.data['st_mass'][i] + self.data['pl_mass'][i] + self.data['pl_mass'][j]
                    self.data['sy_mass'][i] = sy_mass
                    self.data['sy_mass'][j] = sy_mass
                    mu[0] = self.data['pl_mass'][i] / self.data['st_mass'][i]
                    mu[1] = self.data['pl_mass'][j] / self.data['st_mass'][i]
                    zeta = mu[0] + mu[1]
                    gamma[1] = math.sqrt(1 - self.data['min_eccen'][j] ** 2)
                    lambd = math.sqrt(self.data['pl_semia'][j] / self.data['pl_semia'][i])
                    self.data['max_eccen'][i] = self.dHillEmax(gamma, lambd, mu, zeta)
                    if position != 1:
                        k = i - 1
                        mu[1] = self.data['pl_mass'][k] / self.data['st_mass'][i]
                        zeta = mu[0] + mu[1]
                        gamma[1] = math.sqrt(1 - self.data['min_eccen'][k] ** 2)
                        lambd = math.sqrt(self.data['pl_semia'][i] / self.data['pl_semia'][k])
                        emax = self.dHillEmax(gamma, lambd, mu, zeta)
                        if emax < self.data['max_eccen'][i]:
                            self.data['max_eccen'][i] = emax
                if position == iNumPl:
                    j = i - 1
                    sy_mass = self.data['st_mass'][i] + self.data['pl_mass'][i] + self.data['pl_mass'][j]
                    self.data['sy_mass'][i] = sy_mass
                    self.data['sy_mass'][j] = sy_mass
                    mu[0] = self.data['pl_mass'][i] / self.data['st_mass'][i]
                    mu[1] = self.data['pl_mass'][j] / self.data['st_mass'][i]
                    zeta = mu[0] + mu[1]
                    gamma[1] = math.sqrt(1 - self.data['min_eccen'][j] ** 2)
                    lambd = math.sqrt(self.data['pl_semia'][i] / self.data['pl_semia'][j])
                    self.data['max_eccen'][i] = self.dHillEmax(gamma, lambd, mu, zeta)
            else:
                self.data['max_eccen'][i] = self.maxeccen
            i = i + 1
        return self.data

    # applied in this class
    def eccen_dist(self, e):

        dist = 0.1619 - 0.5352*e + 0.6358*e*e - 0.2557*pow(e,3)
        return dist

    # applied in this class
    def rocky(self, pl_rade):
        if (pl_rade / self.R_e) > 2.5:
            return 0
        elif (pl_rade / self.R_e) > 1.5:
            return 2.5 - (pl_rade / self.R_e)
        return 1

    # applied in this class
    def degen(self, emin, emax, i):
        st_lum = self.data['calc_lum'][i]
        pl_semia = self.data['pl_semia'][i]
        rocky = self.data['rocky'][i]
        fmax = self.data['max_Flux1'][i]
        dHabFact = 0
        dTot = 0
        bIHZ = 0
        bOHZ = 0
        if emax < 0 or emin > emax:
            return 0
        flux0 = st_lum / (16 * pi * pl_semia * pl_semia) # correct
        for a in np.arange(self.albmin, self.albmax, 0.01):
            flux = 0
            for e in np.arange(emin, emax, 0.01):
                flux = flux0 * (1 - a) / math.sqrt(1 - e * e)
                dTot += self.eccen_dist(e)
                if flux < fmax and flux > self.minflux:
                    dHabFact += self.eccen_dist(e)
                if flux > fmax:
                    bIHZ = 1
                if flux < self.minflux:
                    bOHZ = 1
            # new_row = pd.DataFrame(index=range(0, 1), columns=list(self.alb_flux_relat.columns))
            # new_row.iloc[0] = [a, flux]
            # self.alb_flux_relat = pd.concat([self.alb_flux_relat, new_row], ignore_index=True)
        if not bIHZ and not bOHZ:
            self.data['constraint'][i] = 0
        if bIHZ:
            self.data['constraint'][i] = 1
        if bOHZ:
            self.data['constraint'][i] = 2
        if bIHZ and bOHZ:
            self.data['constraint'][i] = 3

        return (dHabFact / dTot) * rocky

    def calc_Hp(self):
        for i in range(len(self.data)):
            self.data['calc_lum'][i] = self.get_lum(self.data['st_rad'][i], self.data['st_teff'][i])
            self.data['instellation'][i] = self.get_instell(self.data['calc_lum'][i], self.data['pl_semia'][i])
            self.data['rocky'][i] = self.rocky(self.data['calc_rad'][i])
            self.data['Hp'][i] = self.degen(self.mineccen, self.maxeccen, i)
        return self.data

    def calc_H(self):
        for i in range(len(self.data)):
            emax = self.data['max_eccen'][i]
            emin = self.data['min_eccen'][i]
            try:
                if emax < self.maxeccen:
                    self.data['H'][i] = self.degen(emin, emax, i)
                else:
                    self.data['H'][i] = self.degen(emin, self.maxeccen, i)
            except:
                self.data['H'][i] = float('nan')
        return self.data

    def sort_by(self, parameter):
        sorted = self.data.sort_values(by=[parameter], ascending= False, inplace=False, na_position='last')
        return sorted

    def make_leg(self):
        self.data[['pl_circdur', 'instellation']] = self.data[['pl_circdur', 'instellation']].apply(pd.to_numeric)
        self.data['st_rad'] = self.data['st_rad'] / self.R_s
        self.data['st_mass'] = self.data['st_mass'] / self.M_s
        self.data['calc_lum'] = self.data['calc_lum'] / self.L_s
        self.data['pl_trandep'] = self.data['pl_trandep'] / self.ppm
        self.data['pl_trandur'] = self.data['pl_trandur'] / self.hrsec
        self.data['pl_circdur'] = self.data['pl_circdur'] / self.hrsec
        self.data['pl_orbper'] = self.data['pl_orbper'] / self.daysec
        self.data['calc_rad'] = self.data['calc_rad'] / self.R_e
        self.data['pl_mass'] = self.data['pl_mass'] / self.M_e
        self.data['pl_semia'] = self.data['pl_semia'] / self.aum
        self.data['instellation'] = self.data['instellation'] / self.so_con

        return self.data

    def plot_HZ(self, data):
        data.plot.scatter(x='pl_semia', y='st_mass')
        plt.show()

    def plot_S_Hp(self, data):
        data.plot.scatter(x='instellation', y='Hp')
        plt.show()

    def plot_J_Hp(self, data):
        data.plot.scatter(x='sy_jmag', y='Hp')
        plt.show()

    def plot_albflux(self):
        self.alb_flux_relat.plot.scatter(x='albedo', y='flux')
        plt.show()