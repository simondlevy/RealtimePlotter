#!/usr/bin/python3
'''
Real-time plot demo using sine waves of two different frequencies.

Copyright (C) 2016 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

import numpy as np
from threading import Thread
from time import sleep

from realtime_plot import RealtimePlotter


def threadfun(plotter):

    i = 0

    x = np.linspace(0, 2*np.pi, 100)

    while True:

        plotter.set_ydata(0, np.sin(x + i/4))
        plotter.set_ydata(1, np.sin(x + i))
        i += 1
        sleep(0.1)


def main():

    plotter = RealtimePlotter(
            ((-1, +1), (-1, +1)),
            show_yvals=True,
            window_name='Sinewave demo',
            yticks=[(-1, 0, +1), (-1, 0, +1)],
            ylabels=['Slow', 'Fast'])

    thread = Thread(target=threadfun, args=(plotter, ))
    thread.daemon = True
    thread.start()

    plotter.start()


main()
