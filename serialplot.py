#!/usr/bin/env python
'''
Real-time plot demo using serial input

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


from serial import Serial
from realtime_plot import RealtimePlotter
from time import sleep
from threading import Thread

# Change these to suit your needs
PORT = '/dev/ttyACM0'
BAUD = 115200
RANGE = (0,10000)

class SerialPlotter(RealtimePlotter):

    def __init__(self):

        RealtimePlotter.__init__(self, [RANGE], 
                window_name='Serial input',
                yticks = [RANGE],
                styles = ['b-'])

        self.xcurr = 0
        self.ycurr = 0

    def getValues(self):

         return (self.ycurr,)

def _update(plotter):

    port = Serial(PORT, BAUD)

    msg = ''

    while True:

        c = port.read()

        if c == '\n':
            try:
                plotter.ycurr = int(msg)
            except:
                pass
            msg = ''
        else:
            msg += c

        plotter.xcurr += 1

        sleep(.002)


if __name__ == '__main__':


    plotter = SerialPlotter()

    thread = Thread(target=_update, args = (plotter,))
    thread.daemon = True
    thread.start()

    plotter.start()
