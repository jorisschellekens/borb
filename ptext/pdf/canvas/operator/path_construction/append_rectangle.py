#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Append a rectangle to the current path as a complete
subpath, with lower-left corner (x, y) and dimensions width
and height in user space. The operation
x y width height re
is equivalent to
x y m
( x + width ) y l
( x + width ) ( y + height ) l
x ( y + height ) l
h
"""
