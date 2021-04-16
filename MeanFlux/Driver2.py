# The necessary import statements
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import MeanFlux.InclinInvest as OF

exo = pd.read_csv('~/ASDRP/Data/data.csv', low_memory=False)
exo.rename(columns={'st_dist':'sy_dist', 'st_spstr':'st_spectype'}, inplace=True)
hz_planets = pd.read_csv('~/ASDRP/Data/HZplanets.csv', low_memory=False)

pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.options.mode.chained_assignment = None

print('Total size: ', len(exo))

fluxstuff = OF.FluxInvestigation(exo, hz_planets)

# fluxstuff.prelim()
# fluxstuff.moreRandom()
#
# fluxstuff.tryPlot()

img = mpimg.imread('limits.png')
imgplot = plt.imshow(img)
# plt.show()


print('')

flux_set = fluxstuff.sort_flux(hz_planets)
print('Size of flux set (applied to HZ planets): ', len(flux_set))
limited = fluxstuff.apply_limits(flux_set)
print('Size of limited set: ', len(limited))

print('Mean of original insolation values: ', limited['pl_insol'].mean())
print('Mean of the calculated fluxes: ', limited['calc_flux'].mean())
print('')

flux_set2 = fluxstuff.sort_flux(exo)
print('Size of second flux set (applied to original dataset): ', len(flux_set2))
limited2 = fluxstuff.apply_limits(flux_set2)
print('Size of second limited set: ', len(limited2))

# hz_planets
s1 = limited['pl_name']
# exo planets
s2 = limited2['pl_name']
s1.reset_index(drop=True, inplace = True)
s2.reset_index(drop=True, inplace = True)
dict = fluxstuff.compare_fluxes(s1, s2)
df = pd.DataFrame(dict)
print(df)
