#!/usr/bin/env python
'''
Real-time scrolling multi-plot over time.

Requires: matplotlib
          numpy

Demo:
         python realtime_plot.py

Adapted from example in http://stackoverflow.com/questions/8955869/why-is-plotting-with-matplotlib-so-slow

Copyright (C) 2015 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class RealtimePlotter(object):
    '''
    Real-time scrolling multi-plot over time.  Your data-acquisition code should run on its own thread,
    to prevent blocking / slowdown.
    '''

    def _bozo(self, nrows, propvals, propname, dflt):
        retval = [dflt]*nrows
        if propvals:
            if len(propvals) != nrows:
                raise Exception('Provided %d ylims but %d %s' % (nrows, len(propvals), propname))
            else:
                retval = propvals
        return retval

    def _handle_close(self, event):

        self.is_open = False

    def __init__(self, ylims, size=100, window_name=None, styles=None, ylabels=None, interval_msec=10):
        '''
        Initializes a multi-plot with specified Y-axis limits as a list of pairs; e.g., 
        [(-1,+1), (0.,5)].  Optional parameters are:
       
        size          size of display (X axis) in arbitrary time steps
        window_name   name to display at the top of the figure
        styles        plot styles (e.g., 'b-', 'r.')
        ylabels       Y-axis labels
        interval_msec animation update in milliseconds
        '''

        # Row count is provided by Y-axis limits
        nrows = len(ylims)

        # Bozo filters
        styles = self._bozo(nrows, styles, 'styles', 'b-')
        ylabels = self._bozo(nrows, ylabels, 'ylabels', '')

        # Set up subplots
        self.fig, axes = plt.subplots(nrows)
        if window_name:
            self.fig.canvas.set_window_title(window_name)

        # Set up handler for window-close events
        self.fig.canvas.mpl_connect('close_event', self._handle_close)
        self.is_open = True

        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, size)
        y = np.zeros(size)

        # Create lines
        self.lines = [ax.plot(self.x, y, style, animated=True)[0] for ax,style in zip(axes,styles)]

        # Add properties as specified
        [ax.set_ylabel(ylabel) for ax, ylabel in zip(axes, ylabels)]

        # Set axis limits
        [ax.set_xlim((0,size)) for ax in axes]
        [ax.set_ylim(ylim) for ax,ylim in zip(axes,ylims)]

        # Set X same for all lines
        [line.set_xdata(self.x) for line in self.lines]

        # XXX Hide X axis ticks and labels for now
        [ax.xaxis.set_visible(False) for ax in axes]

        # Allow interval specification
        self.interval_msec = interval_msec

    def start(self):
        '''
        Starts the realtime plotter.
        '''

        ani = animation.FuncAnimation(self.fig, self._animate, interval=self.interval_msec, blit=True)
        plt.show()

    def _animate(self, t):

        yvals = self.getYs()

        for row, line in enumerate(self.lines, start=1):
            ydata = line.get_ydata()
            ydata = np.roll(ydata, -1)
            ydata[-1] = yvals[row-1]
            line.set_ydata(ydata)
            
        return self.lines

# Simpe example with threading

class _SinePlotter(RealtimePlotter):

    def __init__(self):

        RealtimePlotter.__init__(self, [(-1,+1), (-1,+1)], window_name='Sinewave demo',
                styles = ['r-', 'b-'], ylabels=['Slow', 'Fast'])

        self.xcurr = 0

    def getYs(self):
        
        return self._getRow(1), self._getRow(2)

    def _getRow(self, row):

        size = len(self.x)
        
        return np.sin(row*2*np.pi*(float(self.xcurr)%size)/size)


def _update(plotter):

    from time import sleep

    while True:

        plotter.xcurr += 1
        sleep(.002)

if __name__ == '__main__':

    import threading

    plotter = _SinePlotter()

    thread = threading.Thread(target=_update, args = (plotter,))
    thread.daemon = True
    thread.start()

    plotter.start()
 
