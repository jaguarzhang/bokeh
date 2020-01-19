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

# Module under test
import bokeh.plotting._stack as bps # isort:skip

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


def test__single_stack_raises_when_spec_in_kwargs():
    with pytest.raises(ValueError) as e:
        bps.single_stack(['a', 'b'], 'foo', foo=10)

    assert str(e.value).endswith("Stack property 'foo' cannot appear in keyword args")

def test__single_stack_raises_when_kwargs_list_lengths_differ():
    with pytest.raises(ValueError) as e:
        bps.single_stack(['a', 'b'], 'foo', baz=[1, 2], quux=[3,4,5])

    assert str(e.value).endswith("Keyword argument sequences for broadcasting must all be the same lengths. Got lengths: [2, 3]")

def test__single_stack_raises_when_kwargs_list_lengths_and_stackers_lengths_differ():
    with pytest.raises(ValueError) as e:
        bps.single_stack(['a', 'b', 'c'], 'foo',  baz=[1, 2], quux=[3,4])

    assert str(e.value).endswith("Keyword argument sequences for broadcasting must be the same length as stackers")

def test__single_stack_broadcast_with_no_kwargs():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.single_stack(stackers, 'start')
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i+1]

def test__single_stack_broadcast_with_scalar_kwargs():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.single_stack(stackers, 'start', foo=10, bar="baz")
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i+1]
        assert kw['foo'] == 10
        assert kw['bar'] == "baz"
        assert kw['name'] == stackers[i]

def test__single_stack_broadcast_with_list_kwargs():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.single_stack(stackers, 'start', foo=[10, 20, 30, 40], bar="baz")
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i+1]
        assert kw['foo'] == [10, 20, 30, 40][i]
        assert kw['bar'] == "baz"
        assert kw['name'] == stackers[i]

def test__single_stack_broadcast_name_scalar_overrides():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.single_stack(stackers, 'start', foo=[10, 20, 30, 40], bar="baz", name="name")
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i+1]
        assert kw['foo'] == [10, 20, 30, 40][i]
        assert kw['bar'] == "baz"
        assert kw['name'] == "name"

def test__single_stack_broadcast_name_list_overrides():
    names = ["aa", "bb", "cc", "dd"]
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.single_stack(stackers, 'start', foo=[10, 20, 30, 40], bar="baz", name=names)
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i+1]
        assert kw['foo'] == [10, 20, 30, 40][i]
        assert kw['bar'] == "baz"
        assert kw['name'] == names[i]

def test__double_stack_raises_when_spec_in_kwargs():
    with pytest.raises(ValueError) as e:
        bps.double_stack(['a', 'b'], 'foo', 'bar', foo=10)

    assert str(e.value).endswith("Stack property 'foo' cannot appear in keyword args")

    with pytest.raises(ValueError) as e:
        bps.double_stack(['a', 'b'], 'foo', 'bar', bar=10)

    assert str(e.value).endswith("Stack property 'bar' cannot appear in keyword args")

def test__double_stack_raises_when_kwargs_list_lengths_differ():
    with pytest.raises(ValueError) as e:
        bps.double_stack(['a', 'b'], 'foo', 'bar', baz=[1, 2], quux=[3,4,5])

    assert str(e.value).endswith("Keyword argument sequences for broadcasting must all be the same lengths. Got lengths: [2, 3]")

def test__double_stack_raises_when_kwargs_list_lengths_and_stackers_lengths_differ():
    with pytest.raises(ValueError) as e:
        bps.double_stack(['a', 'b', 'c'], 'foo', 'bar', baz=[1, 2], quux=[3,4])

    assert str(e.value).endswith("Keyword argument sequences for broadcasting must be the same length as stackers")

def test__double_stack_broadcast_with_no_kwargs():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.double_stack(stackers, 'start', 'end')
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'end', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i]
        assert list(kw['end']['expr'].fields) == stackers[:(i+1)]

def test__double_stack_broadcast_with_scalar_kwargs():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.double_stack(stackers, 'start', 'end', foo=10, bar="baz")
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'end', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i]
        assert list(kw['end']['expr'].fields) == stackers[:(i+1)]
        assert kw['foo'] == 10
        assert kw['bar'] == "baz"
        assert kw['name'] == stackers[i]

def test__double_stack_broadcast_with_list_kwargs():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.double_stack(stackers, 'start', 'end', foo=[10, 20, 30, 40], bar="baz")
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'end', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i]
        assert list(kw['end']['expr'].fields) == stackers[:(i+1)]
        assert kw['foo'] == [10, 20, 30, 40][i]
        assert kw['bar'] == "baz"
        assert kw['name'] == stackers[i]

def test__double_stack_broadcast_name_scalar_overrides():
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.double_stack(stackers, 'start', 'end', foo=[10, 20, 30, 40], bar="baz", name="name")
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'end', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i]
        assert list(kw['end']['expr'].fields) == stackers[:(i+1)]
        assert kw['foo'] == [10, 20, 30, 40][i]
        assert kw['bar'] == "baz"
        assert kw['name'] == "name"

def test__double_stack_broadcast_name_list_overrides():
    names = ["aa", "bb", "cc", "dd"]
    stackers = ['a', 'b', 'c', 'd']
    kws = bps.double_stack(stackers, 'start', 'end', foo=[10, 20, 30, 40], bar="baz", name=names)
    assert len(kws) == len(stackers)
    for i, kw in enumerate(kws):
        assert set(['start', 'end', 'foo', 'bar', 'name']) == set(kw.keys())
        assert list(kw['start']['expr'].fields) == stackers[:i]
        assert list(kw['end']['expr'].fields) == stackers[:(i+1)]
        assert kw['foo'] == [10, 20, 30, 40][i]
        assert kw['bar'] == "baz"
        assert kw['name'] == names[i]