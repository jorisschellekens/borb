import unittest

from borb.pdf.layout_element.shape.line_art import LineArt


class TestLineArtFlowchartDecisionSize(unittest.TestCase):

    def test_line_art_flowchart_decision_size(self):
        w, h = LineArt.flowchart_decision().get_size(available_space=(2**64, 2**64))
        assert 0 <= w <= 100
        assert 0 <= h <= 100
        assert w in [98, 99, 100] or h in [98, 99, 100]
