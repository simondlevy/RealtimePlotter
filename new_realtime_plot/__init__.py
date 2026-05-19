import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from time import sleep


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


        fig, ax = plt.subplots()
        x = np.linspace(0, 2*np.pi, 1000)
        self.line, = ax.plot(x, np.sin(x))

        self.line.set_ydata([np.nan] * len(x))

        self.ani = FuncAnimation(
                fig,
                self._animate,
                interval=20,
                blit=True,
                cache_frame_data=False)


    def start(self):
        plt.show()

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


