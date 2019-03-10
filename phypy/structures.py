""" File for mathematical structures like a memory polynomial"""

import numpy as np


class MemoryPolynomial:

    def __init__(self, order: int = 5, memory_depth: int = 4, memory_stride: int = 1):
        """Create an instance of a parallel Hammerstein, memory polynomial"""

        self.check_for_errors(order, memory_depth, memory_stride)

        # Save to object
        self.order = order
        self.memory_depth = memory_depth
        self.memory_stride = memory_stride
        self.coeffs = np.zeros((self.n_rows, self.memory_depth))

    def transmit(self, x):
        """Transmit a signal through the Memory Polynomial object"""

        X = self.setup_basis_matrix(x)
        coeffs = self.coeffs.flatten().copy()
        return np.dot(X, coeffs)

    def perform_least_squares(self, x, y):
        """Perform a least squares fit
        Todo:
            - Add support for regularized LS.
        """
        X = self.setup_basis_matrix(x)
        # lamb = 0.0001
        # coeffs, residuals, rank, s = np.linalg.lstsq(X.T.dot(X) + lamb * np.identity(self.n_coeffs),
        # X.T.dot(y), rcond=None)
        coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
        return coeffs

    def setup_basis_matrix(self, x):
        """Setup a matrix of the signal and delayed replicas for multiplication by the coeffs"""
        X = np.zeros((x.size, self.n_coeffs), dtype=np.complex64)
        column_index = 0
        for order in range(1, self.order + 1, 2):
            branch = np.multiply(x, np.power(np.abs(x), (order - 1)))
            for tap in range(0, self.memory_depth):
                delay = tap * self.memory_stride
                X[:, column_index] = np.resize(np.insert(branch, 0, np.zeros(delay)), branch.size)
                column_index += 1
        return X

    @staticmethod
    def check_for_errors(order, memory_depth, memory_stride):
        """Check for errors. Must be odd order with positive memory"""
        if order % 2 == 0 or order <= 0:
            raise Exception("PA Order must be positive and odd")

        if memory_depth <= 0:
            raise Exception("Memorydepth must be positive int")

        if memory_stride <= 0:
            raise Exception("Memory Stride must be a positive int")

    @property
    def n_coeffs(self):
        """"Total number of coefficients including the polynomial order and memory depth"""
        return self.memory_depth * self.n_rows

    @property
    def n_rows(self):
        """Total number of rows in the coeff matrix"""
        return np.floor_divide(self.order + 1, 2)
