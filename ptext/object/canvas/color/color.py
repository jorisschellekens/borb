class PDFColor(object):
    def to_rgb(self) -> "PDFColor":
        pass


class RGBColor(PDFColor):
    def __init__(self, r: float, g: float, b: float):
        self.red = r
        self.green = g
        self.blue = b

    def to_rgb(self):
        return self

    def __deepcopy__(self, memodict={}):
        return RGBColor(self.red, self.green, self.blue)


class CMYKColor(PDFColor):
    def __init__(self, c: float, m: float, y: float, k: float):
        self.cyan = c
        self.magenta = m
        self.yellow = y
        self.key = k

    def to_rgb(self) -> "PDFColor":
        r = (1 - self.cyan) * (1 - self.key)
        g = (1 - self.magenta) * (1 - self.key)
        b = (1 - self.yellow) * (1 - self.key)
        return RGBColor(r, g, b)

    def __deepcopy__(self, memodict={}):
        return CMYKColor(self.cyan, self.magenta, self.yellow, self.key)


class GrayColor(PDFColor):
    def __init__(self, g: float):
        self.gray_level = g

    def to_rgb(self) -> "PDFColor":
        # 0 represents completely black
        # 1 represents white
        return RGBColor(self.gray_level, self.gray_level, self.gray_level)

    def __deepcopy__(self, memodict={}):
        return GrayColor(self.gray_level)
