'''
Real-time scrolling multi-plot.

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
from matplotlib.animation import FuncAnimation


class RealtimePlotter:

    def __init__(self, ylims,  size=100, phaselims=None, show_yvals=False,
                 window_name=None, styles=None, ylabels=None, yticks=[],
                 legends=[], interval_msec=20):
        '''
        Initializes a multi-plot with specified Y-axis limits as a list of
        pairs; e.g., [(-1,+1), (0.,5)].  Optional parameters are:

        size             size of display (X axis) in arbitrary time steps
        phaselims        xlim,ylim for phase plot
        show_yvals       display Y values in plot if True
        window_name      name to display at the top of the figure
        styles           plot styles (e.g., 'b-', 'r.'; default='b-')
        yticks           Y-axis tick / grid positions
        legends          list of legends for each subplot
        interval_msec    animation update in milliseconds

        For overlaying plots, use a tuple for styles; e.g.,
        styles=[('r','g'), 'b']
        '''

        # Row count is provided by Y-axis limits
        nrows = len(ylims)

        # Bozo filters
        styles = self._check_param(nrows, styles, 'styles', 'b-')
        ylabels = self._check_param(nrows, ylabels, 'ylabels', '')
        yticks = self._check_param(nrows, yticks, 'yticks', [])
        self.legends = self._check_param(nrows, legends, 'legends', [])

        self.fig, self.axes = plt.subplots(nrows)

        self.lines = [None] * nrows

        self.ani = FuncAnimation(
                self.fig,
                self._animate,
                interval=20,
                blit=True,
                cache_frame_data=False)


    def start(self):
        plt.show()

    def set_ydata(self, row, ydata):

        if self.lines[row] is None:
            self.lines[row], = self.axes[row].plot(ydata)

        self.lines[row].set_ydata(ydata)

    def _check_param(self, nrows, propvals, propname, dflt):
        retval = [dflt]*nrows
        if propvals:
            if len(propvals) != nrows:
                raise Exception('Provided %d ylims but %d %s' %
                                (nrows, len(propvals), propname))
            else:
                retval = propvals
        return retval

    def _animate(self, i):
        pass


