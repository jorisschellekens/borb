#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module defines an annotation used for profiling
"""
import cProfile
import io
import pstats
from pstats import SortKey  # type: ignore [attr-defined]


def profile(func):
    """
    This annotation wraps itself around a function, profiling it
    """

    def wrapper(*args, **kwargs):
        """
        This function starts the profiling, executes the function (storing the result), outputs the profiling information
        and returns the result
        """
        # setup profiler
        pr = cProfile.Profile()
        pr.enable()

        # execute function
        out_value = func(*args, **kwargs)

        # disable profiler
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        # return
        return out_value

    return wrapper
