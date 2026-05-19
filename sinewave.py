#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from time import sleep


def threadfun(line):

    i = 0

    x = np.linspace(0, 2*np.pi, 1000)

    while True:

        data = np.sin(x + i / 10.0)
 
        line.set_ydata(data)

        i += 1

        sleep(0.02)


def animate(i):
    pass


def main():

    fig, ax = plt.subplots()
    x = np.linspace(0, 2*np.pi, 1000)
    line, = ax.plot(x, np.sin(x))

    line.set_ydata([np.nan] * len(x))

    ani = FuncAnimation(
            fig,
            animate,
            interval=20,
            blit=True,
            cache_frame_data=False)

    thread = Thread(target=threadfun, args=(line,))
    thread.daemon = True
    thread.start()

    plt.show()


main()



