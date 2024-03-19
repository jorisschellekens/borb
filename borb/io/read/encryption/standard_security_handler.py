#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF’s standard security handler shall allow access permissions and up to two passwords to be specified for a
document: an owner password and a user password. An application’s decision to encrypt a document shall be
based on whether the user creating the document specifies any passwords or access restrictions.
"""
import hashlib
import typing

from borb.io.read.encryption.rc4 import RC4
from borb.io.read.types import AnyPDFType
from borb.io.read.types import Boolean
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import HexadecimalString
from borb.io.read.types import Name
from borb.io.read.types import Reference
from borb.io.read.types import Stream
from borb.io.read.types import String


class StandardSecurityHandler:
    """
    PDF’s standard security handler shall allow access permissions and up to two passwords to be specified for a
    document: an owner password and a user password. An application’s decision to encrypt a document shall be
    based on whether the user creating the document specifies any passwords or access restrictions.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        encryption_dictionary: Dictionary,
        owner_password: typing.Optional[str] = None,
        user_password: typing.Optional[str] = None,
    ):
        # (Optional) A code specifying the algorithm to be used in encrypting and
        # decrypting the document:
        # 0 An algorithm that is undocumented. This value shall not be used.
        # 1 "Algorithm 1: Encryption of data using the RC4 or AES algorithms" in 7.6.2,
        # "General Encryption Algorithm," with an encryption key length of 40 bits; see
        # below.
        # 2 (PDF 1.4) "Algorithm 1: Encryption of data using the RC4 or AES algorithms"
        # in 7.6.2, "General Encryption Algorithm," but permitting encryption key lengths
        # greater than 40 bits.
        # 3 (PDF 1.4) An unpublished algorithm that permits encryption key lengths
        # ranging from 40 to 128 bits. This value shall not appear in a conforming PDF
        # file.
        # 4 (PDF 1.5) The security handler defines the use of encryption and decryption
        # in the document, using the rules specified by the CF, StmF, and StrF entries.
        # The default value if this entry is omitted shall be 0, but when present should be a
        # value of 1 or greater.
        self._v = int(encryption_dictionary.get("V", bDecimal(0)))

        # (Required) A 32-byte string, based on the user password, that shall be
        # used in determining whether to prompt the user for a password and, if so,
        # whether a valid user or owner password was entered. For more
        # information, see 7.6.3.4, "Password Algorithms."
        self._u: bytes = (
            StandardSecurityHandler._str_to_bytes(
                StandardSecurityHandler._unescape_pdf_syntax(
                    encryption_dictionary.get("U")
                )
            )
            or b""
        )
        assert len(self._u) == 32

        # (Required) A 32-byte string, based on both the owner and user passwords,
        # that shall be used in computing the encryption key and in determining
        # whether a valid owner password was entered. For more information, see
        # 7.6.3.3, "Encryption Key Algorithm," and 7.6.3.4, "Password Algorithms."
        self._o: bytes = (
            StandardSecurityHandler._str_to_bytes(
                StandardSecurityHandler._unescape_pdf_syntax(
                    encryption_dictionary.get("O")
                )
            )
            or b""
        )
        assert self._o is not None
        assert len(self._o) == 32

        # /ID
        trailer: typing.Optional["PDFObject"] = encryption_dictionary.get_parent()  # type: ignore[name-defined]
        assert trailer is not None
        assert isinstance(trailer, Dictionary)
        if "ID" in trailer:
            self._document_id: bytes = trailer["ID"][0].get_content_bytes()

        # (Required) A set of flags specifying which operations shall be permitted
        # when the document is opened with user access (see Table 22).
        assert "P" in encryption_dictionary
        self._permissions: int = int(encryption_dictionary.get("P"))  # type: ignore[arg-type]

        # (Optional; PDF 1.4; only if V is 2 or 3) The length of the encryption key, in bits.
        # The value shall be a multiple of 8, in the range 40 to 128. Default value: 40.
        # fmt: off
        self._key_length: int = int(encryption_dictionary.get("Length", bDecimal(40)))
        assert self._key_length % 8 == 0, "The length of the encryption key, in bits must be a multiple of 8."
        # fmt: on

        # (Required) A number specifying which revision of the standard security
        # handler shall be used to interpret this dictionary
        self._revision: int = int(encryption_dictionary.get("R", bDecimal(0)))

        # (Optional; meaningful only when the value of V is 4; PDF 1.5) Indicates
        # whether the document-level metadata stream (see 14.3.2, "Metadata
        # Streams") shall be encrypted. Conforming products should respect this
        # value.
        # Default value: true.
        # fmt: off
        self._encrypt_metadata: bool = encryption_dictionary.get("EncryptMetadata", Boolean(True))
        # fmt: on

        # verify password(s)
        password: typing.Optional[bytes] = None
        if user_password is not None:
            self.authenticate_user_password(bytes(user_password, encoding="charmap"))
            password = bytes(user_password, encoding="charmap")
        if owner_password is not None:
            self.authenticate_owner_password(bytes(owner_password, encoding="charmap"))
            password = bytes(owner_password, encoding="charmap")

        # calculate encryption_key
        # assert password is not None
        self._encryption_key: bytes = self._compute_encryption_key(password)

    #
    # PRIVATE
    #

    def _compute_encryption_dictionary_o_value(
        self,
        owner_password: typing.Optional[bytes],
        user_password: typing.Optional[bytes],
    ) -> bytes:
        """
        Algorithm 3: Computing the encryption dictionary’s O (owner password) value
        """

        # a) Pad or truncate the owner password string as described in step (a) of "Algorithm 2: Computing an
        # encryption key". If there is no owner password, use the user password instead.
        padded_owner_password: bytes = StandardSecurityHandler._pad_or_truncate(
            owner_password
        )

        # b) Initialize the MD5 hash function and pass the result of step (a) as input to this function.
        h = hashlib.md5()
        h.update(padded_owner_password)

        # c) (Security handlers of revision 3 or greater) Do the following 50 times: Take the output from the previous
        # MD5 hash and pass it as input into a new MD5 hash.
        if self._revision >= 3:
            prev_digest: bytes = h.digest()[0 : int(self._key_length / 8)]
            for _ in range(0, 50):
                h = hashlib.md5()
                h.update(prev_digest)
                prev_digest = h.digest()[0 : int(self._key_length / 8)]

        # d) Create an RC4 encryption key using the first n bytes of the output from the final MD5 hash, where n shall
        # always be 5 for security handlers of revision 2 but, for security handlers of revision 3 or greater, shall
        # depend on the value of the encryption dictionary’s Length entry.
        key: bytes = h.digest()[0:5]
        if self._revision >= 3:
            key = h.digest()[0 : int(self._key_length / 8)]

        # e) Pad or truncate the user password string as described in step (a) of "Algorithm 2: Computing an encryption
        # key".
        padded_user_password: bytes = StandardSecurityHandler._pad_or_truncate(
            user_password
        )

        # f) Encrypt the result of step (e), using an RC4 encryption function with the encryption key obtained in step
        # (d).
        rc4: RC4 = RC4()
        owner_key: bytes = rc4.encrypt(key, padded_user_password)

        # g) (Security handlers of revision 3 or greater) Do the following 19 times: Take the output from the previous
        # invocation of the RC4 function and pass it as input to a new invocation of the function; use an encryption
        # key generated by taking each byte of the encryption key obtained in step (d) and performing an XOR
        # (exclusive or) operation between that byte and the single-byte value of the iteration counter (from 1 to 19).
        if self._revision >= 3:
            for i in range(1, 20):
                key2: bytes = bytes([b ^ i for b in key])
                owner_key = RC4().encrypt(key2, owner_key)

        # h) Store the output from the final invocation of the RC4 function as the value of the O entry in the encryption
        # dictionary.
        self._o = owner_key
        return owner_key

    def _compute_encryption_dictionary_u_value(self, user_password_string: bytes):
        """
        Algorithm 4: Computing the encryption dictionary’s U (user password) value (Security handlers of revision 2)
        Algorithm 5: Computing the encryption dictionary’s U (user password) value (Security handlers of revision 3 or greater)
        """
        if self._revision == 2:
            # a) Create an encryption key based on the user password string, as described in "Algorithm 2: Computing an
            # encryption key".
            key_rev_2: bytes = self._compute_encryption_key(user_password_string)

            # b) Encrypt the 32-byte padding string shown in step (a) of "Algorithm 2: Computing an encryption key", using
            # an RC4 encryption function with the encryption key from the preceding step.

            # c) Store the result of step (b) as the value of the U entry in the encryption dictionary.
            self._u = RC4().encrypt(
                key_rev_2, StandardSecurityHandler._pad_or_truncate(None)
            )

            return self._u

        if self._revision >= 3:
            # a) Create an encryption key based on the user password string, as described in "Algorithm 2: Computing an
            # encryption key".
            key_rev_3: bytes = self._compute_encryption_key(user_password_string)

            # b) Initialize the MD5 hash function and pass the 32-byte padding string shown in step (a) of "Algorithm 2:
            # Computing an encryption key" as input to this function.
            h = hashlib.md5()
            h.update(StandardSecurityHandler._pad_or_truncate(None))

            # c) Pass the first element of the file’s file identifier array (the value of the ID entry in the document’s trailer
            # dictionary; see Table 15) to the hash function and finish the hash.
            h.update(self._document_id)
            digest: bytes = h.digest()

            # d) Encrypt the 16-byte result of the hash, using an RC4 encryption function with the encryption key from step
            # (a).
            digest = RC4().encrypt(key_rev_3, digest)

            # e) Do the following 19 times: Take the output from the previous invocation of the RC4 function and pass it as
            # input to a new invocation of the function; use an encryption key generated by taking each byte of the
            # original encryption key obtained in step (a) and performing an XOR (exclusive or) operation between that
            # byte and the single-byte value of the iteration counter (from 1 to 19).
            if self._revision >= 3:
                for i in range(1, 20):
                    key2: bytes = bytes([b ^ i for b in key_rev_3])
                    digest = RC4().encrypt(key2, digest)

            # f) Append 16 bytes of arbitrary padding to the output from the final invocation of the RC4 function and store
            # the 32-byte result as the value of the U entry in the encryption dictionary.
            digest += bytes(
                [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
            )
            self._u = digest

    def _compute_encryption_key(self, password: typing.Optional[bytes]) -> bytes:
        # a) Pad or truncate the password string to exactly 32 bytes. If the password string is more than 32 bytes long,
        # use only its first 32 bytes; if it is less than 32 bytes long, pad it by appending the required number of
        # additional bytes from the beginning of the following padding string:
        # < 28 BF 4E 5E 4E 75 8A 41 64 00 4E 56 FF FA 01 08
        # 2E 2E 00 B6 D0 68 3E 80 2F 0C A9 FE 64 53 69 7A >
        # That is, if the password string is n bytes long, append the first 32 - n bytes of the padding string to the end
        # of the password string. If the password string is empty (zero-length), meaning there is no user password,
        # substitute the entire padding string in its place.

        # b) Initialize the MD5 hash function and pass the result of step (a) as input to this function.
        h = hashlib.md5()
        h.update(StandardSecurityHandler._pad_or_truncate(password))

        # c) Pass the value of the encryption dictionary’s O entry to the MD5 hash function. ("Algorithm 3: Computing
        # the encryption dictionary’s O (owner password) value" shows how the O value is computed.)
        h.update(self._o)

        # d) Convert the integer value of the P entry to a 32-bit unsigned binary number and pass these bytes to the
        # MD5 hash function, low-order byte first.
        h.update(self._permissions.to_bytes(length=4, byteorder="little", signed=True))

        # e) Pass the first element of the file’s file identifier array (the value of the ID entry in the document’s trailer
        # dictionary; see Table 15) to the MD5 hash function.
        h.update(self._document_id)

        # f) (Security handlers of revision 4 or greater) If document metadata is not being encrypted, pass 4 bytes with
        # the value 0xFFFFFFFF to the MD5 hash function.
        if self._revision >= 4 and not self._encrypt_metadata:
            h.update(bytes([255, 255, 255, 255]))

        # g) Finish the hash.
        digest: bytes = h.digest()

        # h) (Security handlers of revision 3 or greater) Do the following 50 times: Take the output from the previous
        # MD5 hash and pass the first n bytes of the output as input into a new MD5 hash, where n is the number of
        # bytes of the encryption key as defined by the value of the encryption dictionary’s Length entry.
        n: int = 0
        if self._revision >= 3:
            n = int(self._key_length / 8)
            for _ in range(0, 50):
                h2 = hashlib.md5()
                h2.update(digest[0:n])
                digest = h2.digest()

        # i) Set the encryption key to the first n bytes of the output from the final MD5 hash, where n shall always be 5
        # for security handlers of revision 2 but, for security handlers of revision 3 or greater, shall depend on the
        # value of the encryption dictionary’s Length entry.
        n = 5
        if self._revision >= 3:
            n = int(self._key_length / 8)
        encryption_key: bytes = digest[0:n]

        return encryption_key

    @staticmethod
    def _pad_or_truncate(b: typing.Optional[bytes]) -> bytes:
        # fmt: off
        padding: bytes = bytes([40, 191, 78, 94, 78, 117, 138, 65,
                                100, 0, 78, 86, 255, 250, 1, 8,
                                46, 46, 0, 182, 208, 104, 62, 128,
                                47, 12, 169, 254, 100, 83, 105, 122])
        # fmt: on
        if b is None:
            return padding
        if len(b) > 32:
            return b[0:32]
        if len(b) < 32:
            b2: bytes = b + padding
            return b2[0:32]
        return b

    @staticmethod
    def _str_to_bytes(s: typing.Optional[str]) -> typing.Optional[bytes]:
        if s is None:
            return None
        return bytes(s, encoding="charmap")

    @staticmethod
    def _unescape_pdf_syntax(
        s: typing.Union[str, String, None]
    ) -> typing.Optional[str]:
        # None
        if s is None:
            return None
        # String
        if isinstance(s, String):
            return str(s.get_content_bytes(), encoding="latin1")
        # str
        return str(String(s).get_content_bytes(), encoding="latin1")

    #
    # PUBLIC
    #

    def authenticate_owner_password(self, owner_password: bytes) -> bool:
        """
        Algorithm 7: Authenticating the owner password
        :param owner_password:  the owner password
        :return:                True if the owner password matches, False otherwise
        """
        # a) Compute an encryption key from the supplied password string, as described in steps (a) to (d) of
        # "Algorithm 3: Computing the encryption dictionary’s O (owner password) value".

        # b) (Security handlers of revision 2 only) Decrypt the value of the encryption dictionary’s O entry, using an RC4
        # encryption function with the encryption key computed in step (a).
        # (Security handlers of revision 3 or greater) Do the following 20 times: Decrypt the value of the encryption
        # dictionary’s O entry (first iteration) or the output from the previous iteration (all subsequent iterations),
        # using an RC4 encryption function with a different encryption key at each iteration. The key shall be
        # generated by taking the original key (obtained in step (a)) and performing an XOR (exclusive or) operation
        # between each byte of the key and the single-byte value of the iteration counter (from 19 to 0).

        # c) The result of step (b) purports to be the user password. Authenticate this user password using "Algorithm
        # 6: Authenticating the user password". If it is correct, the password supplied is the correct owner password.

        # TODO
        return False

    def authenticate_user_password(self, user_password: bytes) -> bool:
        """
        Algorithm 6: Authenticating the user password
        :param user_password:   the user password
        :return:                True if the user password matches, False otherwise
        """
        # a) Perform all but the last step of "Algorithm 4: Computing the encryption dictionary’s U (user password)
        # value (Security handlers of revision 2)" or "Algorithm 5: Computing the encryption dictionary’s U (user
        # password) value (Security handlers of revision 3 or greater)" using the supplied password string.
        previous_u_value: bytes = self._u
        self._compute_encryption_dictionary_u_value(user_password)
        u_value: bytes = self._u
        self._u = previous_u_value

        # b)If the result of step (a) is equal to the value of the encryption dictionary’s U entry (comparing on the first 16
        # bytes in the case of security handlers of revision 3 or greater), the password supplied is the correct user
        # password. The key obtained in step (a) (that is, in the first step of "Algorithm 4: Computing the encryption
        # dictionary’s U (user password) value (Security handlers of revision 2)" or "Algorithm 5: Computing the
        # encryption dictionary’s U (user password) value (Security handlers of revision 3 or greater)") shall be used
        # to decrypt the document.
        if self._revision >= 3:
            return self._u[0:16] == u_value[0:16]
        return self._u == u_value

    def decrypt(self, object: AnyPDFType) -> AnyPDFType:
        """
        This function decrypts an object inside the PDF
        :param object:  the object to be decrypted
        :return:        the decrypted object
        """
        return self.encrypt(object)

    def encrypt(self, object: AnyPDFType) -> AnyPDFType:
        """
        This function encrypts an object inside the PDF
        :param object:  the object to be encrypted
        :return:        the encrypted object
        """
        # a) Obtain the object number and generation number from the object identifier of the string or stream to be
        # encrypted (see 7.3.10, "Indirect Objects"). If the string is a direct object, use the identifier of the indirect
        # object containing it.
        reference: typing.Optional[Reference] = object.get_reference()
        if reference is None:
            parent: typing.Optional["PDFObject"] = object.get_parent()  # type: ignore[name-defined]
            assert parent is not None
            reference = parent.get_reference()
        assert reference is not None
        assert reference.object_number is not None
        assert reference.generation_number is not None
        object_number: int = reference.object_number
        generation_number: int = reference.generation_number

        # b) For all strings and streams without crypt filter specifier; treating the object number and generation number
        # as binary integers, extend the original n-byte encryption key to n + 5 bytes by appending the low-order 3
        # bytes of the object number and the low-order 2 bytes of the generation number in that order, low-order byte
        # first. (n is 5 unless the value of V in the encryption dictionary is greater than 1, in which case n is the value
        # of Length divided by 8.)
        # If using the AES algorithm, extend the encryption key an additional 4 bytes by adding the value “sAlT”,
        # which corresponds to the hexadecimal values 0x73, 0x41, 0x6C, 0x54. (This addition is done for backward
        # compatibility and is not intended to provide additional security.)
        encryption_key = (
            self._encryption_key
            + object_number.to_bytes(3, byteorder="little", signed=False)
            + generation_number.to_bytes(2, byteorder="little", signed=False)
        )
        n: int = 5
        if self._v > 1:
            n = int(self._key_length / 8)

        # c) Initialize the MD5 hash function and pass the result of step (b) as input to this function.
        h = hashlib.md5()
        h.update(encryption_key)

        # d) Use the first (n + 5) bytes, up to a maximum of 16, of the output from the MD5 hash as the key for the RC4
        # or AES symmetric key algorithms, along with the string or stream data to be encrypted.
        # If using the AES algorithm, the Cipher Block Chaining (CBC) mode, which requires an initialization vector,
        # is used. The block size parameter is set to 16 bytes, and the initialization vector is a 16-byte random
        # number that is stored as the first 16 bytes of the encrypted stream or string.
        # The output is the encrypted data to be stored in the PDF file.
        n_plus_5: int = min(16, n + 5)
        if isinstance(object, String):
            str_new_content_bytes: bytes = RC4().encrypt(
                h.digest()[0:n_plus_5], object.get_content_bytes()
            )
            # TODO
        if isinstance(object, HexadecimalString):
            hex_str_new_content_bytes: bytes = RC4().encrypt(
                h.digest()[0:n_plus_5], object.get_content_bytes()
            )
            # TODO
        if isinstance(object, Stream):
            object[Name("Bytes")] = RC4().encrypt(
                h.digest()[0:n_plus_5], object["Bytes"]
            )
            return object

        # default
        return object
