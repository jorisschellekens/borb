from ptext.io.tokenize.types.pdf_object import PDFObject


class PDFArray(PDFObject):
    """
    An array object is a one-dimensional collection of objects arranged sequentially. Unlike arrays in many other
    computer languages, PDF arrays may be heterogeneous; that is, an array’s elements may be any combination
    of numbers, strings, dictionaries, or any other objects, including other arrays. An array may have zero
    elements.
    """

    def __init__(self):
        super().__init__()
        self.list = []

    def append(self, object: PDFObject):
        self.list.append(object)
        return self

    def __getitem__(self, item):
        return self.list[item]

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return "[" + "".join([str(x) + "," for x in self.list])[:-1] + "]"
