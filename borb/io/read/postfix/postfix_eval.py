#!/usr/bin/env python
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
import math


class PostScriptEval:
    """
    The language that shall be used in a type 4 function contains expressions involving integers, real numbers, and
    boolean values only. There shall be no composite data structures such as strings or arrays, no procedures, and
    no variables or names. Table 42 lists the operators that can be used in this type of function. (For more
    information on these operators, see Appendix B of the PostScript Language Reference, Third Edition.)
    Although the semantics are those of the corresponding PostScript operators, a full PostScript interpreter is not
    required.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def evaluate(s: str, args: typing.List[Decimal] = []) -> typing.List[Decimal]:
        """
        This function evaluates a postscript str, using args as the (initial) stack.
        This function returns a typing.List[Decimal], or throws an assertion error
        :param s:       the (postfix) str to evaluate
        :param args:    the (initial) stack
        :return:        the resulting stack
        """
        stk: typing.List[typing.Union[Decimal, bool]] = []
        stk += args
        known_operators: typing.List[str] = [
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
            if any([x.startswith(s[i]) for x in known_operators]):
                operator: str = ""
                while i < len(s) and s[i] in "abcdefghijklmnopqrstuvwxyz":
                    operator += s[i]
                    i += 1
                if operator not in known_operators:
                    assert False, "Unknown operator %s in postscript str" % operator

                # abs
                arg0: typing.Optional[typing.Union[Decimal, bool]] = None
                arg1: typing.Optional[typing.Union[Decimal, bool]] = None
                if operator == "abs":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator abs, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator abs, arg 1 must be of type Decimal"
                    # fmt: on
                    arg0 = stk[-1]
                    stk.pop(len(stk) - 1)
                    stk.append(abs(arg0))
                    continue
                # add
                if operator == "add":
                    # fmt: off
                    assert (len(stk) >= 2), "Unable to apply operator add, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator add, arg 1 must be of type Decimal"
                    assert isinstance(stk[-2], Decimal), "Unable to apply operator add, arg 2 must be of type Decimal"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg0 + arg1)
                    continue
                # and
                if operator == "and":
                    # fmt: off
                    assert (len(stk) >= 2), "Unable to apply operator and, stack underflow"
                    assert isinstance(stk[-1], bool), "Unable to apply operator and, arg 1 must be of type bool"
                    assert isinstance(stk[-2], bool), "Unable to apply operator and, arg 2 must be of type bool"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg0 and arg1)
                    continue
                # atan
                if operator == "atan":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator atan, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator atan, arg 1 must be of type Decimal"
                    # fmt: on
                    arg0 = stk[-1]
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.atan(arg0)))
                    continue
                # ceiling
                if operator == "ceiling":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator ceiling, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator ceiling, arg 1 must be of type Decimal"
                    # fmt: on
                    arg0 = stk[-1]
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.ceil(arg0)))
                    continue
                # cos
                if operator == "cos":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator cos, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator cos, arg 1 must be of type Decimal"
                    # fmt: on
                    arg0 = stk[-1]
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.cos(math.degrees(arg0))))
                    continue
                # cvi
                if operator == "cvi":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator cvi, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator cvi, arg 1 must be of type Decimal"
                    # fmt: on
                    arg0 = stk[-1]
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(int(arg0)))
                    continue
                # cvr
                if operator == "cvr":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator cvr, stack underflow"
                    # fmt: on
                # div
                if operator == "div":
                    # fmt: off
                    assert (len(stk) >= 2), "Unable to apply operator div, stack underflow"
                    assert isinstance(stk[-1], Decimal), "Unable to apply operator div, arg 1 must be of type Decimal"
                    assert isinstance(stk[-2], Decimal), "Unable to apply operator div, arg 2 must be of type Decimal"
                    assert stk[-1] != Decimal(0), "Unable to apply operator div, arg1 must not be 0"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 / arg0)
                    continue
                # dup
                if operator == "dup":
                    # fmt: off
                    assert (len(stk) >= 1), "Unable to apply operator dup, stack underflow"
                    # fmt: on
                    stk.append(stk[-1])
                    continue
                # eq
                if operator == "eq":
                    assert len(stk) >= 2, "Unable to apply operator eq, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg0 == arg1)
                    continue
                # exch
                if operator == "exch":
                    # fmt: off
                    assert (len(stk) >= 2), "Unable to apply operator exch, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg0)
                    stk.append(arg1)
                    continue
                # exp
                if operator == "exp":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator exp, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(
                        arg0, Decimal
                    ), "Unable to apply operator exp, unexpected type"
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.exp(arg0)))
                    continue
                # false
                if operator == "false":
                    stk.append(False)
                    continue
                # floor
                if operator == "floor":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator floor, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(
                        arg0, Decimal
                    ), "Unable to apply operator floor, unexpected type"
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.floor(arg0)))
                    continue
                # ge
                if operator == "ge":
                    assert len(stk) >= 2, "Unable to apply operator ge, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(
                        arg0, Decimal
                    ), "Unable to apply operator ge, unexpected type"
                    assert isinstance(
                        arg1, Decimal
                    ), "Unable to apply operator ge, unexpected type"
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 >= arg0)
                    continue
                # gt
                if operator == "gt":
                    assert len(stk) >= 2, "Unable to apply operator gt, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 > arg0)
                    continue
                # idiv
                if operator == "idiv":
                    # fmt: off
                    assert len(stk) >= 2, "Unable to apply operator idiv, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    # fmt: off
                    assert arg0 != Decimal(0), "Unable to apply operator idiv, division by zero"
                    # fmt: on
                    stk.append(Decimal(int(arg1 / arg0)))
                    continue
                # le
                if operator == "le":
                    assert len(stk) >= 2, "Unable to apply operator le, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 <= arg0)
                    continue
                # ln
                if operator == "ln":
                    assert len(stk) >= 1, "Unable to apply operator ln, stack underflow"
                    arg0 = stk[-1]
                    assert isinstance(arg0, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.log(arg0)))
                    continue
                # log
                if operator == "log":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator log, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(arg0, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.log(arg0, Decimal(10))))
                    continue
                # lt
                if operator == "lt":
                    assert len(stk) >= 2, "Unable to apply operator lt, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 < arg0)
                    continue
                # mod
                if operator == "mod":
                    # fmt: off
                    assert len(stk) >= 2, "Unable to apply operator mod, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    # fmt: off
                    assert arg1 != Decimal(0), "Unable to apply operator mod, division by zero"
                    # fmt: on
                    stk.append(Decimal(int(arg1) % int(arg0)))
                    continue
                # mul
                if operator == "mul":
                    # fmt: off
                    assert len(stk) >= 2, "Unable to apply operator mul, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 * arg0)
                    continue
                # ne
                if operator == "ne":
                    assert len(stk) >= 2, "Unable to apply operator ne, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 != arg0)
                    continue
                # neg
                if operator == "neg":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator neg, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(arg0, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(-arg0)
                    continue
                # not
                if operator == "not":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator not, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(arg0, bool)
                    stk.pop(len(stk) - 1)
                    stk.append(not arg0)
                    continue
                # or
                if operator == "or":
                    assert len(stk) >= 2, "Unable to apply operator or, stack underflow"
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, bool)
                    assert isinstance(arg1, bool)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 or arg0)
                    continue
                # pop
                if operator == "pop":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator pop, stack underflow"
                    # fmt: on
                    stk.pop(-1)
                    continue
                # round
                if operator == "round":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator round, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(arg0, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(round(arg0)))
                    continue
                # sin
                if operator == "sin":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator sin, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(arg0, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.sin(math.degrees(arg0))))
                    continue
                # sqrt
                if operator == "sqrt":
                    # fmt: off
                    assert len(stk) >= 1, "Unable to apply operator sqrt, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    assert isinstance(arg0, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.append(Decimal(math.sqrt(arg0)))
                    continue
                # sub
                if operator == "sub":
                    # fmt: off
                    assert len(stk) >= 2, "Unable to apply operator sub, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, Decimal)
                    assert isinstance(arg1, Decimal)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg1 - arg0)
                    continue
                # true
                if operator == "true":
                    stk.append(True)
                    continue
                # xor
                if operator == "xor":
                    # fmt: off
                    assert len(stk) >= 2, "Unable to apply operator xor, stack underflow"
                    # fmt: on
                    arg0 = stk[-1]
                    arg1 = stk[-2]
                    assert isinstance(arg0, bool)
                    assert isinstance(arg1, bool)
                    stk.pop(len(stk) - 1)
                    stk.pop(len(stk) - 1)
                    stk.append(arg0 or arg1 and not (arg0 and arg1))
                    continue

            # unknown, advance by 1
            i += 1

        # check type(s)
        out: typing.List[Decimal] = []
        for arg0 in stk:
            assert isinstance(arg0, Decimal)
            out.append(arg0)

        # return
        return out
