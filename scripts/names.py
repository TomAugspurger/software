# Read name files
# http://www.nber.org/~jbessen/pdpcohdr.dat.zip
# http://www.nber.org/~jbessen/dynass.dat.zip

import pandas as pd

df = pd.read_csv('dynass.dat', sep='\t')
df2 = pd.read_csv('pdpcohdr.dat', sep='\t')
