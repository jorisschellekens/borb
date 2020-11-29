import copy

from ptext.exception.pdf_exception import PDFSyntaxError


class LZWDecode:
    """
    Decompresses data encoded using the LZW (Lempel-Ziv-
    Welch) adaptive compression method, reproducing the original
    text or binary data.
    """

    @staticmethod
    def decode(bytes_in: bytes) -> bytes:
        """
        Decompresses data encoded using the LZW (Lempel-Ziv-
        Welch) adaptive compression method
        """

        # Build the dictionary.
        dict_size = 256
        dictionary = {i: bytearray() for i in range(dict_size)}
        for k, v in dictionary.items():
            v.append(k)

        # use bytearray, otherwise this becomes O(N^2)
        # due to concatenation in a loop
        bytes_out = bytearray()
        w = bytearray()
        w.append(bytes_in[0])
        bytes_out.append(bytes_in[0])

        for i in range(1, len(bytes_in)):
            k = bytes_in[i]
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = copy.deepcopy(w).append(w[0])
            else:
                raise PDFSyntaxError("malformed lzw byte stream")
            bytes_out.extend(entry)

            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = copy.deepcopy(w).append(entry[0])
            dict_size += 1

            w = entry
        return bytes(bytes_out)
