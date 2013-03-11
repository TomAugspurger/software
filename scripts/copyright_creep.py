import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1790, 2001)


def f(x):
    if x < 1832: return 28
    elif x < 1910: return 42
    elif x < 1977: return 56
    elif x < 1998: return 75
    else: return 95

y = map(f, x)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
ax.plot(x, y, 'k')
ax.set_xlim(1790)
ax.set_ylabel('Years of Protection')
ax.set_title('Copyright Creep')
ax.set_xticks([1790, 1831, 1909, 1976, 1998])
ax.set_yticks([28, 42, 56, 75, 95])

ax.annotate('Books', xy=(1790, 28), xycoords='data',
            xytext=(1800, 21), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Prints', xy=(1800, 28), xycoords='data',
            xytext=(1820, 23), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Sheet Music', xy=(1832, 42), xycoords='data',
            xytext=(1832, 25), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Photographs', xy=(1890, 42), xycoords='data',
            xytext=(1850, 30), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('All literary works', xy=(1909, 42), xycoords='data',
            xytext=(1909, 25), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Corporate authorship', xy=(1909, 42), xycoords='data',
            xytext=(1920, 30), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Sound recordings', xy=(1909, 42), xycoords='data',
            xytext=(1940, 35), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Motion pictures', xy=(1909, 42), xycoords='data',
            xytext=(1945, 40), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Computer software', xy=(1971, 56), xycoords='data',
            xytext=(1950, 45), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

ax.annotate('Automatic renewal', xy=(1990, 75), xycoords='data',
            xytext=(1980, 48), textcoords='data',
            arrowprops=dict(arrowstyle="->"), size=16, family='serif')

for loc, spine in ax.spines.items():
    if loc in ['left', 'bottom']:
        continue
    if loc in ['right', 'top']:
        spine.set_color('none')  # don't draw spine
    else:
        raise ValueError('unknown spine location: %s' % loc)
# Get rid of floating ticks:
for i, t in enumerate(ax.get_xticklines()):
    if i % 2 == 1:
        t.set_alpha(0)

for i, t in enumerate(ax.get_yticklines()):
    if i % 2 == 1:
        t.set_alpha(0)

plt.savefig('../resources/copyright_creep.png', dpi=300)
