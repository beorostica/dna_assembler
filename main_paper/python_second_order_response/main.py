
# Import the necessary packages and modules:
from data import CreateCustomData
import numpy as np
import matplotlib.pyplot as plt

timeDurationHot = 3
timeDurationCold = 5
numberRepetitions = 3
dampSlow = 0.67  #Tune the overshoot
wnSlow = 0.05    #Tune the settling time
dampFast = 0.55  #Tune the overshoot
wnFast = 1       #Tune the settling time
ccd = CreateCustomData(timeDurationHot, timeDurationCold, numberRepetitions, dampSlow, wnSlow, dampFast, wnFast)

print(ccd.dataFrame)

#
indX = 1
fig, axes = plt.subplots(nrows=3, ncols=1)


indY = 2
ax = axes[0]
ccd.dataFrame.plot(ax=ax, x=ccd.listIndepColumns[indX], y=ccd.listDepenColumns[indY], color=ccd.listDepenColors[indY])
ax.set_xlim(ccd.dictIndepVariables[indX]['min'], ccd.dictIndepVariables[indX]['max'])
ax.set_ylim(min(ccd.listDepenMins), max(ccd.listDepenMaxs))
ax.xaxis.set_ticks(np.arange(ccd.dictIndepVariables[indX]['min'], ccd.dictIndepVariables[indX]['max'], 5))
ax.yaxis.set_ticks(np.arange(14, 41, 5))
ax.set_xticklabels([])
ax.set_xlabel('')
ax.set_ylabel('(a) Ideal [°C]')
ax.get_legend().remove()

indY = slice(2, 4)
ax = axes[1]
ccd.dataFrame.plot(ax=ax, x=ccd.listIndepColumns[indX], y=ccd.listDepenColumns[indY], color=ccd.listDepenColors[indY])
ax.set_xlim(ccd.dictIndepVariables[indX]['min'], ccd.dictIndepVariables[indX]['max'])
ax.set_ylim(min(ccd.listDepenMins), max(ccd.listDepenMaxs))
ax.xaxis.set_ticks(np.arange(ccd.dictIndepVariables[indX]['min'], ccd.dictIndepVariables[indX]['max'], 5))
ax.yaxis.set_ticks(np.arange(14, 41, 5))
ax.set_xticklabels([])
ax.set_xlabel('')
ax.set_ylabel('(b) Fast [°C]')
ax.get_legend().remove()

indY = slice(0, 2)
ax = axes[2]
ccd.dataFrame.plot(ax=ax, x=ccd.listIndepColumns[indX], y=ccd.listDepenColumns[indY], color=ccd.listDepenColors[indY])
ax.set_xlim(ccd.dictIndepVariables[indX]['min'], ccd.dictIndepVariables[indX]['max'])
ax.set_ylim(min(ccd.listDepenMins), max(ccd.listDepenMaxs))
ax.xaxis.set_ticks(np.arange(ccd.dictIndepVariables[indX]['min'], ccd.dictIndepVariables[indX]['max'], 5))
ax.yaxis.set_ticks(np.arange(14, 41, 5))
ax.set_xlabel(ccd.dictIndepVariables[indX]['name'] + ' ' + ccd.dictIndepVariables[indX]['unit'])
ax.set_ylabel('(c) Slow [°C]')
ax.get_legend().remove()
plt.show()
