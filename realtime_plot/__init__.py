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

    def _check_param(self, nrows, propvals, propname, dflt):
        retval = [dflt]*nrows
        if propvals:
            if len(propvals) != nrows:
                raise Exception('Provided %d ylims but %d %s' % (nrows, len(propvals), propname))
            else:
                retval = propvals
        return retval

    def _handle_close(self, event):

        self.is_open = False

    def __init__(self, ylims, size=100, phaselims=None,
            window_name=None, styles=None, ylabels=None, yticks=[], interval_msec=20):
        '''
        Initializes a multi-plot with specified Y-axis limits as a list of pairs; e.g., 
        [(-1,+1), (0.,5)].  Optional parameters are:
       
        size             size of display (X axis) in arbitrary time steps
        phaselims        xlim,ylim for phase plot
        window_name      name to display at the top of the figure
        styles           plot styles (e.g., 'b-', 'r.'; default='b-')
        yticks           Y-axis tick / grid positions
        interval_msec    animation update in milliseconds
        '''

        # Row count is provided by Y-axis limits
        nrows = len(ylims)

        # Bozo filters
        styles  = self._check_param(nrows, styles, 'styles', 'b-')
        ylabels = self._check_param(nrows, ylabels, 'ylabels', '')
        yticks  = self._check_param(nrows, yticks, 'yticks', [])

        self.fig = plt.gcf()

        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, size)
        y = np.zeros(size)

        # Set up subplots
        self.axes = [None]*nrows
        ncols = 2 if phaselims else 1
        self.sideline = None
        if phaselims:
            side = plt.subplot(1,2,1)
            side.set_aspect('equal')
            self.sideline = side.plot(y, y, 'o', animated=True)
            side.set_xlim(phaselims[0])
            side.set_ylim(phaselims[1])
        for k in range(nrows):
            self.axes[k] = plt.subplot(nrows, ncols, ncols*(k+1))
        if window_name:
            self.fig.canvas.set_window_title(window_name)

        # Set up handler for window-close events
        self.fig.canvas.mpl_connect('close_event', self._handle_close)
        self.is_open = True

        # Create lines
        self.lines = [ax.plot(self.x, y, style, animated=True)[0] for ax,style in zip(self.axes,styles)]

        # Create baselines, initially hidden
        self.baselines = [ax.plot(self.x, y, 'k', animated=True)[0] for ax in self.axes]
        self.baseflags = [False]*nrows

        # Add properties as specified
        [ax.set_ylabel(ylabel) for ax, ylabel in zip(self.axes, ylabels)]

        # Set axis limits
        [ax.set_xlim((0,size)) for ax in self.axes]
        [ax.set_ylim(ylim) for ax,ylim in zip(self.axes,ylims)]

        # Set ticks and gridlines
        [ax.yaxis.set_ticks(ytick) for ax,ytick in zip(self.axes,yticks)]
        [ax.yaxis.grid(True if yticks else False) for ax in self.axes]

        # XXX Hide X axis ticks and labels for now
        [ax.xaxis.set_visible(False) for ax in self.axes]

        # Allow interval specification
        self.interval_msec = interval_msec

    def start(self):
        '''
        Starts the realtime plotter.
        '''

        ani = animation.FuncAnimation(self.fig, self._animate, interval=self.interval_msec, blit=True)
        try:
            plt.show()
        except:
            pass
  
    def getValues(self):
        '''
        Override this method to return actual Y values at current time.
        '''

        return None

    def showBaseline(self, axid, value):
        '''
        Shows a baseline of specified value for specified row of this multi-plot.
        '''

        self._axis_check(axid)

        self.baselines[axid].set_ydata(value * np.ones(self.x.shape))
        self.baseflags[axid] = True

    def hideBaseline(self, axid):
        '''
        Hides the baseline for the specified row of this multi-plot.
        '''

        self._axis_check(axid)

        self.baseflags[axid] = False

    def _axis_check(self, axid):

        nrows = len(self.lines)

        if axid < 0 or axid >= nrows:

            raise Exception('Axis index must be in [0,%d)' % nrows)

    @classmethod
    def roll(cls, getter, setter, line, newval):
        data = getter(line)
        data = np.roll(data, -1)
        data[-1] = newval
        setter(data)

    @classmethod
    def rollx(cls, line, newval):
        RealtimePlotter.roll(line.get_xdata, line.set_xdata, line, newval)

    @classmethod
    def rolly(cls, line, newval):
        RealtimePlotter.roll(line.get_ydata, line.set_ydata, line, newval)

    def _animate(self, t):

        values = self.getValues()

        yvals = values[2:] if self.sideline else values

        for row, line in enumerate(self.lines, start=1):
            RealtimePlotter.rolly(line, yvals[row-1])

        if self.sideline:
            sideline = self.sideline[0]
            RealtimePlotter.rollx(sideline, values[0])
            RealtimePlotter.rolly(sideline, values[1])

        return (self.sideline if self.sideline != None else []) + \
                   self.lines + [baseline for baseline,flag in zip(self.baselines,self.baseflags) if flag]


# Simple example with threading

class _SinePlotter(RealtimePlotter):

    def __init__(self):

        RealtimePlotter.__init__(self, [(-1,+1), (-1,+1)], 
                window_name='Sinewave demo',
                yticks = [(-1,0,+1),(-1,0,+1)],
                styles = ['r--', 'b-'], 
                ylabels=['Slow', 'Fast'])

        self.xcurr = 0

    def getValues(self):

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
 
