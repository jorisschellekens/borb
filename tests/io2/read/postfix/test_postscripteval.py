import typing
import unittest
from decimal import Decimal

from borb.io.read.postfix.postfix_eval import PostScriptEval


class TestPostscriptEval(unittest.TestCase):
    """
    This test checks the PostscriptEval object, which is used to
    evaluate Function objects.
    """

    def test_postscripteval_evaluate(self):

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

        # assert len
        assert len(out) == 1

        # assert value
        assert abs(float(out[0]) - 0.6338117228265895963801312974) < 1 * 10 ** -5
