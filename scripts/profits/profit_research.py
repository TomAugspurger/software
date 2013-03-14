# Read name files
# http://www.nber.org/~jbessen/pdpcohdr.dat.zip
# http://www.nber.org/~jbessen/dynass.dat.zip

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

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
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
df = s.select('profit')

sub = df[['xrdq', 'profit']]
sub.xrdq = sub.xrdq.fillna(method='ffill', limit=4)
sub.profit = sub.profit.fillna(method='ffill', limit=4)
sub = sub.dropna()

sub = sm.add_constant(sub)
grouped = sub.groupby(level='gvkey', group_keys=False)


def lag_scatter(x, y=None, n=4):
    """
    Helper to plot lagged y against x.

    n : number of periods
    """
    if y is None:
        return plt.scatter(x.xrdq[n:], x.profit.shift(n).dropna())
    else:
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

r = grouped.apply(picker, n=20)  # len 335479

#### Aggregate OLS ####
lag_profit = grouped.apply(lambda x: x.profit.shift(8))
sub['lag_profit'] = lag_profit

res = sm.OLS(sub.dropna().lag_profit, sub.dropna()[['const', 'xrdq']]).fit()
print(res.summary())
ax = plt.scatter(sub.dropna().xrdq, sub.dropna().lag_profit, s=4, marker='.', c='k', alpha=.5)


"""
Fun Example:

sx = joined.ix[006066]
ax = sx[['xrdq', 'profit']].plot(secondary_y=['profit'], grid=True)
plt.figure()
ax2 = lag_scatter(sx.xrdq[1:], sy[1:], n=8)
"""
suby = y.ix[:100]
subx = x.ix[:100]
