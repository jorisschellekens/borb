import typing
import unittest

from borb.io.read.encryption.standard_security_handler import StandardSecurityHandler
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import (
    Dictionary,
    Name,
    String,
    List,
    HexadecimalString,
    Reference,
    Stream,
)


class TestStandardSecurityHandler(unittest.TestCase):
    @staticmethod
    def ints_to_string_object(i: typing.List[int]) -> String:
        return String(str(bytes(i), encoding="utf8"))

    def test_standard_security_handler(self):

        trailer_dictionary = Dictionary()
        trailer_dictionary[Name("ID")] = List()
        trailer_dictionary["ID"].append(
            HexadecimalString("87B0E1BD8B0F59E30AFCF1DB4A6F70B2")
        )
        trailer_dictionary["ID"].append(
            HexadecimalString("29F4AA99CA167B4D90E8853A67131865")
        )

        encryption_dictionary = Dictionary()
        encryption_dictionary.set_parent(trailer_dictionary)
        encryption_dictionary[Name("Filter")] = Name("Standard")
        encryption_dictionary[Name("Length")] = bDecimal(128)

        # fmt: off
        encryption_dictionary[Name("U")] = TestStandardSecurityHandler.ints_to_string_object(
            [
                194, 150, 116, 195, 142, 3, 194, 166,
                19, 52, 68, 121, 53, 194, 174, 6,
                100, 46, 85, 26, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0,
            ]
        )
        # fmt: on

        encryption_dictionary[Name("P")] = bDecimal(-1068)
        encryption_dictionary[Name("R")] = bDecimal(3)
        # fmt: off
        encryption_dictionary[Name("O")] = TestStandardSecurityHandler.ints_to_string_object(
            [194, 128, 194, 176, 195, 141, 194, 188,
             195, 172, 194, 161, 67, 81, 75, 195,
             148, 25, 194, 170, 195, 145, 1, 195,
             179, 194, 140, 195, 189, 195, 155, 117,
             45, 195, 139, 195, 169, 111, 109, 194,
             157, 195, 129, 106, 195, 184, 195, 142,
             44, 49, 194, 172,
            ]
        )
        # fmt: on

        encryption_dictionary[Name("V")] = bDecimal(2)

        # create security handler
        ssh = StandardSecurityHandler(encryption_dictionary)

        # assert ssh._encryption_key
        # fmt: off
        bs: typing.List[int] = [x for x in ssh._encryption_key]
        assert bs == [
            72, 14, 85, 41,
            85, 183, 22, 61,
            205, 229, 51, 104,
            40, 81, 149, 13,
        ]
        # fmt: on

        # fmt: off
        stream_bytes: bytes = bytes([x if x > 0 else x + 256 for x in
                                       [97, -102, 10, -83, -20, 76, 83, -122, 39, 93, -39, 125, 20, 81, 91, 107, 82,
                                        -104, 64, -56, 104, -109, -7, -69, -19, -36, -100, 119, -81, -124, 111, -43, 21,
                                        9, -104, 15, 82, -72, 19, 57, -19, 120, 110, -118, -84, 116, -26, 91, -66, 111,
                                        -35, 32, 17, -119, 14, 96, -83, -122, -106, 6, -53, 89, 41, 117, -42, -22, -14,
                                        64, -85, 30, -81, 59, 81, -120, 29, 96, 49, -110, -18, 121, -112, 14, -20, -104,
                                        -56, 102, 30, 45, -86, -52, 23, -32, 50, 42, 4, 34, -76, 95, 119, -34]])
        # fmt: on

        # build Stream object
        stream_object: Stream = Stream().set_reference(Reference(51, 0))
        stream_object[Name("DecodedBytes")] = stream_bytes

        # decrypt object
        ssh._decrypt_data(stream_object)

        # check content
        decrypted_stream_content: str = str(
            stream_object[Name("DecodedBytes")], encoding="utf8"
        )
        assert decrypted_stream_content.startswith(
            '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
        )
