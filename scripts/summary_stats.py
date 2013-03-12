from __future__ import division

import matplotlib

matplotlib.use("AGG")
"""
Files available from:
https://sites.google.com/site/patentdataproject/Home/downloads

Directly:
http://www.nber.org/~jbessen/patassg.dat.zip
http://www.nber.org/~jbessen/pat76_06_assgasc.zip
"""

import numpy as np
import pandas as pd
from pandas.io.data import DataReader
import matplotlib.pyplot as plt
from patent_lookup import Lookup
# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']
gdp = DataReader('GDPC1', data_source='fred',
                 start='1975').resample('A').pct_change()


# df = df[df.duplicated('patent')]  # Drop the dupes for multiple assignees.
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
# To adjust for population
try:
    popn = DataReader('CNP16OV', data_source='fred', start='1970')
    popn = popn.resample('A')
    gdp = DataReader('GDPC1', data_source='fred',
                     start='1974').resample('A')
except IOError:
    print('No Connection.')

## Counts by year
def by_year(df, year_col='appyear', adj=False, style='k-', ax=None):
    """
    Plots the number of patents granted by year.
    year_col can be appyear or gyear (applied vs. granted).

    hjtwt is an adjustment for **citations** not for applications or grants.
    """
    if adj and year_col != 'allcites':
        raise ValueError('Only use adjustment with cites.')
    if adj:
        gr = df.groupby(df[year_col])
        # the .mean() of hjtwt does nothing.  Should all be the same within a year
        fig = (gr.count()['patent'] * gr.mean()['hjtwt']).plot(
            rot=45, style=style, ax=ax)
        fig.set_xlabel('')
        fig.set_ylabel('Number of Patents')
    else:
        gr = df.groupby(df[year_col])
        fig = gr['patent'].count().plot(style=style, ax=ax)
        fig.set_xlabel('')
        fig.set_ylabel('Number of Patents')
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

# By application year, adjusted and unadjusted

fig = plt.figure()
ax1 = fig.add_subplot(111)
fig1, ax1 = by_year(df, ax=ax1)
ax1.set_title('Patents by Application Year')
ax1.set_xlim(1975, 2002)
# ax1.set_yscale('log')
# fig.tight_layout()
plt.savefig('../resources/application_year.png', dpi=300)

# Both twined
cts = df.groupby(df['appyear'])['patent'].count()
ctst = t.groupby(t['appyear'])['patent'].count()
j = pd.concat([cts, ctst], axis=1)
j.columns = ['All', 'Tech']

fig = plt.figure()
ax = fig.add_subplot(111)

j.ix[1975:2002].plot(secondary_y=['Tech'], grid=True, ax=ax)
ax.set_xlabel('')
ax.set_ylabel('Patents Granted')

plt.savefig('../resources/tech_and_all.png', dpi=300)
# By grant year, adjusted and unadjusted
fig = plt.figure()
ax1 = fig.add_subplot(111)
fig1, ax1 = by_year(df, ax=ax1, year_col='gyear')
ax1.set_title('Patents by Grant Year')
ax1.set_xlim(1975, 2002)
# ax1.set_yscale('log')
# fig.tight_layout()
plt.savefig('../resources/grant_year.png', dpi=300)

# All and tech by country:
# Maybe limit to 90's on
by_ctry = df.groupby('country')['patent'].count()
t_by_ctry = t.groupby('country')['patent'].count()
idx = _get_ind(by_ctry)
t_idx = _get_ind(t_by_ctry)

comb = pd.DataFrame([by_ctry[idx], t_by_ctry[t_idx]]).T
comb.columns = ['All', 'Tech']

miss_all = comb[pd.isnull(comb['All'])].index
for ctry in miss_all:
    comb.ix[ctry]['All'] = df.groupby('country')['patent'].count().ix[ctry]

miss_tech = comb[pd.isnull(comb['Tech'])].index
for ctry in miss_tech:
    comb.ix[ctry]['Tech'] = t.groupby('country')['patent'].count().ix[ctry]

# This would be fun to animate. Composition may change though.  Needn't though.
ax = comb.plot(kind='barh', stacked=True)
ax.set_xlabel('Patents Granted')
ax.set_xticks([200000, 600000, 1000000, 1400000, 1800000])
plt.savefig('../resources/by_country.png', dpi=300)
normed = comb.div(comb.sum(1), axis=0)
ax2 = normed.plot(kind='barh', stacked=True)
ax2.set_xlabel('Proportion of Tech Patents')
plt.savefig('../resources/by_country_normalized.png', dpi=300)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
fig3, ax3 = year_and_country(df, ind=idx, adj=True)
ax3.set_xlim(1975, 2002)

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
fig4, ax4 = by_year(t, ax=ax4)
ax4.set_title('Tech Patents by Application Year')
ax4.set_xlim(1975, 2002)
plt.savefig('../resources/tech_patents_by_year.png', dpi=300)

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

cats = ['icl', 'icl_class', 'iclnum', 'cat', 'cat_ocl', 'cclass', 'subcat', 'subcat_ocl', 'subclass', 'subclass1', 'subclass1_ocl', 'subclass_ocl', 'nclass', 'nclass_ocl']

jcats = df[cats]
gr = df[['patent']].groupby((jcats['cat'], df['appyear']))
by_cat_ts = gr.count().unstack(level='cat').ix[1975:2002]
d = {('patent', 1.0): 'chemical', ('patent', 2.0): 'computers', ('patent', 3.0): 'medical',
     ('patent', 4.0): 'electronic', ('patent', 5.0): 'mechanical', ('patent', 6.0): 'other'}
by_cat_ts = by_cat_ts.rename(columns=d)
plt.figure()
ax = by_cat_ts.plot(grid=True)
ax.set_xlabel('')
ax.set_xlim(1975, 2002)
ax.set_ylabel('Patents Granted')
plt.savefig('../resources/by_cat_year.png')


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
