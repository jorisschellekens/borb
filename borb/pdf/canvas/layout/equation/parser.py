#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A parser is a software component that takes input data (frequently text) and builds a data structure
– often some kind of parse tree, abstract syntax tree or other hierarchical structure, giving a structural
representation of the input while checking for correct syntax.
The parsing may be preceded or followed by other steps, or these may be combined into a single step.
"""
import typing

from borb.pdf.canvas.layout.equation.token import Token
from borb.pdf.canvas.layout.equation.token import TokenType
from borb.pdf.canvas.layout.equation.tokenizer import Tokenizer


class Parser:
    """
    A parser is a software component that takes input data (frequently text) and builds a data structure
    – often some kind of parse tree, abstract syntax tree or other hierarchical structure, giving a structural
    representation of the input while checking for correct syntax.
    The parsing may be preceded or followed by other steps, or these may be combined into a single step.
    """

    @staticmethod
    def _to_postfix(infix_expression: str) -> typing.List[Token]:
        tokens: typing.List[Token] = Tokenizer.tokenize(infix_expression)
        postfix: typing.List[Token] = []
        operators: typing.List[Token] = []
        for i, t in enumerate(tokens):
            if t.get_type() == TokenType.NUMBER:
                postfix += [t]
                continue
            if t.get_type() == TokenType.VARIABLE:
                postfix += [t]
                continue
            if t.get_type() == TokenType.FUNCTION:
                operators += [t]
                continue
            if t.get_type() == TokenType.OPERATOR:
                while (
                    len(operators) > 0
                    and operators[-1].get_type() != TokenType.LEFT_PARENTHESIS
                    and (
                        operators[-1].get_precedence() > t.get_precedence()
                        or (
                            operators[-1].get_precedence() == t.get_precedence()
                            and t.get_is_left_associative()
                        )
                    )
                ):
                    postfix += [operators[-1]]
                    operators.pop(-1)
                operators += [t]
                continue
            if t.get_type() == TokenType.COMMA:
                while (
                    len(operators) > 0
                    and operators[-1].get_type() != TokenType.LEFT_PARENTHESIS
                ):
                    postfix += [operators[-1]]
                    operators.pop(-1)
                continue
            if t.get_type() == TokenType.LEFT_PARENTHESIS:
                operators += [t]
                continue
            if t.get_type() == TokenType.RIGHT_PARENTHESIS:
                assert len(operators) > 0
                while (
                    len(operators) > 0
                    and operators[-1].get_type() != TokenType.LEFT_PARENTHESIS
                ):
                    postfix += [operators[-1]]
                    operators.pop(-1)
                assert len(operators) > 0
                assert operators[-1].get_type() == TokenType.LEFT_PARENTHESIS
                operators.pop(-1)
                if (
                    len(operators) > 0
                    and operators[-1].get_type() == TokenType.FUNCTION
                ):
                    postfix += [operators[-1]]
                    operators.pop(-1)
                continue

        # while there are tokens on the operator stack:
        #   If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
        #   {assert the operator on top of the stack is not a (left) parenthesis}
        #   pop the operator from the operator stack onto the output queue
        while len(operators) > 0:
            postfix += [operators[-1]]
            operators.pop(-1)

        # return
        return postfix

    @staticmethod
    def to_abstract_syntax_tree(s: str) -> Token:
        """
        This function converts a str to an abstract syntax tree
        :param s:   the input str
        :return:    a Token, representing the root of the syntax tree
        """
        args: typing.List[Token] = []
        postfix: typing.List[Token] = Parser._to_postfix(s)
        for i, t in enumerate(postfix):

            if t.get_type() == TokenType.NUMBER:
                args += [t]
                continue

            if t.get_type() == TokenType.VARIABLE:
                args += [t]
                continue

            if t.get_type() == TokenType.OPERATOR:
                assert len(args) >= t.get_number_of_arguments()
                for _ in range(0, t.get_number_of_arguments()):
                    # noinspection PyProtectedMember
                    t._children += [args[-1]]
                    args.pop(-1)
                args += [t]
                continue

            if t.get_type() == TokenType.FUNCTION:
                assert len(args) >= t.get_number_of_arguments()
                for _ in range(0, t.get_number_of_arguments()):
                    # noinspection PyProtectedMember
                    t._children += [args[-1]]
                    args.pop(-1)
                args += [t]
                continue

        # check
        assert len(args) == 1

        # return
        return args[0]
