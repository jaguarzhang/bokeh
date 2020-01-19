#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import pytest ; pytest

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import datetime

# External imports
import numpy as np

# Bokeh imports
from bokeh.models import (
    CategoricalAxis,
    CategoricalScale,
    DataRange1d,
    DatetimeAxis,
    FactorRange,
    LinearAxis,
    LinearScale,
    LogAxis,
    LogScale,
    MercatorAxis,
    Range1d,
)

# Module under test
import bokeh.plotting._plot as bpp # isort:skip

#-----------------------------------------------------------------------------
# Setup
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------


_RANGES = [Range1d(), DataRange1d(), FactorRange()]

class Test__get_axis_class(object):

    @pytest.mark.parametrize('range', _RANGES)
    @pytest.mark.unit
    def test_axis_type_None(self, range):
        assert(bpp._get_axis_class(None, range, 0)) == (None, {})
        assert(bpp._get_axis_class(None, range, 1)) == (None, {})

    @pytest.mark.parametrize('range', _RANGES)
    @pytest.mark.unit
    def test_axis_type_linear(self, range):
        assert(bpp._get_axis_class("linear", range, 0)) == (LinearAxis, {})
        assert(bpp._get_axis_class("linear", range, 1)) == (LinearAxis, {})

    @pytest.mark.parametrize('range', _RANGES)
    @pytest.mark.unit
    def test_axis_type_log(self, range):
        assert(bpp._get_axis_class("log", range, 0)) == (LogAxis, {})
        assert(bpp._get_axis_class("log", range, 1)) == (LogAxis, {})

    @pytest.mark.parametrize('range', _RANGES)
    @pytest.mark.unit
    def test_axis_type_datetime(self, range):
        assert(bpp._get_axis_class("datetime", range, 0)) == (DatetimeAxis, {})
        assert(bpp._get_axis_class("datetime", range, 1)) == (DatetimeAxis, {})

    @pytest.mark.parametrize('range', _RANGES)
    @pytest.mark.unit
    def test_axis_type_mercator(self, range):
        assert(bpp._get_axis_class("mercator", range, 0)) == (MercatorAxis, {'dimension': 'lon'})
        assert(bpp._get_axis_class("mercator", range, 1)) == (MercatorAxis, {'dimension': 'lat'})

    def test_axis_type_auto(self):
        assert(bpp._get_axis_class("auto", FactorRange(), 0)) == (CategoricalAxis, {})
        assert(bpp._get_axis_class("auto", FactorRange(), 1)) == (CategoricalAxis, {})
        assert(bpp._get_axis_class("auto", DataRange1d(), 0)) == (LinearAxis, {})
        assert(bpp._get_axis_class("auto", DataRange1d(), 1)) == (LinearAxis, {})
        assert(bpp._get_axis_class("auto", Range1d(), 0)) == (LinearAxis, {})
        assert(bpp._get_axis_class("auto", Range1d(), 1)) == (LinearAxis, {})
        assert(bpp._get_axis_class("auto", Range1d(start=datetime.datetime(2018, 3, 21)), 0)) == (DatetimeAxis, {})
        assert(bpp._get_axis_class("auto", Range1d(start=datetime.datetime(2018, 3, 21)), 1)) == (DatetimeAxis, {})


    @pytest.mark.parametrize('range', _RANGES)
    @pytest.mark.unit
    def test_axis_type_error(self, range):
        with pytest.raises(ValueError):
            bpp._get_axis_class("junk", range, 0)
        with pytest.raises(ValueError):
            bpp._get_axis_class("junk", range, 1)

def test_get_scale_numeric_range_linear_axis():
    s = bpp.get_scale(Range1d(), "linear")
    assert isinstance(s, LinearScale)

    s = bpp.get_scale(Range1d(), "datetime")
    assert isinstance(s, LinearScale)

    s = bpp.get_scale(Range1d(), "auto")
    assert isinstance(s, LinearScale)

def test_get_scale_numeric_range_log_axis():
    s = bpp.get_scale(DataRange1d(), "log")
    assert isinstance(s, LogScale)

def test_get_scale_factor_range():
    s = bpp.get_scale(FactorRange(), "auto")
    assert isinstance(s, CategoricalScale)

def test_get_range_with_None():
    r = bpp.get_range(None)
    assert isinstance(r, DataRange1d)

def test_get_range_with_Range():
    for t in [Range1d, DataRange1d, FactorRange]:
        rng = t()
        r = bpp.get_range(rng)
        assert r is rng

def test_get_range_with_ndarray():
    r = bpp.get_range(np.array([10, 20]))
    assert isinstance(r, Range1d)
    assert r.start == 10
    assert r.end == 20

def test_get_range_with_too_long_ndarray():
    with pytest.raises(ValueError):
        bpp.get_range(np.array([10, 20, 30]))

def test_get_range_with_ndarray_factors():
    f = np.array(["Crosby", "Stills", "Nash", "Young"])
    r = bpp.get_range(f)
    assert isinstance(r, FactorRange)
    assert r.factors == list(f)

def test_get_range_with_series(pd):
    r = bpp.get_range(pd.Series([20, 30]))
    assert isinstance(r, Range1d)
    assert r.start == 20
    assert r.end == 30

def test_get_range_with_too_long_series(pd):
    with pytest.raises(ValueError):
        bpp.get_range(pd.Series([20, 30, 40]))

def test_get_range_with_string_seq():
    f = ["foo" ,"end", "baz"]
    for t in [list, tuple]:
        r = bpp.get_range(t(f))
        assert isinstance(r, FactorRange)
        # FactorRange accepts Seq, but get_range always sets a list copy
        assert r.factors == f

def test_get_range_with_float_bounds():
    r = bpp.get_range((1.2, 10))
    assert isinstance(r, Range1d)
    assert r.start == 1.2
    assert r.end == 10

    r = bpp.get_range([1.2, 10])
    assert isinstance(r, Range1d)
    assert r.start == 1.2
    assert r.end == 10

def testget_range_with_pandas_group(pd):
    from bokeh.sampledata.iris import flowers
    g = flowers.groupby('species')
    r = bpp.get_range(g)
    assert isinstance(r, FactorRange)
    assert r.factors == ['setosa', 'versicolor', 'virginica'] # should always be sorted

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------