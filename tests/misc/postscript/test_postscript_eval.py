import typing
import unittest
from decimal import Decimal

from borb.io.read.postfix.postfix_eval import PostScriptEval


class TestPostscriptEval(unittest.TestCase):
    def test_postscript_eval(self):

        s: str = """
        {
            360 mul sin
            2 div
            exch 360 mul sin
            2 div
            add
        }
        """

        out: typing.List[Decimal] = PostScriptEval.evaluate(
            s, [Decimal(0.5), Decimal(0.4)]
        )
        for x in out:
            print(x)
