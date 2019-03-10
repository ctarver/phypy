"""Module for performing corrections on impairments related  to the PHY such as DPD"""
import numpy as np
try:
    from .structures import MemoryPolynomial
except:
    from structures import MemoryPolynomial


class ILA_DPD(MemoryPolynomial):
    """Implements a DPD object that uses an indirect learning architecture (ILA)

    Implements a digital predistorter (DPD) that uses an indirect learning architecture (ILA)
    and a parallel hammerstein, memory polynomial structure that acts as an inverse of the PA model.

    """
    def __init__(self, order: int = 5, memory_depth: int = 1, memory_stride: int = 5, n_iterations: int = 2):
        self.n_iterations = n_iterations

        super().__init__(order, memory_depth, memory_stride)

        # Make the 1st coeff 1 to have a completely linear DPD with 0 effect
        self.coeffs = np.zeros(shape=(self.n_rows, self.memory_depth))
        self.coeffs[0, 0] = 1

    def perform_learning(self, pa, signal):
        """Learn a new DPD model for a given pa"""
        for _ in range(self.n_iterations):
            # Forward through the predistorter
            pa_input = self.transmit(signal)

            # Transmit the predistorted signal through the actual PA
            pa_output = pa.transmit(pa_input)

            # Remove any PA Gain
            pa_output = pa_output*np.linalg.norm(pa_input)/np.linalg.norm(pa_output)

            # Learn on the postdistorter
            self.coeffs = self.perform_least_squares(pa_output, pa_input).reshape(self.coeffs.shape)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import modulators
    import analog

    dpd = ILA_DPD()

    ofdm = modulators.OFDM(n_subcarriers=600)
    x = ofdm.use(n_symbols=4)

    x = x*15

    pa = analog.PowerAmp(add_iq_imbalance=False, add_lo_leakage=False, noise_variance=0)
    pa.coeffs = np.zeros(shape=pa.coeffs.shape)
    pa.coeffs[0, 0] = 2
    pa.coeffs[1, 0] = 0.1
    pa.coeffs[2, 0] = -0.05
    y = pa.transmit(x)
    dpd.perform_learning(pa, x)
    pa_input_with_dpd = dpd.transmit(x)
    pa_output_with_dpd = pa.transmit(pa_input_with_dpd)

    # Analyze results.
    plt.psd(x, 1024, 10e6, label='original')
    plt.psd(y, 1024, 10e6, label='no dpd')
    plt.psd(pa_output_with_dpd, 1024, 10e6, label='with dpd')
    plt.gca().set_ylim(bottom=-120)
    plt.legend()
    plt.show()
