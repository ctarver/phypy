# -*- coding: utf-8 -*-

"""Module for performing 'analog' related PHY tasks such as the power amplifier"""
import numpy as np
try:
    from .structures import MemoryPolynomial
except:
    from structures import MemoryPolynomial


class PowerAmp(MemoryPolynomial):
    """Power amplifier class that implements a baseband, memory-polynomial based PA """

    def __init__(self, order: int = 5, memory_depth: int = 4, memory_stride: int = 1,
                 noise_variance: float = 0.05, add_lo_leakage: bool = True,
                 add_iq_imbalance: bool = True, seed: int = 1):
        """Creates an instance of a parallel Hammerstein PA model extracted from a WARP PA board"""

        super().__init__(order, memory_depth, memory_stride)

        # Seed the random number generator for reproducibility
        np.random.seed(seed)

        if noise_variance < 0:
            raise Exception("The noisevarriance must be >=0")
        else:
            self.noise_variance = noise_variance

        if add_lo_leakage:
            self.lo_leakage = 0.01*np.random.randn() + 0.01j*np.random.randn()
        else:
            self.lo_leakage = 0

        if add_iq_imbalance:
            gm = 1.07
            pm = 5*np.pi/180
            k1 = 0.5*(1 + gm * np.exp(1j*pm))
            k2 = 0.5*(1 - gm * np.exp(1j*pm))
            sc_iq = 1/np.sqrt(np.abs(k1)**2 + np.abs(k2)**2)
            self.k1 = sc_iq*k1
            self.k2 = sc_iq*k2
        else:
            self.k1 = 1
            self.k2 = 0
        default_poly_coeffs = np.array([[0.9295 - 0.0001j, 0.2939 + 0.0005j, -0.1270 + 0.0034j, 0.0741 - 0.0018j],    # 1st order coeffs
                                        [0.1419 - 0.0008j, -0.0735 + 0.0833j, -0.0535 + 0.0004j, 0.0908 - 0.0473j],   # 3rd order
                                        [0.0084 - 0.0569j, -0.4610 + 0.0274j, -0.3011 - 0.1403j, -0.0623 - 0.0269j],  # 5th order
                                        [0.1774 + 0.0265j, 0.0848 + 0.0613j, -0.0362 - 0.0307j, 0.0415 + 0.0429j]],   # 7th order
                                       np.complex64)

        self.coeffs = default_poly_coeffs[:self.n_rows, :self.memory_depth]
        self.nmse_of_fit = None  # In case we fit the PA to some model

    def transmit(self, x):
        x = self.k1*x + self.k2*np.conj(x)
        return super().transmit(x) + self.noise_variance*np.random.rand(x.size)

    def make_new_model(self, pa_input, pa_output):
        """Learn new coefficients based on pa_inputs and pa_outputs"""
        self.coeffs = self.perform_least_squares(pa_input, pa_output).reshape(self.coeffs.shape)
        model_pa_output = self.transmit(pa_input)
        self.nmse_of_fit = self.calculate_nmse(pa_output, model_pa_output)

    @staticmethod
    def calculate_nmse(desired, actual):
        """Calculate the normalized mean squared error
        Todo:
            - Check this. I think I need to divide by number of samples
        """
        return np.linalg.norm(desired-actual)**2 / np.linalg.norm(desired)**2


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    pa = PowerAmp(order=7, noise_variance=0, add_iq_imbalance=False, add_lo_leakage=False, memory_stride=2)
    pa.coeffs = np.zeros(pa.coeffs.shape)
    pa.coeffs[(0, 0)] = 1
    x = np.exp(1j * (2 * np.pi * 1e6 * np.arange(100)/10e6))
    y = pa.transmit(x)
    pa.make_new_model(x, y)

    plt.plot(x.real)
    plt.plot(y.real)
    plt.show()
