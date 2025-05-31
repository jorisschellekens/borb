import unittest

from borb.pdf.color.pantone_color import PantoneColor


class TestPantoneColorGetMatchingColor(unittest.TestCase):

    def test_pantone_color_get_matching_color_000(self):
        assert (
            PantoneColor.get_matching_color(PantoneColor.ABBEY_STONE)[0]
            == "ABBEY_STONE"
        )

    def test_pantone_color_get_matching_color_001(self):
        assert PantoneColor.get_matching_color(PantoneColor.BABY_BLUE)[0] == "BABY_BLUE"

    def test_pantone_color_get_matching_color_002(self):
        assert PantoneColor.get_matching_color(PantoneColor.CABARET)[0] == "CABARET"

    def test_pantone_color_get_matching_color_003(self):
        assert PantoneColor.get_matching_color(PantoneColor.DACHSHUND)[0] == "DACHSHUND"

    def test_pantone_color_get_matching_color_004(self):
        assert PantoneColor.get_matching_color(PantoneColor.EARTH_RED)[0] == "EARTH_RED"

    def test_pantone_color_get_matching_color_005(self):
        assert (
            PantoneColor.get_matching_color(PantoneColor.FADED_ROSE)[0] == "FADED_ROSE"
        )

    def test_pantone_color_get_matching_color_006(self):
        assert (
            PantoneColor.get_matching_color(PantoneColor.GALAPAGOS_GREEN)[0]
            == "GALAPAGOS_GREEN"
        )

    def test_pantone_color_get_matching_color_007(self):
        assert (
            PantoneColor.get_matching_color(PantoneColor.HABANERO_GOLD)[0]
            == "HABANERO_GOLD"
        )

    def test_pantone_color_get_matching_color_008(self):
        assert PantoneColor.get_matching_color(PantoneColor.IBIS_ROSE)[0] == "IBIS_ROSE"

    def test_pantone_color_get_matching_color_009(self):
        assert PantoneColor.get_matching_color(PantoneColor.JACARANDA)[0] == "JACARANDA"
