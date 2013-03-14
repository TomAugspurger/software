"""
This combines and writes the csv files into a HDF store.

It does not alter NaNs in any way.

"""
import pandas as pd

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

df['profit'] = df.saleq - df.cogsq
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
s.append('profit', df)  # Append makes a Table (better I guess).
s.close()
# read out with s.select()
