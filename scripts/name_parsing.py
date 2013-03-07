import pandas as pd
import matplotlib.pyplot as plt

# TODO Get all telecom companies and look at the patenting around breakup.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
df = s['utility']

# df[df.pdpass == 10111144]  # AT&T

atlantic = set((11708447, 11950250, 12497055, 12497055, 11861618,
                11221126, 11221126, 11221126, 12152584, 11928964,
                11928964, 11221126, 11221126, 11759793))

south = set((11116109,
            13004129,
            12074115,
            12074115,
            13110467,
            12074115,
            12074115,
            13251827,
            12074115,
            13154939,
            12427356,
            12074115,
            12074115,
            12074115,
            12074115,
            12074115,
            13070546,
            13196038))

nynex = set((10999369,
            10861809,
            10861809,
            11615030,
            11615030,
            11615030))

sw = set((12725261,
          11694784,
          10806274,
          10790491,
          10790491))

west = set((11318627,
            11322080,
            11237194,
            11540623,
            10773771,
            11932432,
            11683563,
            11395180,
            11674494))

d = {'atlantic': atlantic, 'south': south, 'nynex': nynex, 'sw': sw,
     'west': west}


d_frames = {k: df[df.pdpass.isin(d[k])] for k in d}
counts = {}
for company, frame in d_frames.iteritems():
    counts[company] = frame.groupby('appyear')['patent'].count()

all_counts = pd.DataFrame(counts)
ax1 = all_counts.ix[:2000].plot(grid=True)
plt.savefig('../resources/att_subsidiaries.png')
ax2 = all_counts.ix[:2000].pct_change().plot(grid=True)
plt.savefig('../resources/att_subsidiaries_pc.png')
att = df[df.pdpass == 10111144].groupby('appyear')['patent'].count()
att.name = 'att'
all_counts = all_counts.join(att, how='outer')
ax3 = all_counts.ix[:2000].plot(grid=True)
plt.savefig('../resources/att_all.png')
ax4 = all_counts.ix[:2000].pct_change().plot(grid=True)
plt.savefig('../resources/att_all_pc.png')
all_counts['all'] = all_counts.sum(axis=1)
ax4 = all_counts.ix[:2000].plot(grid=True)
plt.savefig('../resources/att_all_total.png')
ax5 = all_counts.ix[:2000].pct_change().plot(grid=True)
plt.savefig('../resources/att_all_total_pc.png')
ax6 = all_counts['all'].ix[1970:2000].pct_change().plot(grid=True, label=True)
