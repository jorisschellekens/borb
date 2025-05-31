import unittest

from borb.pdf.color.farrow_and_ball_color import FarrowAndBallColor


class TestFarrowAndBallColorGetMatchingColor(unittest.TestCase):

    def test_farrow_and_ball_color_get_matching_color_000(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.ALL_WHITE)[0]
            == "ALL_WHITE"
        )

    def test_farrow_and_ball_color_get_matching_color_001(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.BABOUCE)[0]
            == "BABOUCE"
        )

    def test_farrow_and_ball_color_get_matching_color_002(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.CAGGIAGE_GREEN)[0]
            == "CAGGIAGE_GREEN"
        )

    def test_farrow_and_ball_color_get_matching_color_003(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.DAUPHIN)[0]
            == "DAUPHIN"
        )

    def test_farrow_and_ball_color_get_matching_color_004(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.EATING_ROOM_RED)[0]
            == "EATING_ROOM_RED"
        )

    def test_farrow_and_ball_color_get_matching_color_005(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.FARROWS_CREAM)[0]
            == "FARROWS_CREAM"
        )

    def test_farrow_and_ball_color_get_matching_color_006(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.GERVASE_YELLOW)[0]
            == "GERVASE_YELLOW"
        )

    def test_farrow_and_ball_color_get_matching_color_007(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.HAGUE_BLUE)[0]
            == "HAGUE_BLUE"
        )

    def test_farrow_and_ball_color_get_matching_color_008(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.INDIA_YELLOW)[0]
            == "INDIA_YELLOW"
        )

    def test_farrow_and_ball_color_get_matching_color_009(self):
        assert (
            FarrowAndBallColor.get_matching_color(FarrowAndBallColor.JAMES_WHITE)[0]
            == "JAMES_WHITE"
        )
