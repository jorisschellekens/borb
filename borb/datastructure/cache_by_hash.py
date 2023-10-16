#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This decorator uses the hash of an object to cache methods.
The output of the method is stored in a private field of the object,
along with its hash, and the hash of the arguments passed to the method.
Thus, if the method is ever called again with the same arguments (equality by hash)
and on the same object (equality be hash), the cached value will be returned.
"""
import copy
import typing


def cached_by_hash(func):
    """
    This decorator uses the hash of an object to cache methods.
    The output of the method is stored in a private field of the object,
    along with its hash, and the hash of the arguments passed to the method.
    Thus, if the method is ever called again with the same arguments (equality by hash)
    and on the same object (equality be hash), the cached value will be returned.
    """

    def _inner(*args, **kwargs):
        # add attribute to store cached value
        field_name_for_cached_val: str = "_cache_for_" + func.__name__
        field_name_for_cache_hit_rate: str = "_cache_for_" + func.__name__ + "_hit_rate"
        if not hasattr(args[0], field_name_for_cached_val):
            setattr(args[0], field_name_for_cached_val, (None, None))
        if not hasattr(args[0].__class__, field_name_for_cache_hit_rate):
            setattr(args[0].__class__, field_name_for_cache_hit_rate, (0, 0))

        # compare keys
        key0: int = hash(tuple([hash(x) for x in args]))
        key_and_val: typing.Tuple[int, typing.Any] = getattr(
            args[0], field_name_for_cached_val
        )
        key1: int = key_and_val[0]
        val1: typing.Any = key_and_val[1]

        # return cached
        prev_hit_rate: typing.Tuple[int, int] = getattr(
            args[0].__class__, field_name_for_cache_hit_rate
        )
        if key0 == key1:
            setattr(
                args[0].__class__,
                field_name_for_cache_hit_rate,
                (prev_hit_rate[0] + 1, prev_hit_rate[1]),
            )
            return copy.deepcopy(val1)

        # set
        val0: typing.Any = func(*args, **kwargs)
        setattr(args[0], field_name_for_cached_val, (key0, val0))
        setattr(
            args[0].__class__,
            field_name_for_cache_hit_rate,
            (prev_hit_rate[0], prev_hit_rate[1] + 1),
        )

        # return
        return val0

    # return inner function
    return _inner
