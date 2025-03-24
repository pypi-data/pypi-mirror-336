from docutils import nodes
from localizesh_sdk import Context, Segment, IdGenerator, LayoutRoot
from typing import Dict, Any, Optional, List
import re
import json

def convert_to_ast(node: nodes.Node) -> Optional[Dict[str, Any]]:

    def math_block_handler(n: nodes.Text) -> Dict[str, str]:
        text = n.astext()
        names = n.get("names", None)
        return {
            "type": "element",
            "tagName": "pre",
            "properties": {"rst_type": "math_block", "names": names},
            "children": [{
                "type": "element",
                "tagName": "code",
                "properties": {},
                "children": [{
                    "type": "text",
                    "value": text
                }]
            }]
        }

    def footnote_reference_handler(n: nodes.Text) -> Dict[str, str]:

        return {
            "type": "text",
            "value": "[#" + n.get("refid", "") + "]_"
        }

    def footnote_handler(n: nodes.Text) -> Dict[str, str]:
        footnote = {
            "type": "text",
            "value": ".. [#" + n.get("names", [""])[0] + "] "
        }
        children = [convert_to_ast(child) for child in n.children]
        paragraph = children[1]
        paragraph_children = paragraph.get("children", [])
        paragraph_children.insert(0, footnote)
        return paragraph

    def text_handler(n: nodes.Text) -> Dict[str, str]:        
        return {"type": "text", "value": n.astext()}

    def title_handler(n: nodes.title) -> Dict[str, Any]:
        separator = node.get('separator', '-')
        header_type = node.get('header_type')
        return {
            "type": "element",
            "tagName": "h3" if header_type == "section" or header_type is None else "h2",
            "properties": {"separator": separator, "header_type": header_type, "rst_type": "title"},
            "children": [convert_to_ast(child) for child in n.children]
        }

    def paragraph_handler(n: nodes.paragraph) -> Dict[str, Any]:
        children = []
        properties = {}
        for child in n.children:
            node = convert_to_ast(child)
            children.append(node)

        return {
            "type": "element",
            "tagName": "p",
            "properties": properties,
            "children": children
        }
    
    def document_handler(n: nodes.document) -> Dict[str, Any]:
        document_title = n.get("title") != "--title"
        children = [convert_to_ast(child) for child in n.children]

        if document_title:
            children.insert(0, {
                "type": "element",
                "tagName": "h2",
                "properties": {"separator": "=", "header_type": "document", "rst_type": "title"},
                "children": [
                    {
                        "type": "text",
                        "value": n.get("title")
                    }
                ]
            })

        return {
            "type": "root",
            "children": children
        }
    
    def list_item_handler(n: nodes.list_item) -> Dict[str, Any]:
        separator = node.get('separator', '-')
        return {
            "type": "element",
            "tagName": "li",
            "properties": {"separator": separator},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def list_handler(n: nodes.list_item) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "ul",
            "properties": {},
            "children": [convert_to_ast(child) for child in n.children]
        }

    def field_handler(n: nodes.list_item) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "table",
            "properties": {"rst_type": "field"},
            "children": [
                {
                    "type": "element",
                    "tagName": "tbody",
                    "properties": {},
                    "children": [
                        {
                            "type": "element",
                            "tagName": "tr",
                            "properties": {},
                            "children": [convert_to_ast(child) for child in n.children]
                        }
                    ]
                }
            ]
        }

    def field_name_handler(n: nodes.list_item) -> Dict[str, Any]:

        return {
            "type": "element",
            "tagName": "td",
            "properties": {"cell_type": "key"},
            "children": [convert_to_ast(child) for child in n.children]
        }

    def field_body_handler(n: nodes.list_item) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "td",
            "properties": {"cell_type": "value"},
            "children": [convert_to_ast(child) for child in n.children]
        }

    def section_handler(n: nodes.section) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "section",
            "properties": {},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def strong_handler(n: nodes.strong) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "strong",
            "properties": {"separator": "**"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def comment_handler(n: nodes.comment) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "p",
            "properties": {"separator": "..", "rst_type": "comment"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def system_message_handler(n: nodes.system_message) -> Dict[str, Any]:
        if len(n.children) > 1:
            return {
                "type": "element",
                "tagName": "p",
                "properties": {"rst_type": "system_message"},
                "children": [{"type": "text", "value": n.children[1].astext()}]
            }
        else:
            return {"type": "text", "value": ""}
    
    def table_handler(n: nodes.table) -> Dict[str, Any]:
        list_table = node.get('list-table', None)
        return {
            "type": "element",
            "tagName": "table",
            "properties": {"list_table": list_table, "rst_type": "table"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def tgroup_handler(n: nodes.tgroup) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "table",
            "properties": {"rst_type": "tgroup"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def thead_handler(n: nodes.thead) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "thead",
            "properties": {"rst_type": "thead"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def row_handler(n: nodes.row) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "tr",
            "properties": {"rst_type": "row"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def entry_handler(n: nodes.entry) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "td",
            "properties": {"rst_type": "entry"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def tbody_handler(n: nodes.tbody) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "tbody",
            "properties": {"rst_type": "tbody"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def colspec_handler(n: nodes.colspec) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "tbody",
            "properties": {"rst_type": "tbody"},
            "children": []
        }
    
    def image_handler(n: nodes.image) -> Dict[str, Any]:
        attributes = n.attributes

        return {
            "type": "element",
            "tagName": "p",
            "properties": {},
            "children": [
                {
                    "type": "element",
                    "tagName": "img",
                    "properties": {
                        "src": attributes.get("uri", ""),
                        "alt": attributes.get("alt", ""),
                        "width": attributes.get("width", ""),
                        "align": attributes.get("align", ""),
                    },
                    "children": []
                }
            ]
        }
    
    def reference_handler(n: nodes.reference) -> Dict[str, Any]:
        label = n.astext()
        cleaned_string = n.rawsource.replace('`', '').replace('__', '')
        url = cleaned_string.replace(label, '').strip()
        url = url[1:len(url) - 1]
        return {
            "type": "element",
            "tagName": "a",
            "properties": {"rst_type": "reference", "href": url},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def literal_handler(n: nodes.literal) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "p",
            "properties": {"rst_type": "literal"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def emphasis_handler(n: nodes.emphasis) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "em",
            "properties": {"rst_type": "emphasis"},
            "children": [convert_to_ast(child) for child in n.children]
        }
    
    def target_handler(n: nodes.target) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "p",
            "properties": {"rst_type": "target"},
            "children": [{"type": "text", "value": n.rawsource}]
        }
    
    def important_handler(n: nodes.important) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "strong",
            "properties": {"rst_type": "important"},
            "children": [{"type": "text", "value": n.rawsource}]
        }
    
    def note_handler(n: nodes.note) -> Dict[str, Any]:
        return {
            "type": "element",
            "tagName": "p",
            "properties": {"rst_type": "note"},
            "children": [{"type": "text", "value": n.rawsource}]
        }
    def warning_handler(n: nodes.warning) -> Dict[str, Any]:
         return {
             "type": "element",
             "tagName": "p",
             "properties": {"rst_type": "warning"},
             "children": [{"type": "text", "value": n.rawsource}]
         }
    def topic_handler(n: nodes.warning) -> Dict[str, Any]:
        classes = n.get("classes")
        first_child = n.children[0]
        return {
            "type": "element",
            "tagName": "p",
            "properties": {"rst_type": "topic", "classes": classes},
            "children": [convert_to_ast(first_child)]
        }

    handlers_node_types = {
        nodes.document: document_handler,
        nodes.Text: text_handler,
        nodes.title: title_handler,
        nodes.paragraph: paragraph_handler,
        nodes.list_item: list_item_handler,
        nodes.option_list_item: list_item_handler,
        nodes.definition_list_item: list_item_handler,
        nodes.enumerated_list: list_handler,
        nodes.definition_list: list_handler,
        nodes.option_list: list_handler,
        nodes.bullet_list: list_handler,
        nodes.field_list: list_handler,
        nodes.field: field_handler,
        nodes.section: section_handler,
        nodes.strong: strong_handler,
        nodes.comment: comment_handler,
        nodes.system_message: system_message_handler,
        nodes.table: table_handler,
        nodes.tgroup: tgroup_handler,
        nodes.thead: thead_handler,
        nodes.row: row_handler,
        nodes.entry: entry_handler,
        nodes.tbody: tbody_handler,
        nodes.colspec: colspec_handler,
        nodes.image: image_handler,
        nodes.reference: reference_handler,
        nodes.literal: literal_handler,
        nodes.emphasis: emphasis_handler,
        nodes.target: target_handler,
        nodes.important: important_handler,
        nodes.note: note_handler,
        nodes.warning: warning_handler,
        nodes.topic: topic_handler,
        nodes.field_body: field_body_handler,
        nodes.field_name: field_name_handler,
        nodes.footnote_reference: footnote_reference_handler,
        nodes.footnote: footnote_handler,
        nodes.math_block: math_block_handler
    }

    for node_type, handler in handlers_node_types.items():
        if isinstance(node, node_type):
            return handler(node)

    return {"type": "text", "value": ""}


def hast_to_document(node, ctx: Context) -> LayoutRoot:
    generator = IdGenerator()
    segments: List[Segment] = []

    def hast_to_document_recursive(node) -> LayoutRoot:
        node_type = node.get("type")

        is_contain_custom_tag = False
        is_contain_text_node_content = False
        content_length = 0
        if node and "children" in node:
            for child in node["children"]:
                tag_name = child.get("tagName", None)
                if child.get("type") == "element" or len(child["value"]) > 0:
                    content_length += 1
                if is_contain_custom_tag is False:
                    is_contain_custom_tag = tag_name == "a" or tag_name == "img"
                if is_contain_text_node_content is False:
                    is_contain_text_node_content = child["type"] == "text" and len(child["value"]) > 0

        if is_contain_text_node_content and content_length > 1 or is_contain_custom_tag is True:
            string_structure = hast_to_string(node)
            segment_id = generator.generate_id(text=string_structure["text"], tags=string_structure["tags"], context=str(ctx))
            segment = {"id": segment_id, "text": string_structure["text"]}

            if string_structure["tags"]:
                segment["tags"] = string_structure["tags"]
            segments.append(segment)

            node["children"] = [{"type": "segment", "id": segment_id}]
            return node

        elif node_type == "text":
            text_value = node.get("value")
            if len(text_value) > 0:
                tags = None
                segment_id = generator.generate_id(text=text_value, tags=tags, context=str(ctx))
                segment = {"id": segment_id, "text": text_value}

                if tags:
                    segment["tags"] = tags

                segments.append(segment)

                return {"type": "segment", "id": segment_id}
            else:
                return node

        elif node and "children" in node:
            node["children"] = [hast_to_document_recursive(child) for child in node["children"]]

        return node

    layout = hast_to_document_recursive(node)
    return layout, segments

def hast_to_string(root_node, options=None) -> str:
    if options is None:
        options = {}

    root_context = options.get('rootContext', {'index': -1})
    tags = {}

    def to_string_recursive(node, context):
        result = []
        if "tagName" in node and node['tagName'] == "img":
            context['index'] += 1
            node_tag_key = f"{node['tagName']}{context['index'] - 1}"

            if node['properties']:
                tags[node_tag_key] = node['properties']

            return "{" + node_tag_key + "}"

        elif node['type'] == 'element':
            node_name = node['tagName']
            node_tag_key = f"{node_name}{context['index']}"
            index = context['index']

            context['index'] += 1

            node_properties_keys = list(node['properties'].keys())
            if node_properties_keys and root_context['index'] != -1:
                tag_attributes = {}
                for prop_key in node_properties_keys:
                    tag_attribute_value = node['properties'][prop_key]
                    tag_attribute_value_is_object = isinstance(tag_attribute_value, dict)
                    tag_attributes[prop_key] = (
                        json.dumps(tag_attribute_value) if tag_attribute_value_is_object else tag_attribute_value
                    )
                tags[node_tag_key] = tag_attributes

            tag_string_open = "{" + node_tag_key + "}" if index != -1 else ""
            tag_string_close = "{/" + node_tag_key + "}" if index != -1 else ""

            result.append(
                tag_string_open + ''.join(
                    to_string_recursive(child_node, context) for child_node in node['children']
                ) + tag_string_close
            )
        elif node['type'] == 'text':
            if 'tags' in node:
                tags.update(node['tags'])
            result.append(node['value'])

        return ''.join(result)

    return {
        'text': to_string_recursive(root_node, root_context),
        'tags': tags
    }