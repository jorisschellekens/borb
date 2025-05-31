import unittest

from borb.pdf.license.version import Version


class TestVersion(unittest.TestCase):

    def test_version_major_bump(self):
        assert Version("3.0.0") > Version("2.9.0")

    def test_version_minor_bump(self):
        assert Version("2.9.0") > Version("2.8.0")

    def test_version_patch_bump(self):
        assert Version("2.9.2") > Version("2.9.0")
