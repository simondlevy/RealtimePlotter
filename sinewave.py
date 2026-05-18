#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from time import sleep

def threadfun():
    while True:
        sleep(0)


def animate(i, line, x):
    line.set_ydata(np.sin(x + i / 10.0))  

def main():

    fig, ax = plt.subplots()
    x = np.linspace(0, 2*np.pi, 1000)
    line, = ax.plot(x, np.sin(x))

    thread = Thread(target=threadfun)
    thread.daemon = True
    thread.start()

    line.set_ydata([np.nan] * len(x))

    ani = FuncAnimation(
            fig,
            animate,
            fargs=(line, x),
            interval=20,
            blit=True,
            cache_frame_data=False)

    plt.show()


main()



