import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
from time import sleep


class RealtimePlotter:

    def __init__(self, ylims):

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

    def _animate(self, i):
        pass


