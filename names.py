import pandas as pd

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/dynass.dat', sep='\t', index_col='pdpass')
df2 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/pdpcohdr.dat', sep='\t')

# gvkeys for the lookup on WRDS compustat.
with open('/Volumes/HDD/Users/tom/DataStorage/Patents/gvkeys.txt', 'w') as f:
    f.write(df2[['gvkey']].to_string(index=False))

# For the HDFStore
# gvkey is unique for this one.
df2 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Patents/pdpcohdr.dat',
                  sep='\t', index_col='gvkey')

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
s.append('names', df2)
