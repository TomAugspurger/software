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
from patent_lookup import Lookup

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']
"""
Just tech industries (see classifications.py)
{46: 'Semiconductor Devices', 21: 'Communications',
   22: 'Computer Hardware & Software',
   23: 'Computer Peripherials', 24: 'Information Storage',
   25: 'Electronic business methods and software']
Some companies of note:
{'amazon': 737570,
'apple' : 32940,
'apple2': 799370,
'google': 706518,?
'att': 706518,
'microsoft' : 373780,
'oracle' :,
'sun' :,
'ibm': 280070
}
"""
cat = df['subcat']
t = df[(cat == 22.0) | (cat == 24.0) | (cat == 25.0)]


## Counts by year
def by_year(df, year_col='appyear', adj=False, style='k-', ax=None):
    """
    Plots the number of patents granted by year.
    year_col can be appyear or gyear (applied vs. granted).
    """
    if adj:
        gr = df.groupby(df[year_col])
        # the .mean() of hjtwt does nothing.  Should all be the same within a year
        fig = (gr.count()['patent'] * gr.mean()['hjtwt']).plot(rot=45, style=style)
        fig.set_xlabel('Year')
        fig.set_ylabel('Patents')
    else:
        gr = df.groupby(df[year_col])
        gr = df.groupby(df[year_col])
        fig = gr['patent'].count().plot(rot=45)
        fig.set_xlabel('Year')
        fig.set_ylabel('Patents')
    ax = fig.axes
    return fig, ax


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
    ax = fig.axes
    return fig, ax, idx


## By Country and time.
def year_and_country(df, ind=None, year_col='appyear', adj=False):
    """Plot of the grants by year, differentiated by country.
    Ind is a subset of the countries you want.  If not provided,
    it will call by_country and get the 10 highest.

    adj: Bool defaults to True.  If true we'll scale by the hjtwt calculation.
    """
    if ind is None:
        idx = _get_ind(df.groupby('country')['patent'].count())
    elif isinstance(ind, int):
        idx = _get_ind(df.groupby('country')['patent'].count(), n=ind)
    else:
        idx = ind
    if adj:
        gr = df.groupby(['country', year_col])
        by_ctry_time = gr['patent'].count() * gr['hjtwt'].mean()
    else:
        by_ctry_time = df.groupby(['country', year_col])['patent'].count()

    by_ctry_time = by_ctry_time.ix[idx]
    by_ctry_time.index = by_ctry_time.index.swaplevel(1, 0)
    fig = (by_ctry_time.unstack()).plot()
    fig.set_xlabel('Year')
    fig.set_ylabel('Patents')
    ax = fig.axes
    return fig, ax

# By year, adjusted and unadjusted

fig = plt.figure()
ax1 = fig.add_subplot(111)
fig1, ax1 = by_year(df, adj=True)
ax1_2 = fig.add_subplot(111)
fig1, ax1_2 = by_year(df)
ax1.set_xlim(1970.)

fig2 = plt.figure()
fig2, ax2, idx = by_country(df)


fig3 = plt.figure()
fig3, ax3 = year_and_country(df, ind=idx, adj=True)
ax3.set_xlim(1970)

fig4 = plt.figure()
fig4, ax4 = by_year(t)
ax4.set_xlim(1970)

fig5 = plt.figure()
fig5, ax5, idx = by_country(t)

fig6 = plt.figure()
fig6, ax6 = year_and_country(t)


## Select the lagest Not working.  Need to figure out
# just what the groupby apply is returning.
# def get_largest(t, c=1500):
#     """
#     Return just those with at least c patents.
#     c = 1500 returns 25 for this version.
#     """
#     gr = t['patent'].groupby(t['uspto_assignee'])
#     large_idx = gr.apply(lambda x: len(x) > c)
#     m = t['uspto_assignee']
#     return t[m.isin(large_idx.index[large_idx])]


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


### Really should break this into multiple files:
### Section citations

def get_most_cited():
    s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
    ser = s['cites']['cited']
    s.close()
    r = ser.value_counts()
    patent_num = r.index[0]
    cited = r[patent_num]
    c = Lookup(patent_num)
    return c, cited

r, number = get_most_cited()
r.patent_to_web().next()
# Bubble jet recording method and apparatus in which a heating element
# generates bubbles in a liquid flow path to project droplets.
# Ink jet printers!  Canon gets 1 & 2; 3 is DNA
