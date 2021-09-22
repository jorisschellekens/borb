#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class acts as an aggregator for all BaseTagTransformer implementations.
    Any of the (supported) HTML tags should be able to be transformed by this BaseTagTransformer.
"""
# fmt: off
from borb.toolkit.export.html_to_pdf.read.transformer import \
    Transformer
from borb.toolkit.export.html_to_pdf.read.body.body_tag_transformer import \
    BodyTagTransformer
from borb.toolkit.export.html_to_pdf.read.head.head_tag_transformer import \
    HeadTagTransformer
from borb.toolkit.export.html_to_pdf.read.head.meta_tag_transformer import \
    MetaTagTransformer
from borb.toolkit.export.html_to_pdf.read.head.title_tag_transformer import \
    TitleTagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.h1_tag_transformer import \
    H1TagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.h2_tag_transformer import \
    H2TagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.h3_tag_transformer import \
    H3TagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.h4_tag_transformer import \
    H4TagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.h5_tag_transformer import \
    H5TagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.h6_tag_transformer import \
    H6TagTransformer
from borb.toolkit.export.html_to_pdf.read.heading.hr_tag_transformer import \
    HrTagTransformer
from borb.toolkit.export.html_to_pdf.read.html.html_tag_transformer import \
    HTMLTagTransformer
from borb.toolkit.export.html_to_pdf.read.image.img_tag_transformer import \
    ImgTagTransformer
from borb.toolkit.export.html_to_pdf.read.list.li_tag_transformer import \
    LiTagTransformer
from borb.toolkit.export.html_to_pdf.read.list.ol_tag_transformer import \
    OlTagTransformer
from borb.toolkit.export.html_to_pdf.read.list.ul_tag_transformer import \
    UlTagTransformer
from borb.toolkit.export.html_to_pdf.read.structure.address_tag_transformer import \
    AddressTagTransformer
from borb.toolkit.export.html_to_pdf.read.structure.main_tag_transformer import \
    MainTagTransformer
from borb.toolkit.export.html_to_pdf.read.structure.section_tag_transformer import \
    SectionTagTransformer
from borb.toolkit.export.html_to_pdf.read.table.table_tag_transformer import \
    TableTagTransformer
from borb.toolkit.export.html_to_pdf.read.table.tbody_tag_transformer import \
    TBodyTagTransformer
from borb.toolkit.export.html_to_pdf.read.table.td_tag_transformer import \
    TdTagTransformer
from borb.toolkit.export.html_to_pdf.read.table.th_tag_transformer import \
    ThTagTransformer
from borb.toolkit.export.html_to_pdf.read.table.tr_tag_transformer import \
    TrTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.a_tag_transformer import \
    ATagTransformer
from borb.toolkit.export.html_to_pdf.read.text.abbr_tag_transformer import \
    AbbrTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.bold.b_tag_transformer import \
    BTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.bold.strong_tag_transformer import \
    StrongTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.br_tag_transformer import \
    BrTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.code_tag_transformer import \
    CodeTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.italic.em_tag_transformer import \
    EmTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.italic.i_tag_transformer import \
    ITagTransformer
from borb.toolkit.export.html_to_pdf.read.text.mark_tag_transformer import \
    MarkTagTransformer
from borb.toolkit.export.html_to_pdf.read.text.p_tag_transformer import \
    PTagTransformer

# fmt: on


class AnyTagTransformer(Transformer):
    """
    This class acts as an aggregator for all BaseTagTransformer implementations.
    Any of the (supported) HTML tags should be able to be transformed by this BaseTagTransformer.
    """

    def __init__(self):
        super(AnyTagTransformer, self).__init__()
        self.add_child(HTMLTagTransformer())

        # head
        self.add_child(HeadTagTransformer())
        self.add_child(MetaTagTransformer())
        self.add_child(TitleTagTransformer())

        # body
        self.add_child(BodyTagTransformer())

        # heading
        self.add_child(H1TagTransformer())
        self.add_child(H2TagTransformer())
        self.add_child(H3TagTransformer())
        self.add_child(H4TagTransformer())
        self.add_child(H5TagTransformer())
        self.add_child(H6TagTransformer())
        self.add_child(HrTagTransformer())

        # bold
        self.add_child(BTagTransformer())
        self.add_child(StrongTagTransformer())

        # special formatting
        self.add_child(BrTagTransformer())
        self.add_child(AbbrTagTransformer())
        self.add_child(MarkTagTransformer())
        self.add_child(CodeTagTransformer())

        # italic
        self.add_child(ITagTransformer())
        self.add_child(EmTagTransformer())

        # link
        self.add_child(ATagTransformer())

        # paragraph
        self.add_child(PTagTransformer())

        # list
        self.add_child(OlTagTransformer())
        self.add_child(UlTagTransformer())
        self.add_child(LiTagTransformer())

        # table
        self.add_child(TableTagTransformer())
        self.add_child(TBodyTagTransformer())
        self.add_child(TrTagTransformer())
        self.add_child(ThTagTransformer())
        self.add_child(TdTagTransformer())

        # image
        self.add_child(ImgTagTransformer())

        # structure elements
        self.add_child(MainTagTransformer())
        self.add_child(SectionTagTransformer())
        self.add_child(AddressTagTransformer())
