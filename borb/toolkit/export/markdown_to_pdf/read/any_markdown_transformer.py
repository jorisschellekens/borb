from borb.toolkit.export.markdown_to_pdf.read.transformer import (
    Transformer,
    TransformerState,
)
from borb.toolkit.export.markdown_to_pdf.read.heading.alternate_syntax_heading_transformer import (
    AlternateSyntaxHeadingTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.heading.heading_transformer import (
    HeadingTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.heading.horizontal_rule_transformer import (
    HorizontalRuleTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.list.ordered_list_transformer import (
    OrderedListTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.list.unordered_list_transformer import (
    UnorderedListTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.table.table_transformer import (
    TableTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.text.blockquote_transformer import (
    BlockQuoteTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.text.fenced_code_snippet_transformer import (
    FencedCodeSnippetTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.text.indented_code_snippet_transformer import (
    IndentedCodeSnippetTransformer,
)
from borb.toolkit.export.markdown_to_pdf.read.text.paragraph_transformer import (
    ParagraphTransformer,
)


class AnyMarkdownTransformer(Transformer):
    def __init__(self):
        super(AnyMarkdownTransformer, self).__init__()
        # fmt: off
        self.add_child_transformer(HeadingTransformer())                \
            .add_child_transformer(AlternateSyntaxHeadingTransformer()) \
            .add_child_transformer(HorizontalRuleTransformer())         \
            .add_child_transformer(BlockQuoteTransformer())             \
            .add_child_transformer(IndentedCodeSnippetTransformer())    \
            .add_child_transformer(FencedCodeSnippetTransformer())      \
            .add_child_transformer(UnorderedListTransformer())          \
            .add_child_transformer(OrderedListTransformer())            \
            .add_child_transformer(TableTransformer())                  \
            .add_child_transformer(ParagraphTransformer())
        # fmt: on

    def _can_transform(self, context: TransformerState) -> bool:
        return True

    def _transform(self, context: TransformerState) -> None:
        input_has_transformed: bool = True
        while input_has_transformed and context.tell() < len(
            context.get_markdown_string()
        ):
            # print("remaining input: `%s`" % context.get_markdown_string()[context.tell():context.get_markdown_string().find("\n", context.tell())])
            input_has_transformed = False
            for t in self._children:
                if t._can_transform(context):
                    t._transform(context)
                    input_has_transformed = True
                    break

            # this part catches any input and advances the tell() by 1
            if not input_has_transformed:
                context.seek(context.tell() + 1)
                input_has_transformed = True
