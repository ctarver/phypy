"""DSP Module for basic DSP functions"""
import numpy as np


def frequency_shift(signal, shift_amount, sampling_rate):
    """Performs a shift in the freqeuency shift by multiplying by a complex sinusoid

    Args:
        signal: The signal to be shifted as a nparray
        shift_amount: Amount to shift by in Hz
        sampling_rate: The original sampling rate of the signal in Hz

    Returns:
        Returns a nparray with the signal shifted by the shift amount
    """
    return signal * np.exp(2*np.pi*1j*np.arange(signal.size)*shift_amount/sampling_rate)
