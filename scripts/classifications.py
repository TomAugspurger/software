from __future__ import division

import pandas as pd

bin = '/Volumes/HDD/Users/tom/DataStorage/Patents/'
xls = pd.ExcelFile(bin + 'classification_06.xls')
df = xls.parse('class06', index_col=0, parse_cols=[1, 2, 3, 4, 5, 6])

# Industries to match: Communications, Computer Hardware & Software,
# Computer Peripherials, Electronic Devices,
# Electronic business methods and software, Information Storage,
# Semiconductor Devices

p = ['Communications', r'Computer Hardware & Software',
    'Computer Peripherials', 'Electronic Devices',
    'Electronic business methods and software', 'Information Storage',
    'Semiconductor Devices']

mask = df['subcatdesc'].apply(lambda x: x in p)
# Look into df['subcatdesc'].str.contains('pattern')

idx = (mask[mask] == True).index
tech = df.ix[idx]

# subcat_ccl is the one we're interested in.
industries = set(tech['subcat_ccl'])

### Read in new df
# s = df['subcat']
# t = df[(s == 46.0) | (s == 21.0) | (s == 22.0) | (s == 23.0) |
#     (s == 24.0) | (s == 25.0)]
