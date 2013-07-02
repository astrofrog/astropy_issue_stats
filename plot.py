import numpy as np
import dateutil.parser
from datetime import datetime as dt
import matplotlib.pyplot as plt

plt.rc('axes', titlesize='medium')
plt.rc('axes', labelsize='medium')
plt.rc('xtick', labelsize='small')
plt.rc('ytick', labelsize='small')
plt.rc('xtick.major', size=2)
plt.rc('ytick.major', size=2)
plt.rc('xtick.minor', size=1)
plt.rc('ytick.minor', size=1)
plt.rc('font', family='serif')
plt.rc('axes', linewidth=0.5)
plt.rc('patch', linewidth=0.5)

release_010 = dt(2012, 6, 19)
release_020 = dt(2013, 2, 20)
release_021 = dt(2013, 4, 4)
release_022 = dt(2013, 5, 22)

def to_year_fraction(date):

    import time

    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction

created = []
for line in open('created.txt'):
    date = dateutil.parser.parse(line)
    day_of_year = to_year_fraction(date)
    created.append(day_of_year)
created = np.array(created)
created.sort()
created_n = np.arange(len(created)) + 1.

closed = []
for line in open('closed.txt'):
    date = dateutil.parser.parse(line)
    day_of_year = to_year_fraction(date)
    closed.append(day_of_year)
closed = np.array(closed)
closed.sort()
closed_n = np.arange(len(closed)) + 1.

dates = np.hstack([created, closed])
diffs = np.hstack([np.repeat(1, len(created)), np.repeat(-1, len(closed))])

order = np.argsort(dates)

dates = dates[order]
diffs = diffs[order]
total = np.cumsum(diffs)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(created, created_n, color='red', lw=2, label='total')
ax.plot(closed, closed_n, color='green', lw=2, label='closed')
ax.plot(dates, total, color='blue', lw=2, label='open')
ax.xaxis.set_ticks([2011, 2012, 2013])
ax.legend(loc=2, fontsize=12)
ax.xaxis.set_ticklabels(['2011', '2012', '2013'])
ax.axvline(to_year_fraction(release_010), color='k', ls='dashed')
ax.text(to_year_fraction(release_010) - 0.01, 1350., '0.1', rotation=90, ha='right', size=10)
ax.axvline(to_year_fraction(release_020), color='k', ls='dashed')
ax.text(to_year_fraction(release_020) - 0.01, 1350., '0.2', rotation=90, ha='right', size=10)
ax.axvline(to_year_fraction(release_021), color='k', ls='dashed')
ax.text(to_year_fraction(release_021) - 0.01, 1350., '0.2.1', rotation=90, ha='right', size=10)
ax.axvline(to_year_fraction(release_022), color='k', ls='dashed')
ax.text(to_year_fraction(release_022) - 0.01, 1350., '0.2.2', rotation=90, ha='right', size=10)
ax.set_xlabel("Time")
ax.set_ylabel("Number of issues")
ax.set_title("Astropy issues")
ax.set_xlim(2011.75, 2013.6)
fig.savefig('stats.png')