#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains everything needed to represent a low-level token in mathematical syntax
"""
import enum
import typing


class TokenType(enum.Enum):
    """
    This enum represents the various kinds of Token objects the Equation parser can encounter
    """

    COMMA = 1
    FUNCTION = 2
    LEFT_PARENTHESIS = 3
    NUMBER = 4
    OPERATOR = 5
    RIGHT_PARENTHESIS = 6
    VARIABLE = 7


class Token:
    """
    This module contains everything needed to represent a low-level token in mathematical syntax
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        is_left_associative: typing.Optional[bool] = None,
        number_of_arguments: typing.Optional[int] = None,
        precedence: typing.Optional[int] = None,
        text: str = "",
        type: TokenType = TokenType.NUMBER,
    ):
        self._children: typing.List["Token"] = []
        self._is_left_associative: typing.Optional[bool] = is_left_associative
        self._number_of_arguments: typing.Optional[int] = number_of_arguments
        self._precedence: typing.Optional[int] = precedence
        self._text: str = text
        self._type: TokenType = type

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_children(self) -> typing.List["Token"]:
        """
        This function returns the children of this Token
        :return:    the children of this Token
        """
        return self._children

    def get_is_left_associative(self) -> typing.Optional[bool]:
        """
        This function return True if this Token represents a left-associative operator,
        False if it represents a right-associative operator, and None if this Token does
        not represent an operator
        :return:    True if this Token represents a left-associative operator
        """
        return self._is_left_associative

    def get_number_of_arguments(self) -> typing.Optional[int]:
        """
        This function returns the number of arguments the operator (represented by this Token)
        accepts, and None if this Token does not represent an operator
        :return:    the number of arguments this operator accepts
        """
        return self._number_of_arguments

    def get_precedence(self) -> typing.Optional[int]:
        """
        This function returns the precedence of the operator (represented by this Token)
        and None if this Token does not represent an operator
        :return:    the precedence of this operator
        """
        return self._precedence

    def get_text(self) -> str:
        """
        This function returns the text associated with this Token
        :return:    the text associated with this Token
        """
        return self._text

    def get_type(self) -> TokenType:
        """
        This function returns the TokenType of this Token
        :return:    the TokenType of this Token
        """
        return self._type
