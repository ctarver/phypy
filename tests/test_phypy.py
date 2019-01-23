#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `phypy` package."""

import pytest
from phypy import analog


def test_even_pa_order():
    with pytest.raises(analog.PAError):
        analog.PowerAmp(order=4)


def test_negative_pa_order():
    with pytest.raises(analog.PAError):
        analog.PowerAmp(order=-4)


def test_pa_setup():
    pa = analog.PowerAmp(order=5, memory_depth=2, noise_variance=0.01, add_lo_leakage=False, add_iq_imbalance=False)
    assert pa.order == 5
    assert pa.memory_depth == 2
    assert pa.noise_variance == 0.01
    assert pa.lo_leakage == 0
    assert pa.k1 == 1
    assert pa.k2 == 0
