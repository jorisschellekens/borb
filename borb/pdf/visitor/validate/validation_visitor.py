#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A visitor implementation for validating a PDF document against its declared conformance level.

This class operates within the Visitor Pattern and is responsible for:
- Determining the conformance level of the PDF document (e.g., PDF/A, PDF/UA, etc.).
- Gathering all relevant `ConformanceCheck` instances using `ConformanceChecks`.
- Traversing the document structure and executing checks on applicable PDF nodes.
- Reporting violations and optionally interacting with a root visitor.

This visitor is intended to be applied once per document and tracks its usage to prevent reuse.

It integrates with the `NodeVisitor` hierarchy and is designed to be composable with other visitors,
using delegation to a `root` visitor when necessary.
"""
import typing

from borb.pdf import Document
from borb.pdf.primitives import PDFType, reference
from borb.pdf.visitor.node_visitor import NodeVisitor
from borb.pdf.visitor.validate.conformance_check import ConformanceCheck
from borb.pdf.visitor.validate.conformance_checks import ConformanceChecks


class ValidationVisitor(NodeVisitor):
    """
    A visitor implementation for validating a PDF document against its declared conformance level.

    This class operates within the Visitor Pattern and is responsible for:
    - Determining the conformance level of the PDF document (e.g., PDF/A, PDF/UA, etc.).
    - Gathering all relevant `ConformanceCheck` instances using `ConformanceChecks`.
    - Traversing the document structure and executing checks on applicable PDF nodes.
    - Reporting violations and optionally interacting with a root visitor.

    This visitor is intended to be applied once per document and tracks its usage to prevent reuse.

    It integrates with the `NodeVisitor` hierarchy and is designed to be composable with other visitors,
    using delegation to a `root` visitor when necessary.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, root: typing.Optional[NodeVisitor] = None):
        """
        Initialize the ValidationVisitor.

        This constructor sets up the visitor for PDF conformance validation. An optional
        root visitor can be passed in to enable delegation of certain operations (e.g., reference
        resolution or generic visitation logic).

        :param root: An optional root `NodeVisitor` instance used to delegate operations such as
                     reference resolution or node dispatch. If None, the visitor operates standalone.
        """
        super().__init__()
        self.__root: typing.Optional[NodeVisitor] = root
        self.__has_been_used: bool = False

    #
    # PRIVATE
    #

    @staticmethod
    def __get_all_objects(d: Document) -> typing.List[PDFType]:
        obj_todo: typing.List[typing.Any] = [d]
        obj_done: typing.List[typing.Any] = []
        ids_done: typing.Set[int] = set()
        while len(obj_todo) > 0:
            n: typing.Any = obj_todo.pop(0)
            if isinstance(n, reference):
                n = n.get_referenced_object()
            if id(n) in ids_done:
                continue
            obj_done += [n]
            ids_done.add(id(n))
            if isinstance(n, dict):
                for k, v in n.items():
                    obj_todo += [k]
                    obj_todo += [v]
                continue
            if isinstance(n, list):
                for k in n:
                    obj_todo += [k]
                continue
        return obj_done

    @staticmethod
    def __print_warning(c: ConformanceCheck, r: typing.Optional[reference]) -> None:
        ref_str = f"{r}" if r else "<unknown object reference>"

        # print warning
        import warnings

        warnings.warn(
            f"Conformance {', '.join(c.name for c in c.get_conformance())} — "
            f"Clause {c.get_clause()}, Test {c.get_test_number()}: {c.get_description()} "
            f"(Object: {ref_str})",
            category=UserWarning,
            stacklevel=2,
        )

    @staticmethod
    def __throw_assert(c: ConformanceCheck, r: typing.Optional[reference]) -> None:
        # TODO
        pass

    #
    # PUBLIC
    #

    def visit(self, node: typing.Any) -> typing.Optional[typing.Any]:
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
        if not isinstance(node, Document):
            return False
        if self.__has_been_used:
            return False

        # get all checks that need to be performed
        all_checks: typing.List[ConformanceCheck] = [
            x
            for x in ConformanceChecks.get()
            if node.get_conformance_at_create() in x.get_conformance()
        ]

        # get all objects on which checks need to be performed
        all_objects: typing.List[PDFType] = []
        if len(all_checks) > 0:
            all_objects = ValidationVisitor.__get_all_objects(node)

        # determine what we ought to do when encountering a non-conformance
        # fmt: off
        on_non_conformance_print_warning: bool = True
        on_non_conformance_throw_assert: bool = False
        try:
            on_non_conformance_print_warning = node._Document__on_non_conformance_print_warning # type: ignore[attr-defined]
            on_non_conformance_throw_assert = node._Document__on_non_conformance_throw_assert   # type: ignore[attr-defined]
        except:
            pass
        # fmt: on

        # perform checks
        for obj in all_objects:
            for check in all_checks:
                if check.check_whether_object_violates_clause(obj):
                    obj_ref = next(
                        iter(
                            [
                                x
                                for x in node.get("XRef", [])
                                if id(x.get_referenced_object()) == id(obj)
                            ]
                        ),
                        None,
                    )
                    if on_non_conformance_print_warning:
                        ValidationVisitor.__print_warning(c=check, r=obj_ref)
                    if on_non_conformance_throw_assert:
                        ValidationVisitor.__throw_assert(c=check, r=obj_ref)

        # delegate to root
        self.__has_been_used = True
        if self.__root is not None:
            self.__root.visit(node)

        # return
        return True
