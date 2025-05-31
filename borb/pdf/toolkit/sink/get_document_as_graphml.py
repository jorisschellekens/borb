#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A sink class that converts a PDF document into a GraphML representation.

The `GetDocumentAsGraphML` class serves as a sink at the end of the PDF processing pipeline
and is responsible for converting the document's structure into a GraphML file. This allows
for visualizing the PDF as a graph, where elements such as text, shapes, or images are
represented as nodes and their relationships as edges.

This conversion enables easy debugging and analysis of the PDF structure, making it useful
for identifying issues in PDF generation or processing. The resulting GraphML file can be
opened with graph editing tools for further inspection and manipulation.

This class does not modify the PDF content but simply extracts its structural relationships
for GraphML representation.
"""
import collections
import pathlib
import typing

from borb.pdf.document import Document
from borb.pdf.primitives import PDFType, stream, name
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.sink.sink import Sink

GraphNodeType = collections.namedtuple(
    "GraphNodeType", ["children", "color", "graph_id", "memory_id", "shape", "text"]
)


class GetDocumentAsGraphML(Sink):
    """
    A sink class that converts a PDF document into a GraphML representation.

    The `GetDocumentAsGraphML` class serves as a sink at the end of the PDF processing pipeline
    and is responsible for converting the document's structure into a GraphML file. This allows
    for visualizing the PDF as a graph, where elements such as text, shapes, or images are
    represented as nodes and their relationships as edges.

    This conversion enables easy debugging and analysis of the PDF structure, making it useful
    for identifying issues in PDF generation or processing. The resulting GraphML file can be
    opened with graph editing tools for further inspection and manipulation.

    This class does not modify the PDF content but simply extracts its structural relationships
    for GraphML representation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, where_to: typing.Union[str, pathlib.Path]):
        """
        Initialize a `GetDocumentAsGraphML` instance.

        The `GetDocumentAsGraphML` class acts as a sink in the PDF processing pipeline, converting
        the document's structure into a GraphML representation. This constructor initializes the
        internal data structures needed to capture and organize PDF elements for graph-based analysis.

        The extracted GraphML representation enables debugging and visualization of the PDF’s structure,
        facilitating the identification of relationships between elements.
        """
        super().__init__()
        self.__document: typing.Optional[Document] = None
        self.__where_to: pathlib.Path = (
            where_to if isinstance(where_to, pathlib.Path) else pathlib.Path(where_to)
        )

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_output(self) -> typing.Any:
        """
        Retrieve the aggregated results from the pipeline.

        This method should be overridden by subclasses to provide the specific output
        collected by the `Sink`. By default, it returns `None`, indicating that no
        aggregation or processing has been implemented.

        :return: The aggregated output from the pipeline, or `None` if not implemented.
        """
        # process using stack
        graph: typing.Dict[int, GraphNodeType] = {}
        todo: typing.List[typing.Tuple[PDFType, PDFType]] = [(None, self.__document)]  # type: ignore[list-item]
        ids_done: typing.Set[int] = set()
        while len(todo) > 0:
            parent_id, node = todo.pop(0)
            if id(node) in ids_done:
                continue
            ids_done.add(id(node))

            # dictionaries
            next_id: typing.Optional[int] = None
            if (
                isinstance(node, dict)
                and not isinstance(node, stream)
                and not isinstance(node, Document)
            ):
                todo += [(id(node), key) for key in node.keys()]
                todo += [(id(key), value) for key, value in node.items()]

                # add node
                next_id = len(graph)
                graph[next_id] = GraphNodeType(
                    graph_id=next_id,
                    memory_id=id(node),
                    text="DICT",
                    shape="RECTANGLE",
                    color="#0B3954",
                    children=[],
                )

            # document
            if isinstance(node, Document):
                todo += [
                    (id(node), key) for key in node.keys() if key not in [name("XRef")]
                ]
                todo += [
                    (id(key), value)
                    for key, value in node.items()
                    if key not in [name("XRef")]
                ]

                # add node
                next_id = len(graph)
                graph[next_id] = GraphNodeType(
                    graph_id=next_id,
                    memory_id=id(node),
                    text="DOC",
                    shape="RECTANGLE",
                    color="#0B3954",
                    children=[],
                )

            # lists
            if isinstance(node, list):
                todo += [(id(node), x) for x in node]

                # add node
                next_id = len(graph)
                graph[next_id] = GraphNodeType(
                    graph_id=next_id,
                    memory_id=id(node),
                    text="LIST",
                    shape="RECTANGLE",
                    color="#0B3954",
                    children=[],
                )

            # primitives
            if (
                isinstance(node, bool)
                or isinstance(node, float)
                or isinstance(node, int)
                or isinstance(node, name)
                or isinstance(node, str)
            ):
                next_id = len(graph)
                graph[next_id] = GraphNodeType(
                    graph_id=next_id,
                    memory_id=id(node),
                    text=str(node),
                    shape="ELLIPSE",
                    color="#F1CD2E",
                    children=[],
                )

            # stream
            if isinstance(node, stream):
                todo += [
                    (id(node), key)
                    for key in node.keys()
                    if key not in ["Bytes", "DecodedBytes"]
                ]
                todo += [
                    (id(key), value)
                    for key, value in node.items()
                    if key not in ["Bytes", "DecodedBytes"]
                ]

                # add node
                next_id = len(graph)
                graph[next_id] = GraphNodeType(
                    graph_id=next_id,
                    memory_id=id(node),
                    text="STREAM",
                    shape="RECTANGLE",
                    color="#0B3954",
                    children=[],
                )

            # link
            parent_node: typing.Optional[GraphNodeType] = None
            if parent_id is not None:
                parent_node = next(
                    iter([v for k, v in graph.items() if v.memory_id == parent_id]),
                    None,
                )
            if parent_node is not None:
                graph[parent_node.graph_id] = GraphNodeType(
                    graph_id=parent_node.graph_id,
                    memory_id=parent_node.memory_id,
                    text=parent_node.text,
                    color=parent_node.color,
                    shape=parent_node.shape,
                    children=parent_node.children + [next_id],
                )

        # build graphml
        # fmt: off
        graphml_str = ""
        graphml_str += """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
        graphml_str += """\n<!-- produced by borb, based on yEd Live 2025 -->"""
        graphml_str += """\n<graphml xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml.html/2.0/ygraphml.xsd " xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:yca="http://www.yworks.com/xml/yfiles-compat-arrows/1.0" xmlns:ycns="http://www.yworks.com/xml/yfiles-compat-node-styles/1.0" xmlns:yjs2="http://www.yworks.com/xml/yfiles-for-html/2.0/xaml" xmlns:demostyle2="http://www.yworks.com/yFilesHTML/demos/FlatDemoStyle/2.0" xmlns:demostyle="http://www.yworks.com/yFilesHTML/demos/FlatDemoStyle/1.0" xmlns:icon-style="http://www.yworks.com/yed-live/icon-style/1.0" xmlns:bpmn="http://www.yworks.com/xml/yfiles-bpmn/2.0" xmlns:demotablestyle="http://www.yworks.com/yFilesHTML/demos/FlatDemoTableStyle/1.0" xmlns:uml="http://www.yworks.com/yFilesHTML/demos/UMLDemoStyle/1.0" xmlns:GraphvizNodeStyle="http://www.yworks.com/yFilesHTML/graphviz-node-style/1.0" xmlns:Vue2jsNodeStyle="http://www.yworks.com/demos/yfiles-vuejs-node-style/1.0" xmlns:Vue3jsNodeStyle="http://www.yworks.com/demos/yfiles-vue-node-style/3.0" xmlns:explorer-style="http://www.yworks.com/data-explorer/1.0" xmlns:yx="http://www.yworks.com/xml/yfiles-common/4.0" xmlns:y="http://www.yworks.com/xml/yfiles-common/3.0" xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/3.0" xmlns:yjs="http://www.yworks.com/xml/yfiles-for-html/3.0/xaml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">"""
        graphml_str += """\n\t<key id="d0" for="node" attr.type="int" attr.name="zOrder" y:attr.uri="http://www.yworks.com/xml/yfiles-z-order/1.0/zOrder"/>"""
        graphml_str += """\n\t<key id="d1" for="node" attr.type="boolean" attr.name="Expanded" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/folding/Expanded">"""
        graphml_str += """\n\t\t<default>true</default>"""
        graphml_str += """\n\t</key>"""
        graphml_str += """\n\t<key id="d2" for="node" attr.type="string" attr.name="url"/>"""
        graphml_str += """\n\t<key id="d3" for="node" attr.type="string" attr.name="description"/>"""
        graphml_str += """\n\t<key id="d4" for="node" attr.name="NodeLabels" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/NodeLabels"/>"""
        graphml_str += """\n\t<key id="d5" for="node" attr.name="NodeGeometry" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/NodeGeometry"/>"""
        graphml_str += """\n\t<key id="d6" for="all" attr.name="UserTags" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/UserTags"/>"""
        graphml_str += """\n\t<key id="d7" for="node" attr.name="NodeStyle" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/NodeStyle"/>"""
        graphml_str += """\n\t<key id="d8" for="node" attr.name="NodeViewState" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/folding/1.1/NodeViewState"/>"""
        graphml_str += """\n\t<key id="d9" for="edge" attr.type="string" attr.name="url"/>"""
        graphml_str += """\n\t<key id="d10" for="edge" attr.type="string" attr.name="description"/>"""
        graphml_str += """\n\t<key id="d11" for="edge" attr.name="EdgeLabels" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/EdgeLabels"/>"""
        graphml_str += """\n\t<key id="d12" for="edge" attr.name="EdgeGeometry" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/EdgeGeometry"/>"""
        graphml_str += """\n\t<key id="d13" for="edge" attr.name="EdgeStyle" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/EdgeStyle"/>"""
        graphml_str += """\n\t<key id="d14" for="edge" attr.name="EdgeViewState" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/folding/1.1/EdgeViewState"/>"""
        graphml_str += """\n\t<key id="d15" for="port" attr.name="PortLabels" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/PortLabels"/>"""
        graphml_str += """\n\t<key id="d16" for="port" attr.name="PortLocationParameter" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/PortLocationParameter">"""
        graphml_str += """\n\t\t<default>"""
        graphml_str += """\n\t\t\t<x:Static Member="y:FreeNodePortLocationModel.NodeCenterAnchored"/>"""
        graphml_str += """\n\t\t</default>"""
        graphml_str += """\n\t</key>"""
        graphml_str += """\n\t<key id="d17" for="port" attr.name="PortStyle" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/PortStyle">"""
        graphml_str += """\n\t\t<default>"""
        graphml_str += """\n\t\t\t<x:Static Member="y:VoidPortStyle.Instance"/>"""
        graphml_str += """\n\t\t</default>"""
        graphml_str += """\n\t</key>"""
        graphml_str += """\n\t<key id="d18" for="port" attr.name="PortViewState" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/folding/1.1/PortViewState"/>"""
        graphml_str += """\n\t<key id="d19" attr.name="SharedData" y:attr.uri="http://www.yworks.com/xml/yfiles-common/2.0/SharedData"/>"""
        # fmt: on

        # shared data
        # fmt: off
        graphml_str += """\n\t<data key="d19">"""
        graphml_str += """\n\t\t<y:SharedData>"""
        graphml_str += """\n\t\t\t<yx:ExteriorNodeLabelModel x:Key="1" Margins="5"/>"""
        graphml_str += """\n\t\t\t<yx:CompositeLabelModelParameter x:Key="2">"""
        graphml_str += """\n\t\t\t\t<yx:CompositeLabelModelParameter.Parameter>"""
        graphml_str += """\n\t\t\t\t\t<yx:ExteriorNodeLabelModelParameter Position="Bottom" Model="{y:GraphMLReference 1}"/>"""
        graphml_str += """\n\t\t\t\t</yx:CompositeLabelModelParameter.Parameter>"""
        graphml_str += """\n\t\t\t\t<yx:CompositeLabelModelParameter.Model>"""
        graphml_str += """\n\t\t\t\t\t<yx:CompositeLabelModel>"""
        graphml_str += """\n\t\t\t\t\t\t<yx:CompositeLabelModel.Models>"""
        graphml_str += """\n\t\t\t\t\t\t\t<yx:CompositeLabelModelModelPair Model="{y:GraphMLReference 1}"/>"""
        graphml_str += """\n\t\t\t\t\t\t\t<yx:CompositeLabelModelModelPair>"""
        graphml_str += """\n\t\t\t\t\t\t\t\t<yx:CompositeLabelModelModelPair.Model>"""
        graphml_str += """\n\t\t\t\t\t\t\t\t\t<yx:InteriorNodeLabelModel/>"""
        graphml_str += """\n\t\t\t\t\t\t\t\t</yx:CompositeLabelModelModelPair.Model>"""
        graphml_str += """\n\t\t\t\t\t\t\t</yx:CompositeLabelModelModelPair>"""
        graphml_str += """\n\t\t\t\t\t\t\t<yx:CompositeLabelModelModelPair Model="{x:Static yx:FreeNodeLabelModel.Instance}"/>"""
        graphml_str += """\n\t\t\t\t\t\t</yx:CompositeLabelModel.Models>"""
        graphml_str += """\n\t\t\t\t\t</yx:CompositeLabelModel>"""
        graphml_str += """\n\t\t\t\t</yx:CompositeLabelModelParameter.Model>"""
        graphml_str += """\n\t\t\t</yx:CompositeLabelModelParameter>"""
        graphml_str += """\n\t\t\t<yjs:Font x:Key="3" fontSize="12" lineSpacing="0.2"/>"""
        graphml_str += """\n\t\t\t<yjs:Stroke x:Key="4">"""
        graphml_str += """\n\t\t\t\t<yjs:Stroke.fill>"""
        graphml_str += """\n\t\t\t\t\t<yjs:CssFill cssString="#663800"/>"""
        graphml_str += """\n\t\t\t\t</yjs:Stroke.fill>"""
        graphml_str += """\n\t\t\t</yjs:Stroke>"""
        graphml_str += """\n\t\t</y:SharedData>"""
        graphml_str += """\n\t</data>"""
        # fmt: on

        # persist graph (header)
        # fmt: off
        graphml_str += """\n\t<graph id="G" edgedefault="directed">"""
        graphml_str += """\n\t\t<data key="d6">"""
        graphml_str += """\n\t\t\t<y:Json>{"version":"2.0.0","origin":"yed-live","theme":{"name":"light","version":"1.0.0"}}</y:Json>"""
        graphml_str += """\n\t\t</data>"""
        # fmt: on

        # persist nodes
        for k, v in graph.items():
            # fmt: off
            graphml_str += f"""\n\t\t<node id="n{k}">"""
            graphml_str += """\n\t\t\t<data key="d0">1</data>"""
            graphml_str += """\n\t\t\t<data key="d4">"""
            graphml_str += """\n\t\t\t\t<x:List>"""
            graphml_str += f"""\n\t\t\t\t\t<y:Label Text="{v.text}" LayoutParameter="{{y:GraphMLReference 2}}">"""
            graphml_str += """\n\t\t\t\t\t\t<y:Label.Style>"""
            graphml_str += """\n\t\t\t\t\t\t\t<yjs:LabelStyle backgroundFill="WHITE" verticalTextAlignment="CENTER" horizontalTextAlignment="CENTER" backgroundStroke="WHITE" font="{y:GraphMLReference 3}"/>"""
            graphml_str += """\n\t\t\t\t\t\t</y:Label.Style>"""
            graphml_str += """\n\t\t\t\t\t</y:Label>"""
            graphml_str += """\n\t\t\t\t</x:List>"""
            graphml_str += """\n\t\t\t</data>"""
            graphml_str += """\n\t\t\t<data key="d5">"""
            graphml_str += """\n\t\t\t\t<y:RectD X="1329.25" Y="394.25" Width="60" Height="60"/>"""
            graphml_str += """\n\t\t\t</data>"""
            graphml_str += """\n\t\t\t<data key="d7">"""
            graphml_str += f"""\n\t\t\t\t<yjs:ShapeNodeStyle stroke="{{y:GraphMLReference 4}}" fill="{v.color}" shape="{v.shape}"/>"""
            graphml_str += """\n\t\t\t</data>"""
            graphml_str += f"""\n\t\t\t<port name="p{k}"/>"""
            graphml_str += """\n\t\t</node>"""
            # fmt: on

        # persist edges
        for k0, v0 in graph.items():
            for k1 in v0.children:
                # fmt: off
                graphml_str += f"""\n\t\t<edge id="e{len(graph)*k0+k1}" source="n{k0}" target="n{k1}" sourceport="p{k0}" targetport="p{k1}">"""
                graphml_str += """\n\t\t\t<data key="d13">"""
                graphml_str += """\n\t\t\t\t<yjs:PolylineEdgeStyle stroke="#FF000000">"""
                graphml_str += """\n\t\t\t\t\t<yjs:PolylineEdgeStyle.targetArrow>"""
                graphml_str += """\n\t\t\t\t\t\t<yjs:Arrow stroke="BLACK" fill="BLACK" cropLength="1" lengthScale="0.75" widthScale="0.75" type="TRIANGLE"/>"""
                graphml_str += """\n\t\t\t\t\t</yjs:PolylineEdgeStyle.targetArrow>"""
                graphml_str += """\n\t\t\t\t\t<yjs:PolylineEdgeStyle.sourceArrow>"""
                graphml_str += """\n\t\t\t\t\t\t<yjs:Arrow stroke="BLACK" fill="BLACK" type="NONE"/>"""
                graphml_str += """\n\t\t\t\t\t</yjs:PolylineEdgeStyle.sourceArrow>"""
                graphml_str += """\n\t\t\t\t</yjs:PolylineEdgeStyle>"""
                graphml_str += """\n\t\t\t</data>"""
                graphml_str += """\n\t\t</edge>"""
                # fmt: on

        # end file
        graphml_str += """\n\t</graph>"""
        graphml_str += """\n</graphml>"""

        # write
        with open(self.__where_to, "w") as fh:
            fh.write(graphml_str)

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        self.__document = event.get_document()
