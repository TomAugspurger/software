from __future__ import division, print_function, unicode_literals

import pandas as pd
import statsmodels.formula.api as smf


def _freq_parse(ind):
    """
    Use to parse the frequency.
    """
    pass


def _seasonal_factor(df, col, frequency='Q'):
    """
    Going to need the whole pandas object actually.

    Take a pandas DatetimeIndex (or probably any time object meeting
    some criteria), and return the seasonal factor.

    Example:

        s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
        df = s.select('profit')
        sub = df[['xrdq', 'profit']]

        means = sub.groupby(level=1).sum()
        means = means.join(_seasonal_factors(means, 'profit'))
    """

    trend_only = smf.ols(col + '~ np.arange(len(df))',
                         data=df).fit().fittedvalues
    ratios = df[col] / trend_only
    if frequency == 'Q':
        freq = 'quarter'
    elif frequency == 'M':
        freq = 'month'
    periods = df.index.__getattribute__(freq)
    factors = ratios.groupby(periods).mean()
    df._seasonal_factors = factors
    gr = df[col].groupby(periods)
    deseasonalized = gr.apply(lambda x: x / factors[x.name])

    return pd.DataFrame({'trend_' + col: trend_only,
                         'deseasonal_' + col: deseasonalized})
