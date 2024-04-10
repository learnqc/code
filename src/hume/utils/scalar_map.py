from matplotlib import pyplot, colors, cm
import colorcet

plt = pyplot
cmap = plt.get_cmap('cet_CET_C6')
norm = colors.Normalize(vmin=0, vmax=360)
scalarMap = cm.ScalarMappable(norm=norm, cmap=cmap)
