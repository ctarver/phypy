# -*- coding: utf-8 -*-

"""Module for power amplifier related tools"""


class PowerAmp:
    """Power amplifier class that implements a memoryless, polynomial-based PA """

    def __init__(self, order=5):
        if order % 2 == 0:
            raise PAError("PA Order must be odd")
        else:
            self.order = order

    def create_coeffs(self):
        pass


class PAError(Exception):
    pass


if __name__ == "__main__":
    pa = PowerAmp(order=6)
