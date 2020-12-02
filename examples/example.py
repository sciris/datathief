'''
Illustrate example usage of Datathief.

Figure from:

    Du Z, Xu X, Wu Y, Wang L, Cowling BJ, Meyers L.
    Serial Interval of COVID-19 among Publicly Reported Confirmed Cases.
    https://www.medrxiv.org/content/10.1101/2020.02.19.20025452v4
'''

import pylab as pl
import datathief as dt

# Read data
filename = 'du_fig1a_annotated.png'
xlim = [-10, 20]
ylim = [0, 15]
data = dt.datathief(filename, xlim=xlim, ylim=ylim)

# Plotting
fig = pl.figure(figsize=(12,4))

ax1 = pl.subplot(1,2,1)
ax1.imshow(pl.imread(filename))
ax1.set_title('Original')

ax2 = pl.subplot(1,2,2)
ax2.bar(data.x, data.y)
ax2.set_title('Extracted')
ax2.set_xlabel('Serial interval')
ax2.set_ylabel('Frequency')

pl.show()