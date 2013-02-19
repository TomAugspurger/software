"""
Files available from:
https://sites.google.com/site/patentdataproject/Home/downloads

Directly:
http://www.nber.org/~jbessen/patassg.dat.zip
http://www.nber.org/~jbessen/pat76_06_assgasc.zip
"""
from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt
try:
    from mpl_toolkits import basemap
except ImportError:
    print('Won\'t be able to plot the maps.')

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']
# Just tech industries (see classifications.py)
# {46: 'Semiconductor Devices', 21: 'Communications',
#    22: 'Computer Hardware & Software',
#    23: 'Computer Peripherials', 24: 'Information Storage',
#    25: 'Electronic business methods and software']
cat = df['subcat']
t = df[(cat == 46.0) | (cat == 21.0) | (cat == 22.0) | (cat == 23.0) |
    (cat == 24.0) | (cat == 25.0)]


## Counts by year
def by_year(df, year_col='appyear'):
    """Plots the number of patents granted by year.
    year_col can be appyear or gyear (applied vs. granted).
    """
    gr = df.groupby(df[year_col])
    fig = gr['patent'].count().plot(rot=45)
    fig.set_xlabel('Year')
    fig.set_ylabel('Patents')
    return fig


def _get_ind(s, n=10):
    """Helper to get the top n countries.
    """
    s.sort()
    return s[-n:].index


## Patents by Country
def by_country(df):
    by_ctry = df.groupby('country')['patent'].count()
    idx = _get_ind(by_ctry)
    fig = by_ctry[idx].plot(kind='barh')
    fig.set_ylabel('Patents')
    return fig, idx


## By Country and time.
def year_and_country(df, ind=None, year_col='appyear'):
    """Plot of the grants by year, differentiated by country.
    Ind is a subset of the countries you want.  If not provided,
    it will call by_country and get the 10 highest.
    """
    by_ctry_time = df.groupby(['country', year_col])['patent'].count()
    if ind is None:
        idx = _get_ind(df.groupby('country')['patent'].count())
    elif isinstance(ind, int):
        idx = _get_ind(df.groupby('country')['patent'].count(), n=ind)
    else:
        idx = ind
    by_ctry_time = by_ctry_time.ix[idx]
    by_ctry_time.index = by_ctry_time.index.swaplevel(1, 0)
    fig = (by_ctry_time.unstack()).plot()
    fig.set_xlabel('Year')
    fig.set_ylabel('Patents')
    return fig

fig1 = plt.figure()
fig1 = by_year(df)

fig2 = plt.figure()
fig2 = by_country(df)

fig3 = plt.figure()
fig3 = year_and_country(df)

fig4 = plt.figure()
fig4 = by_year(t)

fig5 = plt.figure()
fig5 = by_country(t)

fig6 = plt.figure()
fig6 = year_and_country(t)


"""
Looks like the leaders change when just software.

For all:  ['IT', 'CH', 'TW', 'CA', 'KR', 'GB', 'FR', 'DE', 'JP', 'US']
software: ['NL', 'SE', 'GB', 'CA', 'FR', 'TW', 'DE', 'KR', 'JP', 'US']
"""

## Experiments with basemap and shapefiles
# Requires http://matplotlib.org/basemap/users/installing.html
# Which relies on a C library.
"""
Doc Dump:

State map from: http://www.arcgis.com/home/item.html?id=f7f805eb65eb4ab787a0a3e1116ca7e5
matplotlib examples: http://matplotlib.org/basemap/users/examples.html
filling: http://www.geophysique.be/2011/01/27/matplotlib-basemap-tutorial-07-shapefiles-unleached/
http://matplotlib.1069221.n5.nabble.com/How-to-draw-a-specific-country-by-basemap-td15744.html
http://www.naturalearthdata.com
http://pypi.python.org/pypi/GDAL/
"""


gr = df.groupby('state')
cts = gr['patent'].count()
