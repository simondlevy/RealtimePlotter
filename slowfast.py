#!/usr/bin/python3

import numpy as np
from threading import Thread
from time import sleep

# from new_realtime_plot import RealtimePlotter
from realtime_plot import RealtimePlotter


def threadfun(plotter):

    i = 0

    x = np.linspace(0, 2*np.pi, 1000)

    while True:

        plotter.set_ydata(0, np.sin(x + i))

        plotter.set_ydata(1, np.sin(x + i/100))

        i += 1

        sleep(0.02)


def main():

    plotter = RealtimePlotter(((-1,+1), (-1,+1)),
                show_yvals=True,
                window_name='Sinewave demo',
                yticks = [(-1,0,+1),(-1,0,+1)],
                ylabels=['Slow', 'Fast'])


    thread = Thread(target=threadfun, args=(plotter, ))
    thread.daemon = True
    thread.start()

    plotter.start()


main()



