import copy

from ptext.primitive.pdf_dictionary import PDFDictionary


class LZWDecode:
    @staticmethod
    def decode_with_parameter_dictionary(
        bytes_in: bytes, decode_params: PDFDictionary = None
    ) -> bytes:

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
                raise ValueError("lzw mal-compressed k: %s" % k)
            bytes_out.extend(entry)

            # Add w+entry[0] to the dictionary.
            dictionary[dict_size] = copy.deepcopy(w).append(entry[0])
            dict_size += 1

            w = entry
        return bytes(bytes_out)
