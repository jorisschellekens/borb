import pathlib
import unittest
import datetime

from borb.pdf import Paragraph
from borb.pdf.license.license import License
from borb.pdf.license.version import Version


class TestLicense(unittest.TestCase):

    PRIVATE_KEY_PATH: pathlib.Path = pathlib.Path(
        "/home/joris-schellekens/Code/borb-license-key/borb-license-key-private-001.pem"
    )

    def test_create_license(self):
        License.create_license(
            company="borb EZ",
            license_path="license.json",
            max_date=datetime.datetime.now() + datetime.timedelta(days=365),
            max_version=Version("3.0.0"),
            min_date=datetime.datetime.now(),
            name="Joris Schellekens",
            private_key_path=TestLicense.PRIVATE_KEY_PATH,
        )
        pathlib.Path("license.json").unlink()

    def test_register_license(self):
        License.create_license(
            company="borb EZ",
            license_path="license.json",
            max_date=datetime.datetime.now() + datetime.timedelta(days=365),
            max_version=Version("3.0.0"),
            min_date=datetime.datetime.now(),
            name="Joris Schellekens",
            private_key_path=TestLicense.PRIVATE_KEY_PATH,
        )
        assert License.register("license.json")
        pathlib.Path("license.json").unlink()

    def test_get_license_information(self):
        License.create_license(
            company="borb EZ",
            license_path="license.json",
            max_date=datetime.datetime.now() + datetime.timedelta(days=365),
            max_version=Version("3.0.0"),
            min_date=datetime.datetime.now(),
            name="Joris Schellekens",
            private_key_path=TestLicense.PRIVATE_KEY_PATH,
        )
        assert License.register("license.json")
        assert License.get_company() == "borb EZ"
        assert License.get_max_version() == Version("3.0.0")
        assert License.get_name() == "Joris Schellekens"
        pathlib.Path("license.json").unlink()
