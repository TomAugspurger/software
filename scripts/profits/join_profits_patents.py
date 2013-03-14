import pandas as pd

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

patents = s['utility']
profits = s.select('profit')[['xrdq', 'profit']]

# Would like a dict of compan -> patentsself.
