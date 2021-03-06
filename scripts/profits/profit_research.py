# Read name files
# http://www.nber.org/~jbessen/pdpcohdr.dat.zip
# http://www.nber.org/~jbessen/dynass.dat.zip

import pandas as pd

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/dynass.dat', sep='\t', index_col='pdpass')
df2 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/pdpcohdr.dat', sep='\t')

# gvkeys for the lookup on WRDS compustat.
with open('/Volumes/HDD/Users/tom/DataStorage/Patents/gvkeys.txt', 'w') as f:
    f.write(df2[['gvkey']].to_string(index=False))

# Unique key formed by company, date
wrds = pd.read_csv(
    '/Volumes/HDD/Users/tom/DataStorage/Patents/profit_research.csv',
    parse_dates=['datadate'], index_col=['gvkey', 'datadate'])

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
s = wrds[['GP', 'XRD', 'NAICS']].dropna()

