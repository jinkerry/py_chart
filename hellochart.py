__author__ = 'jinfeng'

import matplotlib
import pylab as pl

x1 = [1, 2, 3, 4, 5]# Make x, y arrays for each graph
y1 = [1, 4, 9, 16, 25]
x2 = [1, 2, 4, 6, 8]
y2 = [2, 4, 8, 12, 16]
pl.plot(x1, y1, 'r')# use pylab to plot x and y
pl.plot(x2, y2, 'g')
pl.title('Plot of y vs. x')
pl.xlabel('x axis')
# make axis labels
pl.ylabel('y axis')
pl.xlim(0.0, 9.0)
# set axis limits
pl.ylim(0.0, 30.0)
pl.show()
# show the plot on the screen



