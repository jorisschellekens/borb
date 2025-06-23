#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visitor class for converting specific string objects to name objects in a PDF document.

`ReplaceStrByNameVisitor` is a preparatory step in the PDF serialization
process, ensuring that dictionary keys or values that require name objects
(as defined by the PDF specification) are properly set. Users interacting
with the PDF structure may inadvertently assign regular strings to such
fields, as they manipulate the PDF document similarly to a JSON-like
structure.

This visitor iterates through the document, identifying and replacing
string objects with name objects wherever required. This automatic conversion
helps maintain PDF format compliance without requiring users to manually
distinguish between string and name object types.
"""
import typing

from borb.pdf.document import Document
from borb.pdf.primitives import PDFType, name
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.write_new.write_new_visitor import WriteNewVisitor


class ReplaceStrByNameVisitor(WriteNewVisitor):
    """
    Visitor class for converting specific string objects to name objects in a PDF document.

    `ReplaceStrByNameVisitor` is a preparatory step in the PDF serialization
    process, ensuring that dictionary keys or values that require name objects
    (as defined by the PDF specification) are properly set. Users interacting
    with the PDF structure may inadvertently assign regular strings to such
    fields, as they manipulate the PDF document similarly to a JSON-like
    structure.

    This visitor iterates through the document, identifying and replacing
    string objects with name objects wherever required. This automatic conversion
    helps maintain PDF format compliance without requiring users to manually
    distinguish between string and name object types.
    """

    # fmt: off
    __KNOWN_NAMES: typing.List[str] = [
        'A', 'A85', 'AA', 'AC', 'ADBE', 'AESV2', 'AESV3', 'AHx', 'AIS', 'AP', 'AS', 'ASCII85Decode', 'ASCIIHexDecode',
        'AbsoluteColorimetric', 'AcroForm', 'Action', 'Activation', 'ActualText', 'Adobe.PPKLite', 'Adobe.PPKMS',
        'Adobe.PubSec', 'AllPages', 'Alt', 'Alternate', 'And', 'Animation', 'Annot', 'Annots', 'AntiAlias',
        'AppDefault', 'Art', 'ArtBox', 'Ascent', 'Asset', 'Assets', 'AuthEvent', 'Author',
        'adbe.pkcs7.detached', 'adbe.pkcs7.s4', 'adbe.pkcs7.s5', 'adbe.pkcs7.sha1', 'adbe.x509.rsa_sha1',
        'B', 'BBox', 'BC', 'BG', 'BM', 'BS', 'Background', 'BaseEncoding', 'BaseFont', 'BaseVersion', 'BibEntry',
        'BigFive', 'Binding', 'BindingMaterialName', 'BitsPerComponent', 'BitsPerSample', 'Bl', 'BlackIs1',
        'BlackPoint', 'BleedBox', 'Blinds', 'BlockQuote', 'Border', 'Bounds', 'Box', 'Btn', 'ByteRange',
        'C', 'C0', 'C1', 'CA', 'CCITTFaxDecode', 'CF', 'CFM', 'CI', 'CIDFontType0', 'CIDFontType2', 'CIDSet',
        'CIDSystemInfo', 'CIDToGIDMap', 'CMD', 'CO', 'CS', 'CYX', 'CalGray', 'CalRGB', 'CapHeight', 'Caption',
        'Catalog', 'Category', 'Center', 'CenterWindow', 'Cert', 'Ch', 'CharProcs', 'CheckSum', 'Circle', 'Cloud',
        'Code', 'Collection', 'CollectionField', 'CollectionItem', 'CollectionSchema', 'CollectionSort',
        'CollectionSubitem', 'ColorSpace', 'Colors', 'Columns', 'Condition', 'Configuration', 'Configurations',
        'ContactInfo', 'Content', 'Contents', 'Coords', 'Count', 'Courier', 'Courier-Bold', 'Courier-BoldOblique',
        'Courier-Oblique', 'CreationDate', 'Creator', 'CreatorInfo', 'CropBox', 'Crypt', 'CuePoint', 'CuePoints',
        'ca',
        'D', 'DA', 'DC', 'DCS', 'DCTDecode', 'DL', 'DP', 'DR', 'DS', 'DV', 'DW', 'Data', 'Deactivation', 'Decode',
        'DecodeParms', 'Default', 'DefaultCMYK', 'DefaultCryptFilter', 'DefaultGray', 'DefaultRGB', 'Desc',
        'DescendantFonts', 'Descent', 'Dest', 'DestOutputProfile', 'Dests', 'DeviceCMYK', 'DeviceGray', 'DeviceRGB',
        'Di', 'Differences', 'Direction', 'DisplayDocTitle', 'Dissolve', 'Div', 'Dm', 'DocMDP', 'DocOpen', 'Document',
        'Domain', 'Duplex', 'DuplexFlipLongEdge', 'DuplexFlipShortEdge', 'Dur',
        'E', 'EF', 'EFF', 'EFOpen', 'EPSG', 'EarlyChange', 'Embedded', 'EmbeddedFile', 'EmbeddedFiles', 'Encode',
        'EncodedByteAlign', 'Encoding', 'Encrypt', 'EncryptMetadata', 'EndOfBlock', 'EndOfLine', 'Event', 'Export',
        'ExportState', 'ExtGState', 'Extend', 'ExtensionLevel', 'Extensions',
        'F', 'FB', 'FD', 'FDF', 'FDecodeParms', 'FFilter', 'FG', 'FRM', 'FS', 'FT', 'Far', 'Ff', 'Fields', 'Figure',
        'FileAttachment', 'Filespec', 'Filter', 'First', 'FirstChar', 'FirstPage', 'Fit', 'FitB', 'FitBH', 'FitBV',
        'FitH', 'FitR', 'FitV', 'FitWindow', 'Fl', 'Flags', 'Flash', 'FlashVars', 'FlateDecode', 'Fo', 'Font',
        'FontBBox', 'FontDescriptor', 'FontFile', 'FontFile2', 'FontFile3', 'FontMatrix', 'FontName', 'Foreground',
        'Form', 'FormType', 'Formula', 'FreeText', 'FullScreen', 'Function', 'FunctionType', 'Functions',
        'GBK', 'GCS', 'GEO', 'GEOGCS', 'GPTS', 'GTS_PDFA1', 'GTS_PDFX', 'GTS_PDFXVersion', 'Gamma', 'Glitter', 'GoTo',
        'GoToE', 'GoToR', 'Group',
        'H', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HAlign', 'HF', 'HOffset', 'Height', 'Helv', 'Helvetica',
        'Helvetica-Bold', 'Helvetica-BoldOblique', 'Helvetica-Oblique', 'Hid', 'Hide', 'HideMenubar', 'HideToolbar',
        'HideWindowUI', 'Highlight',
        'I', 'ICCBased', 'ID', 'IF', 'IRT', 'ITXT', 'IX', 'Identity', 'Image', 'ImageB', 'ImageC', 'ImageI',
        'ImageMask', 'ImportData', 'Ind', 'Index', 'Indexed', 'Info', 'Ink', 'InkList', 'Instances', 'Intent',
        'Interpolate', 'IsMap', 'ItalicAngle',
        'JBIG2Decode', 'JBIG2Globals', 'JPXDecode', 'JS', 'JavaScript',
        'K', 'Keywords', 'Kids',
        'L', 'L2R', 'LBody', 'LI', 'LPTS', 'LZWDecode', 'Lang', 'Language', 'Last', 'LastChar', 'LastPage', 'Launch',
        'Lbl', 'Length', 'Length1', 'Limits', 'Line', 'Linear', 'Link', 'ListMode', 'Location', 'Lock', 'Locked',
        'M', 'MCID', 'MCR', 'MK', 'MMType1', 'MacExpertEncoding', 'MacRomanEncoding', 'MarkInfo', 'Marked', 'Mask',
        'Material', 'Matrix', 'Max', 'MaxLen', 'Measure', 'MediaBox', 'Metadata', 'Min', 'ModDate',
        'max', 'min',
        'n0', 'n1', 'n2', 'n3', 'n4',
        'N', 'NM', 'Name', 'Named', 'Names', 'Navigation', 'NavigationPane', 'Near', 'NeedAppearances', 'NewWindow',
        'Next', 'NextPage', 'NonFullScreenPageMode', 'NonStruct', 'None', 'Not', 'Note', 'NumCopies', 'NumberFormat',
        'Nums',
        'O', 'OBJR', 'OC', 'OCG', 'OCGs', 'OCMD', 'OCProperties', 'OE', 'OFF', 'ON', 'OP', 'OPM', 'Obj', 'ObjStm',
        'Off', 'OneColumn', 'Open', 'OpenAction', 'Opt', 'Or', 'Order', 'Ordering', 'Org', 'Oscillating', 'Outlines',
        'OutputCondition', 'OutputConditionIdentifier', 'OutputIntent', 'OutputIntents',
        'op',
        'P', 'PC', 'PDF', 'PDFDocEncoding', 'PDU', 'PI', 'PO', 'PROJCS', 'PS', 'PV', 'Page', 'PageElement',
        'PageLabels', 'PageLayout', 'PageMode', 'Pages', 'PaintType', 'Panose', 'Params', 'Parent', 'ParentTree',
        'ParentTreeNextKey', 'Part', 'PassContextClick', 'Pattern', 'PatternType', 'Perceptual', 'Perms', 'Pg',
        'PickTrayByPDFSize', 'PlayCount', 'Polygon', 'Polyline', 'Popup', 'Position', 'Predictor', 'Preferred',
        'Presentation', 'PreserveRB', 'Prev', 'PrevPage', 'Print', 'PrintArea', 'PrintClip', 'PrintPageRange',
        'PrintScaling', 'PrintState', 'Private', 'ProcSet', 'Producer', 'Properties', 'PtData',
        'Q', 'QuadPoints', 'Quote',
        'R', 'R2L', 'RBGroups', 'RC', 'RD', 'RI', 'RL', 'RT', 'RV', 'Range', 'Reason', 'Recipients', 'Rect',
        'Reference', 'Registry', 'RegistryName', 'RelativeColorimetric', 'Rendition', 'ResetForm', 'Resources',
        'RichMedia', 'RichMediaActivation', 'RichMediaAnimation', 'RichMediaCommand', 'RichMediaConfiguration',
        'RichMediaContent', 'RichMediaDeactivation', 'RichMediaExecute', 'RichMediaInstance', 'RichMediaParams',
        'RichMediaPosition', 'RichMediaPresentation', 'RichMediaSettings', 'RichMediaWindow', 'RoleMap', 'Root',
        'Rotate', 'Rows', 'Ruby', 'RunLengthDecode',
        'S', 'SMask', 'SS', 'SV', 'SW', 'Saturation', 'Schema', 'Screen', 'Scripts', 'Sect', 'Separation',
        'SetOCGState', 'Settings', 'Shading', 'ShadingType', 'Shift-JIS', 'Sig', 'SigFlags', 'SigRef', 'Simplex',
        'SinglePage', 'Size', 'Sort', 'Sound', 'Span', 'Speed', 'Split', 'Square', 'Squiggly', 'St', 'Stamp',
        'Standard', 'State', 'StdCF', 'StemV', 'StmF', 'StrF', 'StrikeOut', 'StructElem', 'StructParent',
        'StructParents', 'StructTreeRoot', 'Style', 'SubFilter', 'Subject', 'SubmitForm', 'Subtype', 'Supplement',
        'Symbol',
        'T', 'TA', 'TBody', 'TD', 'TFoot', 'TH', 'THead', 'TI', 'TK', 'TM', 'TOC', 'TOCI', 'TP', 'TR', 'TU', 'Table',
        'Tabs', 'Text', 'Threads', 'Thumb', 'TilingType', 'Time', 'Title', 'ToUnicode', 'Toggle', 'Toolbar', 'Trans',
        'TransformMethod', 'TransformParams', 'Transparency', 'Transparent', 'Trapped', 'TrimBox', 'TrueType', 'Ttl',
        'TwoColumnLeft', 'TwoColumnRight', 'TwoPageLeft', 'TwoPageRight', 'Tx', 'Type', 'Type0', 'Type1', 'Type3',
        '-Bold', '-BoldItalic', '-Italic', '-Roman',
        'U', 'UE', 'UF', 'UHC', 'UR', 'UR3', 'URI', 'URL', 'Underline', 'Usage', 'UseAttachments', 'UseNone', 'UseOC',
        'UseOutlines', 'UseThumbs', 'User', 'UserProperties', 'UserUnit',
        'V', 'V2', 'VAlign', 'VE', 'VOffset', 'VP', 'VeriSign.PPKVS', 'Version', 'Vertices', 'Video', 'View',
        'ViewArea', 'ViewClip', 'ViewState', 'ViewerPreferences', 'Viewport', 'Views', 'VisiblePages',
        'W', 'W2', 'WC', 'WKT', 'WP', 'WS', 'Warichu', 'WhitePoint', 'Widget', 'Width', 'Widths', 'Win',
        'WinAnsiEncoding', 'Window', 'Windowed', 'Wipe',
        'X', 'XA', 'XD', 'XFA', 'XML', 'XObject', 'XPTS', 'XRef', 'XRefStm', 'XStep', 'XYZ',
        'YStep',
        'ZaDb', 'ZapfDingbats', 'Zoom',
        '3D',
    ]
    # fmt: on

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None) -> None:
        """
        Initialize a new instance of `ReplaceStrByNameVisitor`.

        This constructor sets up the visitor to perform name-object replacement in a
        PDF document. It accepts an optional root `NodeVisitor` to provide context
        within a visitor hierarchy. An internal flag, `__has_been_used`, tracks whether
        this visitor has been applied, enabling it to operate only once per session.

        :param root: An optional `NodeVisitor` instance representing the root of the visitor
                     hierarchy, often used to manage shared context or data among multiple
                     visitors. Defaults to `None`.
        """
        super().__init__(root=root)
        self.__has_been_used: bool = False

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def visit(self, node: typing.Any) -> bool:
        """
        Traverse the PDF document tree using the visitor pattern.

        This method is called when a node does not have a specialized handler.
        Subclasses can override this method to provide default behavior or logging
        for unsupported nodes. If any operation is performed on the node (e.g.,
        writing or persisting), the method returns `True`. Otherwise, it returns
        `False` to indicate that the visitor did not process the node.

        :param node:    the node (PDFType) to be processed
        :return:        True if the visitor processed the node False otherwise
        """
        # check whether this is a document
        if not isinstance(node, Document):
            return False
        if "XRef" not in node:
            return False
        if len(node["XRef"]) == 0:
            return False
        if "Trailer" not in node:
            return False
        if self.__has_been_used:
            return False

        for xref_entry in node["XRef"]:
            obj: typing.Optional[PDFType] = xref_entry.get_referenced_object()
            if obj is None:
                continue

            # IF the object is a dictionary
            # THEN ensure all keys are names
            if isinstance(obj, dict):
                obj = {
                    (name(k) if not isinstance(k, name) else k): v
                    for k, v in obj.items()
                }

        # delegate
        self.__has_been_used = True
        self.go_to_root_and_visit(node)

        # return
        return True
