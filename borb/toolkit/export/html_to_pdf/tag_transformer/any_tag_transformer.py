#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class acts as an aggregator for all BaseTagTransformer implementations.
    Any of the (supported) HTML tags should be able to be transformed by this BaseTagTransformer.
"""
# fmt: off
from borb.toolkit.export.html_to_pdf.tag_transformer.base_tag_transformer import \
    BaseTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.body.body_tag_transformer import \
    BodyTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.head.head_tag_transformer import \
    HeadTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.head.meta_tag_transformer import \
    MetaTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.head.title_tag_transformer import \
    TitleTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.h1_tag_transformer import \
    H1TagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.h2_tag_transformer import \
    H2TagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.h3_tag_transformer import \
    H3TagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.h4_tag_transformer import \
    H4TagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.h5_tag_transformer import \
    H5TagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.h6_tag_transformer import \
    H6TagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.heading.hr_tag_transformer import \
    HrTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.html_tag_transformer import \
    HTMLTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.image.img_tag_transformer import \
    ImgTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.list.li_tag_transformer import \
    LiTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.list.ol_tag_transformer import \
    OlTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.list.ul_tag_transformer import \
    UlTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.structure.address_tag_transformer import \
    AddressTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.structure.main_tag_transformer import \
    MainTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.structure.section_tag_transformer import \
    SectionTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.table.table_tag_transformer import \
    TableTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.table.tbody_tag_transformer import \
    TBodyTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.table.td_tag_transformer import \
    TdTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.table.th_tag_transformer import \
    ThTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.table.tr_tag_transformer import \
    TrTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.a_tag_transformer import \
    ATagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.abbr_tag_transformer import \
    AbbrTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.bold.b_tag_transformer import \
    BTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.bold.strong_tag_transformer import \
    StrongTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.br_tag_transformer import \
    BrTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.code_tag_transformer import \
    CodeTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.italic.em_tag_transformer import \
    EmTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.italic.i_tag_transformer import \
    ITagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.mark_tag_transformer import \
    MarkTagTransformer
from borb.toolkit.export.html_to_pdf.tag_transformer.text.p_tag_transformer import \
    PTagTransformer

# fmt: on


class AnyTagTransformer(BaseTagTransformer):
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
