#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `phypy` package."""

import pytest
import numpy as np
from phypy import analog
from phypy import modulators as mods
from phypy import dsp

def test_pa_setup():
    pa = analog.PowerAmp(order=5, memory_depth=2, noise_variance=0.01, add_lo_leakage=False, add_iq_imbalance=False)
    assert pa.order == 5
    assert pa.memory_depth == 2
    assert pa.noise_variance == 0.01
    assert pa.lo_leakage == 0
    assert pa.k1 == 1
    assert pa.k2 == 0


def test_pa_transmission_with_unit_coeff():
    """Test that the pa output is equal to the pa input if there is only a 1 in the 1st order term"""
    pa = analog.PowerAmp(order=7, noise_variance=0, add_iq_imbalance=False, add_lo_leakage=False)
    pa.coeffs = np.zeros(pa.coeffs.shape)
    pa.coeffs[(0, 0)] = 1
    x = np.exp(1j * (2 * np.pi * 1e6 * np.arange(100)/10e6))
    assert sum(np.abs(pa.transmit(x) - x)) <= 1e-5


def test_ofdm_setup_lte_20mhz():
    """Test the default setup of the OFDM class"""
    ofdm = mods.OFDM()
    assert ofdm.n_subcarriers == 1200
    assert ofdm.subcarrier_spacing == 15000  # 15 kHz
    assert ofdm.cp_length == 144  # Normal cyclic prefix
    assert ofdm.fft_size == 2048
    assert ofdm.sampling_rate == 30.72e6  # 30.72 MHz
    assert (ofdm.symbol_alphabet == np.array([-1+1j, -1-1j, 1+1j, 1-1j])).all()


def test_ofdm_setup_lte_5mhz():
    """Test the default setup of the OFDM class"""
    ofdm = mods.OFDM(n_subcarriers=300)
    assert ofdm.n_subcarriers == 300
    assert ofdm.subcarrier_spacing == 15000  # 15 kHz
    assert ofdm.cp_length == 144  # Normal cyclic prefix
    assert ofdm.fft_size == 512
    assert ofdm.sampling_rate == 7.68e6  # MHz
    assert (ofdm.symbol_alphabet == np.array([-1+1j, -1-1j, 1+1j, 1-1j])).all()


def test_freq_shift():
    """ Test the frequency shift. A 1 MHz signal shifted by 1 MHz should be a 2 MHz signal"""
    sampling_rate = 20e6  # 20 MHz
    sin_freq = 1e6  # 1 MHz sinusoid
    seconds = 0.00001  # 0.01 ms of data

    sampling_period = 1/sampling_rate
    t_array = np.arange(start=0, stop=seconds, step=sampling_period)
    samples = np.exp(2*np.pi*1j*sin_freq*t_array)
    y = dsp.frequency_shift(samples, shift_amount=1e6, sampling_rate=sampling_rate)
    two_mhz_sin = np.exp(2*np.pi*1j*(2*sin_freq)*t_array)
    error = np.square(np.abs(two_mhz_sin - y)).mean()
    assert error < 1e-20
