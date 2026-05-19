#!/usr/bin/python3

import numpy as np
from threading import Thread
from time import sleep

from new_realtime_plot import RealtimePlotter


def threadfun(plotter):

    i = 0

    x = np.linspace(0, 2*np.pi, 1000)

    while True:

        data = np.sin(x + i / 10.0)
 
        plotter.set_ydata(data)

        i += 1

        sleep(0.02)


def animate(i):
    pass


def main():

    plotter = RealtimePlotter( ((-1,+1),) )

    thread = Thread(target=threadfun, args=(plotter, ))
    thread.daemon = True
    thread.start()

    plotter.start()


main()



