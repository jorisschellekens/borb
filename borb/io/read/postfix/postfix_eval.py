# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The language that shall be used in a type 4 function contains expressions involving integers, real numbers, and
boolean values only. There shall be no composite data structures such as strings or arrays, no procedures, and
no variables or names. Table 42 lists the operators that can be used in this type of function. (For more
information on these operators, see Appendix B of the PostScript Language Reference, Third Edition.)
Although the semantics are those of the corresponding PostScript operators, a full PostScript interpreter is not
required.
"""
import typing
from decimal import Decimal
from math import atan, ceil, cos, degrees, exp, floor, log, sin, sqrt


class PostScriptEval:
    """
    The language that shall be used in a type 4 function contains expressions involving integers, real numbers, and
    boolean values only. There shall be no composite data structures such as strings or arrays, no procedures, and
    no variables or names. Table 42 lists the operators that can be used in this type of function. (For more
    information on these operators, see Appendix B of the PostScript Language Reference, Third Edition.)
    Although the semantics are those of the corresponding PostScript operators, a full PostScript interpreter is not
    required.
    """

    @staticmethod
    def evaluate(s: str, args: typing.List[Decimal]) -> typing.List[Decimal]:
        """
        This function evaluates a postscript str, using args as the (initial) stack.
        This function returns a typing.List[Decimal], or throws an assertion error
        """
        stk: typing.List[typing.Union[Decimal, bool]] = [x for x in args]
        ops: typing.List[str] = [
            "abs",
            "add",
            "and",
            "atan",
            "bitshift",  # TODO
            "ceiling",
            "copy",
            "cos",
            "cvi",
            "cvr",
            "div",
            "dup",
            "eq",
            "exch",
            "exp",
            "false",
            "floor",
            "ge",
            "gt",
            "idiv",
            "index",  # TODO
            "le",
            "ln",
            "log",
            "lt",
            "mod",
            "mul",
            "ne",
            "neg",
            "not",
            "or",
            "pop",
            "roll",  # TODO
            "round",
            "sin",
            "sqrt",
            "sub",
            "true",
            "truncate",  # TODO
            "xor",
        ]

        i: int = 0
        while i < len(s):

            # whitespace
            if s[i] in " \n\t":
                i += 1
                continue

            # brackets
            if s[i] == "{" or s[i] == "}":
                i += 1
                continue

            # operand
            if s[i] in "0123456789.-":
                operand: str = ""
                while i < len(s) and s[i] in "0123456789.-":
                    operand += s[i]
                    i += 1
                stk.append(Decimal(operand))
                continue

            # operator
            if any([x.startswith(s[i]) for x in ops]):
                operator: str = ""
                while i < len(s) and s[i] in "abcdefghijklmnopqrstuvwxyz":
                    operator += s[i]
                    i += 1
                if operator not in ops:
                    assert False, "Unknown operator %s in postscript str" % operator

                x: typing.Optional[typing.Union[Decimal, bool]] = None
                y: typing.Optional[typing.Union[Decimal, bool]] = None

                # abs
                if operator == "abs":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator abs, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(abs(x))
                    continue
                # add
                if operator == "add":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator add, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(x + y)
                    continue
                # and
                if operator == "and":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator and, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, bool)
                    assert isinstance(y, bool)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(x and y)
                    continue
                # atan
                if operator == "atan":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator atan, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(atan(x)))
                    continue
                # ceiling
                if operator == "ceiling":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator ceiling, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(ceil(x)))
                    continue
                # cos
                if operator == "cos":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator cos, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(cos(degrees(x))))
                    continue
                # cvi
                if operator == "cvi":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator cvi, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(int(x)))
                    continue
                # cvr
                if operator == "cvr":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator cvr, stack underflow"
                # div
                if operator == "div":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator div, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    assert x != Decimal(
                        0
                    ), "Unable to apply operator div, division by zero"
                    stk.append(y / x)
                    continue
                # dup
                if operator == "dup":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator dup, stack underflow"
                    stk.append(stk[-1])
                    continue
                # eq
                if operator == "eq":
                    assert len(stk) >= 2, "Unable to apply operator eq, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(x == y)
                    continue
                # exch
                if operator == "exch":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator exch, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(x)
                    stk.append(y)
                    continue
                # exp
                if operator == "exp":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator exp, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(exp(x)))
                    continue
                # false
                if operator == "false":
                    stk.append(False)
                    continue
                # floor
                if operator == "floor":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator floor, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(floor(x)))
                    continue
                # ge
                if operator == "ge":
                    assert len(stk) >= 2, "Unable to apply operator ge, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y >= x)
                    continue
                # gt
                if operator == "gt":
                    assert len(stk) >= 2, "Unable to apply operator gt, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y > x)
                    continue
                # idiv
                if operator == "idiv":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator idiv, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    assert x != Decimal(
                        0
                    ), "Unable to apply operator idiv, division by zero"
                    stk.append(Decimal(int(y / x)))
                    continue
                # le
                if operator == "le":
                    assert len(stk) >= 2, "Unable to apply operator le, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y <= x)
                    continue
                # ln
                if operator == "ln":
                    assert len(stk) >= 1, "Unable to apply operator ln, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(log(x)))
                    continue
                # log
                if operator == "log":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator log, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(log(x, Decimal(10))))
                    continue
                # lt
                if operator == "lt":
                    assert len(stk) >= 2, "Unable to apply operator lt, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y < x)
                    continue
                # mod
                if operator == "mod":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator mod, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    assert y != Decimal(
                        0
                    ), "Unable to apply operator mod, division by zero"
                    stk.append(Decimal(int(y) % int(x)))
                    continue
                # mul
                if operator == "mul":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator mul, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y * x)
                    continue
                # ne
                if operator == "ne":
                    assert len(stk) >= 2, "Unable to apply operator ne, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y != x)
                    continue
                # neg
                if operator == "neg":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator neg, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(-x)
                    continue
                # not
                if operator == "not":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator not, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, bool)
                    stk.pop(len(stk) - 1)
                    stk.append(not x)
                    continue
                # or
                if operator == "or":
                    assert len(stk) >= 2, "Unable to apply operator or, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, bool)
                    assert isinstance(y, bool)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y or x)
                    continue
                # pop
                if operator == "pop":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator pop, stack underflow"
                    stk.pop(-1)
                    continue
                # round
                if operator == "round":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator round, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(round(x)))
                    continue
                # sin
                if operator == "sin":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator sin, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(sin(degrees(x))))
                    continue
                # sqrt
                if operator == "sqrt":
                    assert (
                        len(stk) >= 1
                    ), "Unable to apply operator sqrt, stack underflow"
                    x = stk[-1]
                    assert isinstance(x, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(sqrt(x)))
                    continue
                # sub
                if operator == "sub":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator sub, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, Decimal)
                    assert isinstance(y, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(y - x)
                    continue
                # true
                if operator == "true":
                    stk.append(True)
                    continue
                # xor
                if operator == "xor":
                    assert (
                        len(stk) >= 2
                    ), "Unable to apply operator xor, stack underflow"
                    x = stk[-1]
                    y = stk[-2]
                    assert isinstance(x, bool)
                    assert isinstance(y, bool)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(x or y and not (x and y))
                    continue

            # unknown, advance by 1
            i += 1

        # check type(s)
        out: typing.List[Decimal] = []
        for x in stk:
            assert isinstance(x, Decimal)
            out.append(x)

        # return
        return out
