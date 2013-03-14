# Read name files
# http://www.nber.org/~jbessen/pdpcohdr.dat.zip
# http://www.nber.org/~jbessen/dynass.dat.zip

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/dynass.dat', sep='\t', index_col='pdpass')
df2 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/pdpcohdr.dat', sep='\t')

# gvkeys for the lookup on WRDS compustat.
# with open('/Volumes/HDD/Users/tom/DataStorage/Patents/gvkeys.txt', 'w') as f:
#     f.write(df2[['gvkey']].to_string(index=False))

# Unique key formed by company, date
wrds = pd.read_csv(
    '/Volumes/HDD/Users/tom/DataStorage/Patents/profit_research.csv',
    index_col=['gvkey', 'datadate'])

"""
wrds.columns

Index([gvkey, datadate, fyear, indfmt, consol, popsrc, datafmt, cusip,
      CURCD, GP, XRD, COSTAT, COUNTY, NAICS], dtype=object)

gvkey is an identifier (should be unique in COMPUSTAT)
datadate is recorded date.
fyear : fiscal year?
indfmt:
consol:
popsrc:
datafmt: data format?
cusip:
CURCD: currency
GP: gross profit
XRD: research and development
county: whoops should have been country. ICO
COSTAT:
NAICS: Classifier.
"""
# Only NaNs are in XRD
df1 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/research_profit_q_1.csv',
                  index_col=['gvkey', 'datadate'], parse_dates=['datadate'])
df2 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/research_profit_q_2.csv',
                  index_col=['gvkey', 'datadate'], parse_dates=['datadate'])
df = pd.concat([df1, df2])
df = df.sort()
df.columns = map(lambda x: x.lower(), df.columns)

y = df.saleq - df.cogsq
# len(y.isnull()): 81678
y = y.fillna(method='ffill', limit=3)  # 22618 items

x = df[['xrdq']]
x.xrdq = x.xrdq.fillna(method='ffill', limit=4)
x = x.dropna()  # 385275 items
x = sm.add_constant(x)

ind = y.index.intersection(x.index)  # 385043 items
y = y.ix[ind]
y.name = 'profit'
x = x.ix[ind]

joined = x.join(y)  # len 385774


def lag_scatter(x, y, n=4):
    """
    Helper to plot lagged y against x.

    n : number of periods
    """
    return plt.scatter(x[n:], y.shift(n).dropna())


def picker(x, n=4):
    """
    Get the companies with more than n observations.

    Pass this to the groupby objcet:
    gr = j.groupby(level='gvkey', group_keys='False')
    """
    if len(x) < n:
        pass
    else:
        return x



"""
Fun Example:

sx = x.ix[1013]
sy = y.ix[1013]
plt.close()
sx.head()
j = sx.join(sy)
sy.name='profit'
j = sx.join(sy)
ax = j[['xrdq', 'profit']].plot(secondary_y=['profit'], grid=True)
plt.figure()
ax2 = lag_scatter(sx.xrdq[1:], sy[1:], n=8)
"""
suby = y.ix[:100]
subx = x.ix[:100]
