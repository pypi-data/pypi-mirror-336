import numpy as np
import pandas as pd
import sciris as sc
import matplotlib.pyplot as plt
import starsim as ss
np; pd; sc; plt; ss

folder = '/home/cliffk/idm/hpvsim/hpvsim/data/files'

files = sc.getfilelist(folder, '*.obj')
d = sc.objdict()
with sc.timer():
    for file in files:
        d[file] = sc.load(file)

#%%
url = 'https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz'
df = sc.dataframe.read_csv(url)

#%%
country = 'Zambia'
wb = d[0]
wb_y = wb['years']
wb_cbr = wb[country]

un = df[df['Location'] == country]
un_y = un['Time']
un_cbr = un['CBR']

sc.options(dpi=200)
plt.figure()
plt.scatter(wb_y, wb_cbr, label=f'WB {country}')
plt.scatter(un_y, un_cbr, label=f'UN {country}')
plt.legend()
plt.show()