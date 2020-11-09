import copy

from ptext.object.canvas.color.color import RGBColor
from ptext.object.canvas.geometry.matrix import Matrix


class CanvasGraphicsState:
    def __init__(self):
        self.ctm = Matrix.identity_matrix()
        self.text_matrix = Matrix.identity_matrix()
        self.text_line_matrix = Matrix.identity_matrix()
        self.text_rise = 0
        self.character_spacing = 0
        self.word_spacing = 0
        self.horizontal_scaling = 100
        self.leading = 0
        self.font = None
        self.font_size = None
        self.clipping_path = None
        self.non_stroke_color_space = None
        self.non_stroke_color = RGBColor(0, 0, 0)
        self.stroke_color_space = None
        self.stroke_color = RGBColor(0, 0, 0)
        self.line_width = 1
        self.line_cap = None
        self.line_join = None
        self.miter_limit = 10
        self.dash_pattern = None
        self.rendering_intent = None
        self.stroke_adjustment = None
        self.blend_mode = None
        self.soft_mask = None
        self.alpha_constant = None
        self.alpha_source = None

    def __deepcopy__(self, memodict={}):
        out = CanvasGraphicsState()
        out.ctm = copy.deepcopy(self.ctm)
        out.text_matrix = copy.deepcopy(self.text_matrix)
        out.text_line_matrix = copy.deepcopy(self.text_line_matrix)
        out.text_rise = self.text_rise
        out.character_spacing = self.character_spacing
        out.word_spacing = self.word_spacing
        out.horizontal_scaling = self.horizontal_scaling
        out.leading = self.leading
        out.font = copy.deepcopy(self.font)
        out.font_size = self.font_size
        # out.clipping_path = None
        # out.non_stroke_color_space = None
        out.non_stroke_color = copy.deepcopy(self.non_stroke_color)
        # out.stroke_color_space = None
        out.stroke_color = copy.deepcopy(self.stroke_color)
        out.line_width = self.line_width
        # self.line_cap = None
        # self.line_join = None
        out.miter_limit = self.miter_limit
        # self.dash_pattern = None
        # self.rendering_intent = None
        # self.stroke_adjustment = None
        # self.blend_mode = None
        # self.soft_mask = None
        # self.alpha_constant = None
        # self.alpha_source = None
        return out
