#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from time import sleep

def threadfun():

    while True:

        sleep(0)

def init():
    line.set_ydata([np.nan] * len(x))

def animate(i):
    line.set_ydata(np.sin(x + i / 10.0))  

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 1000)
line, = ax.plot(x, np.sin(x))

thread = Thread(target=threadfun)
thread.daemon = True
thread.start()

ani = FuncAnimation(fig, animate, init_func=init,
                    interval=20, blit=True, cache_frame_data=False)

plt.show()



