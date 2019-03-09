# -*- coding: utf-8 -*-

"""Module for performing 'analog' related PHY tasks such as the power amplifier"""
import numpy as np


class PowerAmp:
    """Power amplifier class that implements a baseband, memory-polynomial based PA """

    def __init__(self, order: int = 5, memory_depth: int = 4, noise_variance: float = 0.05,
                 add_lo_leakage: bool = True, add_iq_imbalance: bool = True, seed: int = 1):
        """Creates an instance of a parallel Hammerstein PA model extracted from a WARP PA board"""

        # Seed the random number generator for reproducibility
        np.random.seed(seed)

        # Check for errors and add to instance
        if order % 2 == 0 or order <= 0:
            raise PAError("PA Order must be positive and odd")
        else:
            self.order = order

        if memory_depth <= 0:
            raise PAError("Memorydepth must be positive int")
        else:
            self.memory_depth = memory_depth

        if noise_variance < 0:
            raise PAError("The noisevarriance must be >=0")
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
        n_rows = np.floor_divide(self.order + 1, 2)
        self.coeffs = default_poly_coeffs[:n_rows, :self.memory_depth]

    def transmit(self, x):
        """Transmit a signal through the PA object"""
        x = self.k1*x + self.k2*np.conj(x)
        X = self.setup_basis_matrix(x)
        coeffs = self.coeffs.flatten().copy()
        return np.dot(X, coeffs) + self.noise_variance*np.random.rand(x.size)

    def setup_basis_matrix(self, x):
        """Setup a matrix of the signal and delayed replicas for multiplication by the coeffs"""
        X = np.zeros((x.size, self.n_coeffs), dtype=np.complex64)
        column_index = 0
        for order in range(1, self.order + 1, 2):
            branch = np.multiply(x, np.power(np.abs(x), (order-1)))
            for delay in range(0, self.memory_depth):
                X[:, column_index] = np.resize(np.insert(branch, 0, np.zeros(delay)), branch.size)
                column_index += 1
        return X

    def make_new_model(self, pa_input, pa_output):
        """Learn new coefficients based on pa_inputs and pa_outputs"""
        self.coeffs = self.perform_least_squares(pa_input, pa_output).reshape(self.coeffs.shape)
        model_pa_output = self.transmit(pa_input)
        self.nmse_of_fit = self.calculate_nmse(pa_output, model_pa_output)

    def perform_least_squares(self, x, y):
        """Perform a least squares fit
        Todo:
            - Add support for regularized LS.
        """
        X = self.setup_basis_matrix(x)
        #lamb = 0.0001
        #coeffs, residuals, rank, s = np.linalg.lstsq(X.T.dot(X) + lamb * np.identity(self.n_coeffs),
        # X.T.dot(y), rcond=None)
        coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
        return coeffs

    @staticmethod
    def calculate_nmse(desired, actual):
        """Calculate the normalized mean squared error
        Todo:
            - Check this. I think I need to divide by number of samples
        """
        return np.linalg.norm(desired-actual)**2 / np.linalg.norm(desired)**2

    @property
    def n_coeffs(self):
        """"Total number of coefficients including the polynomial order and memory depth"""
        return np.floor_divide(self.memory_depth * (self.order + 1), 2)


class PAError(Exception):
    """Exceptions for Errors related to the Power Amplifier Construction and use"""
    pass


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    pa = PowerAmp(order=7, noise_variance=0, add_iq_imbalance=False, add_lo_leakage=False)
    pa.coeffs = np.zeros(pa.coeffs.shape)
    pa.coeffs[(0, 0)] = 1
    x = np.exp(1j * (2 * np.pi * 1e6 * np.arange(100)/10e6))
    y = pa.transmit(x)
    pa.make_new_model(x, y)

    plt.plot(x.real)
    plt.plot(y.real)
    plt.show()
