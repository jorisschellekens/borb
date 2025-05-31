#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class to represent and manage software licenses.

This class provides functionality to verify, retrieve, and manage the state of a software license.
"""
import datetime
import pathlib
import typing


class License:
    """
    A class to represent and manage software licenses.

    This class provides functionality to verify, retrieve, and manage the state of a software license.
    """

    __BORB_PUBLIC_KEYS: typing.List[bytes] = [
        b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvC5Daxt1u0DdxjvHrcpr
HPWcmy48umRPwwVTqJEokPkC0UZK+6riD4ZZSHIgCL0IqnqbNqqytcDScF9lZOvq
y/5j8sVHFSpGlgHRLZBnCyFrlFH7XUAs/97Is9/SG8ucKgyFnAmjxCNo6IrKaUIW
OcCO2UjRD+3m56w5vf4XSGoDeG1Ghd0bfk4nApUpZaYfghbRMQydCRukXC3fzEpO
uoFWP16g7SQzIiFbwMrlZOp+CG51wZNmIzi3/fRZxoLkPAtpbVBUDiEZiwWE4xkX
eBo3E56kBwFIk0PNyJ5yaqiInwZlYAe2xet3pQgDk7OS7hirAh2NklXSJIP2pPII
TQIDAQAB
-----END PUBLIC KEY-----"""
    ]

    __COMPANY: typing.Optional[str] = None
    __NAME: typing.Optional[str] = None
    __MAX_VERSION: typing.Optional["Version"] = None
    __MIN_DATE: typing.Optional[datetime.datetime] = None
    __MAX_DATE: typing.Optional[datetime.datetime] = None

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __parse_date_str(s: typing.Optional[str]) -> typing.Optional[datetime.datetime]:
        if s is None:
            return None
        try:
            return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    @staticmethod
    def __parse_version_str(s: typing.Optional[str]) -> typing.Optional["Version"]:
        if s is None:
            return None
        try:
            from borb.pdf.license.version import Version

            return Version(s)
        except:
            return None

    #
    # PUBLIC
    #

    @staticmethod
    def create_license(
        company: str,
        license_path: typing.Union[str, pathlib.Path],
        max_date: datetime.datetime,
        max_version: "Version",
        min_date: datetime.datetime,
        name: str,
        private_key_path: typing.Union[str, pathlib.Path],
    ):
        """
        Create a new software license with the provided parameters.

        :param company: str - The name of the company for which the license is being created.
        :param license_path: typing.Union[str, pathlib.Path] - The file path where the license file will be saved.
        :param max_date: datetime.datetime - The maximum expiration date for the license.
        :param max_version: Version - The maximum software version this license applies to.
        :param min_date: datetime.datetime - The minimum start date for the license validity.
        :param name: str - The name of the individual or organization the license is issued to.
        :param private_key_path: typing.Union[str, pathlib.Path] - The file path to the private key used to sign the license.
        :return: None
        """
        # create license dictionary
        # fmt: off
        license_as_json: typing.Dict[str, str] = {
            "company": company,
            "name": name,
            "max_version": str(max_version),
            "min_date": min_date.strftime("%Y-%m-%d %H:%M:%S"),
            "max_date": max_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        # fmt: on

        # convert to bytes
        # fmt: off
        unsigned_license_hash: bytes = b''
        try:
            import hashlib
            import json
            unsigned_license_hash = hashlib.sha256(json.dumps(license_as_json, indent=3).encode()).hexdigest().encode()
        except:
            pass
        # fmt: on

        # Load private key from a file
        if isinstance(private_key_path, str):
            private_key_path = pathlib.Path(private_key_path)
        assert isinstance(private_key_path, pathlib.Path)
        assert private_key_path.exists()
        try:
            from cryptography.hazmat.primitives import serialization  # type: ignore[import-not-found]

            with open(private_key_path, "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(), password=None
                )
        except:
            pass

        # Encode message with private key
        license_bytes_signed_hash: bytes = b""
        try:
            from cryptography.hazmat.primitives.asymmetric import padding  # type: ignore[import-not-found]
            from cryptography.hazmat.primitives import hashes  # type: ignore[import-not-found]

            license_bytes_signed_hash = private_key.sign(
                unsigned_license_hash, padding.PKCS1v15(), hashes.SHA256()
            )
        except:
            pass

        # enter key in dictionary
        try:
            import base64

            license_as_json["license_key"] = base64.b64encode(
                license_bytes_signed_hash
            ).decode()
        except:
            pass

        # return
        try:
            import json

            with open(license_path, "w") as license_file_handle:
                license_file_handle.write(json.dumps(license_as_json, indent=3))
        except:
            pass

    @staticmethod
    def get_company() -> typing.Optional[str]:
        """
        Retrieve the company associated with the registered license.

        :return: The name (of the company), or None if the license is not registered.
        """
        return License.__COMPANY

    @staticmethod
    def get_max_date() -> typing.Optional[datetime.datetime]:
        """
        Retrieve the (max) date until which the license is valid.

        :return: The (max) date, or None if the license is not registered.
        """
        return License.__MAX_DATE

    @staticmethod
    def get_max_version() -> typing.Optional["Version"]:
        """
        Retrieve the (max) version of the software that the license is valid for.

        :return: The version object, or None if the license is not registered.
        """
        return License.__MAX_VERSION

    @staticmethod
    def get_min_date() -> typing.Optional[datetime.datetime]:
        """
        Retrieve the (min) date from which the license is valid.

        :return: The (min) date, or None if the license is not registered.
        """
        return License.__MIN_DATE

    @staticmethod
    def get_name() -> typing.Optional[str]:
        """
        Retrieve the name of the individual associated with the registered license.

        :return: The name (of the person), or None if the license is not registered.
        """
        return License.__NAME

    @staticmethod
    def register(where_from: typing.Union[str, pathlib.Path]) -> bool:
        """
        Register an entity based on the specified source location.

        :param where_from:  The source location from which to register.
                            Can be a string representing a file path or a `pathlib.Path` object.
        :return: True if the registration is successful, False otherwise.
        """
        # IF where_from is a str
        # THEN we convert it into a pathlib.Path
        if isinstance(where_from, str):
            where_from = pathlib.Path(where_from)

        # IF where_from is a pathlib.Path
        # THEN it must exist AND be a file
        assert isinstance(where_from, pathlib.Path)
        assert where_from.exists()
        assert where_from.is_file()

        try:
            import hashlib
            from cryptography.hazmat.primitives import serialization  # type: ignore[import-not-found]
            from cryptography.hazmat.primitives import hashes  # type: ignore[import-not-found]
            from cryptography.hazmat.primitives.asymmetric import padding  # type: ignore[import-not-found]
            from cryptography.hazmat.primitives.asymmetric import rsa  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'cryptography' library to use the License class. "
                "You can install it with 'pip install cryptography'."
            )

        # read json, parse, fill in fields
        license_as_json: typing.Dict[str, typing.Any] = {}
        try:
            import json

            with open(where_from, "r") as fh:
                license_as_json = json.loads(fh.read())
        except:
            pass

        # get the license key (signed hash)
        signed_license_hash: bytes = license_as_json.get("license_key", "").encode()

        # calculate the license key (unsigned hash)
        import copy

        license_as_json_dup = copy.deepcopy(license_as_json)
        if "license_key" in license_as_json_dup:
            license_as_json_dup.pop("license_key")
        unsigned_license_hash: bytes = b""
        try:
            import hashlib
            import json

            unsigned_license_hash = (
                hashlib.sha256(json.dumps(license_as_json_dup, indent=3).encode())
                .hexdigest()
                .encode()
            )
        except:
            pass

        # verify using the public key(s)
        for public_key_bytes in License.__BORB_PUBLIC_KEYS:

            # read
            try:
                public_key = serialization.load_pem_public_key(public_key_bytes)
            except Exception as e:
                continue

            # verify
            try:
                import base64

                public_key.verify(
                    base64.b64decode(signed_license_hash),
                    unsigned_license_hash,
                    padding.PKCS1v15(),
                    hashes.SHA256(),
                )

                # IF we got there, verification did not fail (throw an error/assert)
                # THEN we can set the static fields to the information in the license (json)
                # fmt: off
                License.__COMPANY = license_as_json.get("company", "")
                License.__NAME = license_as_json.get("name", None) or license_as_json.get("anonymous_user_id", None) or ""
                License.__MAX_VERSION = License.__parse_version_str(license_as_json.get("max_version", None))
                License.__MIN_DATE = License.__parse_date_str(license_as_json.get("min_date", None))
                License.__MAX_DATE = License.__parse_date_str(license_as_json.get("max_date", None))
                # fmt: on

                # IF the validity can not be confirmed
                # THEN delete all set information AND throw assert
                if (
                    License.__MIN_DATE is None
                    or License.__MAX_DATE is None
                    or License.__MAX_VERSION is None
                ):
                    License.__COMPANY = None
                    License.__NAME = None
                    License.__MAX_VERSION = None
                    License.__MIN_DATE = None
                    License.__MAX_DATE = None
                    assert False

                # IF the validity of the license (version) has expired
                # THEN delete all set information and raise assert
                from borb.pdf.license.version import Version

                if License.__MAX_VERSION < Version.get_current_version():
                    License.__COMPANY = None
                    License.__NAME = None
                    License.__MAX_VERSION = None
                    License.__MIN_DATE = None
                    License.__MAX_DATE = None
                    assert False

                # IF the validity of the license has expired
                # THEN delete all set information AND throw assert
                if License.__MAX_DATE < datetime.datetime.now():
                    License.__COMPANY = None
                    License.__NAME = None
                    License.__MAX_VERSION = None
                    License.__MIN_DATE = None
                    License.__MAX_DATE = None
                    assert False

                # IF the license is not valid YET
                # THEN delete all set information and throw assert
                if License.__MIN_DATE > datetime.datetime.now():
                    License.__COMPANY = None
                    License.__NAME = None
                    License.__MAX_VERSION = None
                    License.__MIN_DATE = None
                    License.__MAX_DATE = None
                    assert False

                # IF we got here
                # THEN the license must be valid
                return True

            except:
                pass

        # return
        return False


if __name__ == "__main__":
    from borb.pdf.license.version import Version

    License.create_license(
        company="borb EZ",
        license_path="license_for_borb_ez.json",
        max_date=datetime.datetime.now() + datetime.timedelta(days=365),
        max_version=Version("3.0.0"),
        min_date=datetime.datetime.now(),
        name="Joris Schellekens",
        private_key_path="/home/joris-schellekens/Code/borb-license-key/borb-license-key-private-001.pem",
    )
    License.register("license_for_borb_ez.json")
