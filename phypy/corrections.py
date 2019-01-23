"""Module for performing corrections on impairments related  to the PHY such as DPD"""
import numpy as np
import analog


class ILA_DPD(analog.PowerAmp):
    def __init__(self, order: int = 5, memory_depth: int = 1):
        super().__init__(order, memory_depth, add_iq_imbalance=False, add_lo_leakage=False, noise_variance=0)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    dpd = ILA_DPD()
    x = np.exp(1j * (2 * np.pi * 1e6 * np.arange(100)/10e6))
    y = pa.transmit(x)
    plt.plot(x.real)
    plt.plot(y.real)
    plt.show()
