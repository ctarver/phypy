#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `phypy` package."""

import pytest
from phypy import analog


def test_pa_error():
    with pytest.raises(analog.PAError):
        analog.PowerAmp(order=4)


def test_pa_setup():
    pa = analog.PowerAmp(order=5)
    assert pa.order == 5
