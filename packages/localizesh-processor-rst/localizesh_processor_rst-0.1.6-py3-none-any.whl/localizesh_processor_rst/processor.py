from docutils.core import publish_doctree, publish_from_doctree

from localizesh_sdk import Context, Document, Processor
from .utils.post_parse_doctree import post_parse_doctree
from .utils.convert_to_ast import convert_to_ast, hast_to_document
from .utils.convert_to_rst import convert_to_rst

class RstProcessor(Processor):
    
    def parse(self, res: str, ctx: Context) -> Document:
        doctree = publish_doctree(res)
        doctree = post_parse_doctree(res, doctree)

        hast = convert_to_ast(doctree)

        layout, segments = hast_to_document(hast, ctx)
        document = Document(layout=layout, segments=segments)

        return document

    def stringify(self, document: Document, ctx: Context) -> str:
        return convert_to_rst(document.layout, document.segments)