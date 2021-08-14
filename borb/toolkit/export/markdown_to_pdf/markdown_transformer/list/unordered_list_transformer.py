#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of BaseMarkdownTransformer handles unordered lists
"""
import typing

from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.toolkit.export.markdown_to_pdf.markdown_transformer.base_markdown_transformer import (
    BaseMarkdownTransformer,
    MarkdownTransformerState,
)


class UnorderedListTransformer(BaseMarkdownTransformer):
    """
    This implementation of BaseMarkdownTransformer handles unordered lists
    """

    def _can_transform(self, context: MarkdownTransformerState) -> bool:
        """
        To create an unordered list, add dashes (-), asterisks (*), or plus signs (+) in front of line items.
        Indent one or more items to create a nested list.
        """
        indent_level: int = 0
        while (
            context.tell() + indent_level < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + indent_level] == " "
        ):
            indent_level += 1
        return (
            context.get_markdown_string()[context.tell() + indent_level]
            in ["*", "-", "+"]
            and context.tell() + indent_level + 1 < len(context.get_markdown_string())
            and context.get_markdown_string()[context.tell() + indent_level + 1] == " "
        )

    def _transform(self, context: MarkdownTransformerState) -> None:

        # continue processing lines until we hit <newline><newline>
        end_pos: int = self._until_double_newline(context)
        if end_pos == -1:
            end_pos = len(context.get_markdown_string())
        list_lines_raw: typing.List[str] = context.get_markdown_string()[
            context.tell() : end_pos - 1
        ].split("\n")

        # determine initial indentation level
        index: int = 0
        prev_indentation_level: int = 0
        while list_lines_raw[0][prev_indentation_level] == " ":
            prev_indentation_level += 1

        list_items_str: typing.List[str] = []
        while index < len(list_lines_raw):

            # determine the indentation level
            indentation_level: int = 0
            while (
                indentation_level < len(list_lines_raw[index])
                and list_lines_raw[index][indentation_level] == " "
            ):
                indentation_level += 1

            # IF the indentation level changed (+4) AND there is no list_symbol --> continuation of previous item
            if indentation_level == prev_indentation_level + 4 and list_lines_raw[
                index
            ].strip()[0] not in ["+", "-", "*"]:
                list_items_str[-1] += "\n" + list_lines_raw[index][4:]
                index += 1
                continue

            # IF the indentation level changed AND there is a list symbol --> grab everything on that indentation level
            if indentation_level > prev_indentation_level and list_lines_raw[
                index
            ].strip()[0] in ["+", "-", "*"]:
                sublist_end_index: int = index
                while sublist_end_index < len(list_lines_raw) and list_lines_raw[
                    sublist_end_index
                ].startswith("".join([" " for _ in range(0, indentation_level)])):
                    sublist_end_index += 1
                list_items_str.append(
                    "".join(
                        [
                            list_lines_raw[i][indentation_level:] + "\n"
                            for i in range(index, sublist_end_index)
                        ]
                    )
                )
                index = sublist_end_index
                continue

            # IF the indentation level is equal AND there is no list_symbol --> error in markdown
            if indentation_level == prev_indentation_level and list_lines_raw[
                index
            ].strip()[0] not in ["+", "-", "*"]:
                assert (
                    False
                ), "Invalid markdown: To add another element in a list while preserving the continuity of the list, indent the element four spaces or one tab."

            # IF the indentation level is equal AND there is a list_symbol --> new item
            if indentation_level == prev_indentation_level and list_lines_raw[
                index
            ].lstrip()[0] in ["+", "-", "*"]:
                list_items_str.append(list_lines_raw[index].lstrip()[2:])
                index += 1

        # build UnorderedList
        ul: UnorderedList = UnorderedList()
        for s in list_items_str:
            sub_context: MarkdownTransformerState = MarkdownTransformerState(s)
            sub_context._document = context._document
            sub_context._parent_layout_element = ul
            self.get_root()._transform(sub_context)

        # add
        context.get_parent_layout_element().add(ul)  # type: ignore [union-attr]

        # seek
        context.seek(end_pos + 1)
