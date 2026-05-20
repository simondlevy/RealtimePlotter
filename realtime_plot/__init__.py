'''
Real-time scrolling multi-plot over time.

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
from threading import Thread


class RealtimePlotter:
    '''
    Real-time scrolling multi-plot over time.  Your data-acquisition code
    should run on its own thread, to prevent blocking / slowdown.
    '''

    def __init__(self, source, ylims, size=100, show_yvals=False,
                 window_name='Realtime Plotter', styles=None, ylabels=None,
                 legend=None, yticks=[], interval_msec=20):
        '''
        Initializes a multi-plot with specified Y-axis limits as a list of
        pairs; e.g., [(-1,+1), (0.,5)].  Optional parameters are:

        size             size of display (X axis) in arbitrary time steps
        show_yvals       display Y values in plot if True
        window_name      name to display at the top of the figure
        styles           plot styles (e.g., 'b-', 'r.'; default='b-')
        legend           legend for each subplot (tuple or list)
        yticks           Y-axis tick / grid positions
        interval_msec    animation update in milliseconds

        For overlaying plots, use a tuple for styles; e.g.,
        styles=[('r','g'), 'b']
        '''

        self.source = source

        # Row count is provided by Y-axis limits
        nrows = len(ylims)

        # Signal (line) count is provided by styles
        nlines = nrows if styles is None else len(styles)

        # Create an empyt figure
        self.fig = plt.gcf()

        # X values are arbitrary ascending; Y is initially zero
        self.x = np.arange(0, size)
        y = np.zeros(size)

        # Set up subplots
        self.axes = [None]*nrows
        self.sideline = None
        for k in range(nrows):
            self.axes[k] = plt.subplot(nrows, 1, k+1)

        # Turn unspecified Y-axis labels into empty list
        ylabels = [] if ylabels is None else ylabels

        # Set window name
        self.fig.canvas.manager.set_window_title(window_name)

        # Create lines
        self.lines = [None] * nlines

        # Set line styles
        self.styles = styles

        # Set up legend
        self.legend = legend

        # Create baselines, initially hidden
        self.baselines = [axis.plot(self.x, y, 'k', animated=True)[0]
                          for axis in self.axes]
        self.baseflags = [False]*nrows

        # Add properties as specified
        [axis.set_ylabel(ylabel) for axis, ylabel in zip(self.axes, ylabels)]

        # Set axis limits
        [axis.set_xlim((0, size)) for axis in self.axes]
        [axis.set_ylim(ylim) for axis, ylim in zip(self.axes, ylims)]

        # Set ticks and gridlines
        [axis.yaxis.set_ticks(ytick) for axis, ytick in zip(self.axes, yticks)]
        [axis.yaxis.grid(True if yticks else False) for axis in self.axes]

        # Hide X axis ticks and labels for now
        [axis.xaxis.set_visible(False) for axis in self.axes]

        # Add axis text if indicated
        self.axis_texts = ([axis.text(0.8, ylim[1] - .1 * (ylim[1] - ylim[0]),
                                      '')
                           for axis, ylim in zip(self.axes, ylims)]
                           if show_yvals else [])

        # If we don't assign the result of the function, we won't see anything!
        self.ani = animation.FuncAnimation(
                self.fig, self._animate, interval=interval_msec, blit=True,
                cache_frame_data=False)

        # Set up handler for window-close events
        self.fig.canvas.mpl_connect('close_event', self._handle_close)

        self.running = True

    def start(self):
        '''
        Starts the realtime plotter.
        '''
        thread = Thread(target=self._threadfun)
        thread.daemon = True
        thread.start()

        plt.show()

    def _set_ydata(self, row, ydata):

        if self.lines[row] is None:
            k = row if len(self.axes) > 1 else 0
            self.lines[row], = self.axes[k].plot(
                    ydata, 'b' if self.styles is None else self.styles[row])

        self.lines[row].set_ydata(ydata)

        if self.legend is not None:
            plt.legend(self.legend, loc='upper right')

        texts = self.axis_texts
        if len(texts) > 0:
            texts[row].set_text('%+f' % ydata[-1])

    def _threadfun(self):

        while self.running:

            for row, vals in enumerate(self.source.read()):

                self._set_ydata(row, vals)

    def _handle_close(self, _):
        self.running = False

    def _animate(self, t):
        pass
