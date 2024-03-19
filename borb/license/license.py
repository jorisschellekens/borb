#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A license (or licence) is an official permission or permit to do, use, or own something
(as well as the document of that permission or permit). A license is granted by a party (licensor) to another party
(licensee) as an element of an agreement between those parties. In the case of a license issued by a government,
the license is obtained by applying for it. In the case of a private party, it is by a specific agreement,
usually in writing (such as a lease or other contract).

The simplest definition is "A license is a promise not to sue," because a license usually either permits
the licensed party to engage in an activity which is illegal, and subject to prosecution,
without the license (e.g. fishing, driving an automobile, or operating a broadcast radio or television station),
or it permits the licensed party to do something that would violate the rights of the licensing party
(e.g. make copies of a copyrighted work), which, without the license,
the licensed party could be sued, civilly, criminally, or both.
"""
import base64
import datetime
import json
import logging
import typing
import hashlib
import pathlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from borb.license.uuid import UUID

logger = logging.getLogger(__name__)


class License:
    """
    A license (or licence) is an official permission or permit to do, use, or own something
    (as well as the document of that permission or permit). A license is granted by a party (licensor) to another party
    (licensee) as an element of an agreement between those parties. In the case of a license issued by a government,
    the license is obtained by applying for it. In the case of a private party, it is by a specific agreement,
    usually in writing (such as a lease or other contract).
    """

    # fmt: off
    _LICENSE_COMPANY: typing.Optional[str] = None
    _LICENSE_USER_ID: typing.Optional[str] = None
    _LICENSE_VALID_FROM_IN_MS: typing.Optional[int] = None
    _LICENSE_VALID_UNTIL_IN_MS: typing.Optional[int] = None
    # fmt: on

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _create_key_pair(
        private_key_file: pathlib.Path = pathlib.Path(__file__).parent
        / "private_key.pem",
        public_key_file: pathlib.Path = pathlib.Path(__file__).parent
        / "public_key.pem",
    ):
        # Generate a new RSA private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Serialize the private key to PEM format and save to file
        with open(private_key_file, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        # Serialize the public key to PEM format and save to file
        public_key = private_key.public_key()
        with open(public_key_file, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    @staticmethod
    def _create_license(
        company: str = "",
        output_file: pathlib.Path = pathlib.Path(__file__).parent / "license_key.json",
        private_key_file: pathlib.Path = pathlib.Path(
            "/home/joris/Code/borb-license-key-private/borb-license-key-private-001.pem"
        ),
        user_id: str = UUID.get(),
        valid_from_in_ms: int = int(datetime.datetime.now().timestamp() * 1000),
        valid_until_in_ms: int = int(datetime.datetime.now().timestamp() * 1000)
        + 7 * 24 * 60 * 60 * 1000,
    ) -> None:
        # set up dictionary
        # fmt: off
        license_dict: typing.Dict[str, str] = {
            "anonymous_user_id": user_id,
            "company": company,
            "valid_from_as_str": datetime.datetime.fromtimestamp(valid_from_in_ms / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            "valid_until_as_str": datetime.datetime.fromtimestamp(valid_until_in_ms / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        }
        # fmt: on

        # convert to bytes
        license_bytes: bytes = json.dumps(license_dict, indent=3).encode()
        license_bytes_unsigned_hash: bytes = (
            hashlib.sha256(license_bytes).hexdigest().encode()
        )

        # Load private key from a file
        with open(private_key_file, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        # Encode message with private key
        license_bytes_signed_hash = private_key.sign(
            license_bytes_unsigned_hash, padding.PKCS1v15(), hashes.SHA256()
        )

        # Base64 encode the encrypted message for transmission
        base64_license_bytes_signed_hash = base64.b64encode(license_bytes_signed_hash)

        # enter key in dictionary
        license_dict["license_key"] = base64_license_bytes_signed_hash.decode()

        # dump dictionary
        with open(output_file, "w") as fh:
            fh.write(json.dumps(license_dict, indent=3))

    @staticmethod
    def _datetime_str_to_ms(s: typing.Optional[str]) -> typing.Optional[int]:
        if s is None:
            return None
        try:
            return int(
                datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timestamp() * 1000
            )
        except:
            logger.warning("Unable to convert %s to a datetime" % str(s))
            return None

    #
    # PUBLIC
    #

    @staticmethod
    def get_company() -> typing.Optional[str]:
        """
        This function returns the company to which this License was granted
        :return:    the company to which this License was granted
        """
        return License._LICENSE_COMPANY

    @staticmethod
    def get_user_id() -> typing.Optional[str]:
        """
        This function returns the user_id to which this License was granted
        :return:    the user_id to which this License was granted
        """
        return License._LICENSE_USER_ID

    @staticmethod
    def get_valid_from_in_ms() -> typing.Optional[int]:
        """
        This function returns the start of the validity period of this License
        :return:    the start of the validity period of this License
        """
        return License._LICENSE_VALID_FROM_IN_MS

    @staticmethod
    def get_valid_until_in_ms() -> typing.Optional[int]:
        """
        This function returns the end of the validity period of this License
        :return:    the end of the validity period of this License
        """
        return License._LICENSE_VALID_UNTIL_IN_MS

    @staticmethod
    def register(path_to_license_file: pathlib.Path) -> bool:
        """
        This function (attempts to) register a license (specified as a Path)
        :param path_to_license_file:    the license to register
        :return:                        True if the license is valid, False otherwise
        """

        # check whether the file exists
        if not path_to_license_file.exists():
            logger.warning("File %s does not exist" % str(path_to_license_file))
            return False

        # read license
        json_dict: typing.Optional[typing.Dict[str, str]] = None
        try:
            with open(path_to_license_file, "r") as fh:
                json_dict = json.loads(fh.read())
        except:
            # fmt: off
            logger.warning("Unable to convert contents of %s to JSON" % str(path_to_license_file))
            # fmt: on
            return False

        # remove key entry
        if json_dict is None:
            return False
        license_hash_0: bytes = json_dict.get("license_key", "").encode()
        json_dict.pop("license_key")

        # to bytes
        license_bytes1: bytes = json.dumps(json_dict, indent=3).encode()

        # hash
        license_hash_1: bytes = hashlib.sha256(license_bytes1).hexdigest().encode()

        # Load public key(s) from a file
        key_dir: pathlib.Path = pathlib.Path(__file__).parent / "public_keys"
        assert key_dir.exists()
        assert key_dir.is_dir()
        for public_key_file in [key_dir / "public_key_001.pem"]:
            # read key
            with open(public_key_file, "rb") as f:
                public_key = serialization.load_pem_public_key(f.read())

            # Base64 decode the encoded message
            encrypted_message = base64.b64decode(license_hash_0)

            # Verify the signature using the public key
            try:
                public_key.verify(
                    encrypted_message,
                    license_hash_1,
                    padding.PKCS1v15(),
                    hashes.SHA256(),
                )
                # fmt: off
                License._LICENSE_COMPANY = json_dict.get("company", None)
                License._LICENSE_USER_ID = json_dict.get("anonymous_user_id", None)
                License._LICENSE_VALID_FROM_IN_MS = License._datetime_str_to_ms(json_dict.get("valid_from_as_str", None))
                License._LICENSE_VALID_UNTIL_IN_MS = License._datetime_str_to_ms(json_dict.get("valid_until_as_str", None))
                # fmt: on

                # check _LICENSE_VALID_FROM_IN_MS
                now_in_ms: int = int(datetime.datetime.now().timestamp() * 1000)
                if (
                    License._LICENSE_VALID_FROM_IN_MS is not None
                    and License._LICENSE_VALID_FROM_IN_MS > now_in_ms
                ):
                    # fmt: off
                    logger.warning("License %s is valid FROM %s" % (str(path_to_license_file), json_dict.get("valid_from_as_str", "N.A.")))
                    # fmt: on
                    License._LICENSE_COMPANY = None
                    License._LICENSE_USER_ID = None
                    License._LICENSE_VALID_FROM_IN_MS = None
                    License._LICENSE_VALID_UNTIL_IN_MS = None
                    return False

                # check _LICENSE_VALID_UNTIL_IN_MS
                if (
                    License._LICENSE_VALID_UNTIL_IN_MS is not None
                    and License._LICENSE_VALID_UNTIL_IN_MS < now_in_ms
                ):
                    # fmt: off
                    logger.warning("License %s is valid UNTIL %s" % (str(path_to_license_file), json_dict.get("valid_until_as_str", "N.A.")))
                    # fmt: on
                    License._LICENSE_COMPANY = None
                    License._LICENSE_USER_ID = None
                    License._LICENSE_VALID_FROM_IN_MS = None
                    License._LICENSE_VALID_UNTIL_IN_MS = None
                    return False

                return True
            except:
                continue

        # default
        return False


if __name__ == "__main__":
    # fmt: off
    # noinspection PyProtectedMember
    License._create_license(
        company="borb (EZ)",
        output_file=pathlib.Path("/home/joris/Code/borb-dev/tests/license/artifacts_test_register_license/license.json"),
        user_id="Joris Schellekens",
    )
    # fmt: on
