#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In cryptography, RC4 (Rivest Cipher 4 also known as ARC4 or ARCFOUR meaning Alleged RC4, see below) is a stream cipher.
While it is remarkable for its simplicity and speed in software, multiple vulnerabilities have been discovered in RC4, rendering it insecure.
It is especially vulnerable when the beginning of the output keystream is not discarded, or when nonrandom or related keys are used.
Particularly problematic uses of RC4 have led to very insecure protocols such as WEP.

As of 2015, there is speculation that some state cryptologic agencies may possess the capability to break RC4 when used in the TLS protocol.
IETF has published RFC 7465 to prohibit the use of RC4 in TLS; Mozilla and Microsoft have issued similar recommendations.

A number of attempts have been made to strengthen RC4, notably Spritz, RC4A, VMPC, and RC4+.
"""


class RC4:
    """
    In cryptography, RC4 (Rivest Cipher 4 also known as ARC4 or ARCFOUR meaning Alleged RC4, see below) is a stream cipher.
    While it is remarkable for its simplicity and speed in software, multiple vulnerabilities have been discovered in RC4, rendering it insecure.
    It is especially vulnerable when the beginning of the output keystream is not discarded, or when nonrandom or related keys are used.
    Particularly problematic uses of RC4 have led to very insecure protocols such as WEP.

    As of 2015, there is speculation that some state cryptologic agencies may possess the capability to break RC4 when used in the TLS protocol.
    IETF has published RFC 7465 to prohibit the use of RC4 in TLS; Mozilla and Microsoft have issued similar recommendations.

    A number of attempts have been made to strengthen RC4, notably Spritz, RC4A, VMPC, and RC4+.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._p: int = 0
        self._q: int = 0
        self._state = [n for n in range(256)]

    #
    # PRIVATE
    #

    def _byte_generator(self):
        self._p = (self._p + 1) % 256
        self._q = (self._q + self._state[self._p]) % 256
        self._state[self._p], self._state[self._q] = (
            self._state[self._q],
            self._state[self._p],
        )
        return self._state[(self._state[self._p] + self._state[self._q]) % 256]

    def _set_key(self, key: bytes):
        self._state = [n for n in range(256)]
        self._p = 0
        self._q = 0
        j: int = 0
        for i in range(256):
            if len(key) > 0:
                j = (j + self._state[i] + key[i % len(key)]) % 256
            else:
                j = (j + self._state[i]) % 256
            self._state[i], self._state[j] = self._state[j], self._state[i]

    #
    # PUBLIC
    #

    def encrypt(self, key: bytes, input: bytes):
        """
        This function encrypts a given byte array with a given key,
        returning the encrypted bytes.
        :param key:     the key to be used for encrypting
        :param input:   the input byte array to be encrypted
        :return:        the encrypted bytes
        """
        self._set_key(key)
        return bytes([p ^ self._byte_generator() for p in input])
