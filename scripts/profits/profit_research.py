# Read name files
# http://www.nber.org/~jbessen/pdpcohdr.dat.zip
# http://www.nber.org/~jbessen/dynass.dat.zip

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
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


# Looking at nans:
def check_nans(frame, n=4):
    """
    Find percentage NaN for various ffills.
    """
    xrdq_pc, profit_pc = [], []
    for i in range(n):
        temp_frame = sub.groupby(level='gvkey', group_keys=False).fillna(
            method='ffill', limit=i)
        null_xrdq = sum(temp_frame.xrdq.isnull()) / len(temp_frame)
        null_profit = sum(temp_frame.profit.isnull()) / len(temp_frame)
        xrdq_pc.append(null_xrdq)
        profit_pc.append(null_profit)
        print(
            "\nlimit={0}, xrdq={1}, profit={2}".format(i, null_xrdq,
                                                       null_profit))
    return xrdq_pc, profit_pc
# sub.xrdq = sub.xrdq.fillna(method='ffill', limit=4)
# sub.profit = sub.profit.fillna(method='ffill', limit=4)
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
res = smf.ols('lag_profit ~ xrdq', data=sub.dropna()).fit()
print(res.summary())
ax = plt.scatter(sub.dropna().xrdq, sub.dropna().lag_profit, s=4, marker='.', c='k', alpha=.5)

locations = sub['loc'].unique()

"""
Fun Example:

sx = sub.ix[006066]
ax = sx[['xrdq', 'profit']].plot(secondary_y=['profit'], grid=True)
plt.figure()
ax2 = lag_scatter(sx.xrdq[1:], sx.profit[1:], n=8)
"""


def many_plots(df, ax=None, filter=False):
    """Generator to go over outer keys (companies) of the dataframe and add
    them all to one plot.  May want pct_chng to deal with scale issues.

    Go over df.index.levels[0] but use exceptions probaly.

    example:
        gen = many_plots(sub.pct_change().dropna())
        gen2 = it.islice(gen, 50)
        for i in gen2:
            i
    """
    for idx in df.index.levels[0]:
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        try:
            if filter:
                new = df.ix[idx][['xrdq', 'profit']].apply(
                    lambda x: sm.tsa.filters.hpfilter(x)[0])
                ax = new.plot(secondary_y=['profit'], ax=ax, legend=False,
                              alpha=.25, xlim=(726952.0, 734045.0))
            else:
                ax = df[['xrdq', 'profit']].ix[idx].plot(
                    secondary_y=['profit'], ax=ax, legend=False,
                    alpha=.25, xlim=(726952.0, 734045.0))
        except (IndexError, ValueError):
            continue
        yield ax


### With Indicies
sub = df[['xrdq', 'profit', 'naics']].dropna()
sectors = sub.reset_index().groupby([
    'naics', 'datadate'])[['profit', 'xrdq']]
