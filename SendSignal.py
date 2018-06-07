from ctypes import windll
import time

class PortParallel(object):

    def __init__(self, address=0xcff8):
        self.port = windll.inpoutx64
        self.address = address

    def send_signal(self, trig):
        self.port.Out32(self.address, trig)
        time.sleep(0.03)
        self.port.Out32(self.address, 0)
