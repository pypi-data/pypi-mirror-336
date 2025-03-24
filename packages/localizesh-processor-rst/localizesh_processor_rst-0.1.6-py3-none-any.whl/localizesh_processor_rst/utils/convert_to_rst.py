from typing import Dict, List, Callable
from localizesh_sdk import LayoutRoot, LayoutElement, LayoutSegment, Segment
import re
import json

def convert_to_rst(node: LayoutRoot, segments: List[Segment]) -> str:
    if node is None:
        return ""

    try:
        node_type = node["type"]
    except KeyError:
        return ""

    def convert_root(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(children)

    def convert_element(node: LayoutElement) -> str:
        tag_handlers = {
            "title": convert_h,
            "img": convert_image,
            "reference": convert_reference,
            'strong': convert_strong,
            'literal': convert_literal,
            'emphasis': convert_emphasis,
            "p": convert_p,
            "section": convert_section,
            "ul": convert_ul,
            "li": convert_li,
            "pre": convert_pre,
            "field_list": convert_field_list,
            "field": convert_field,
            "system_message": convert_system_message,
            "comment": convert_comment,
            "table": convert_table,
            "tgroup": convert_tgroup,
            "thead": convert_thead,
            "tbody": convert_tbody,
            "row": convert_row,
            "entry": convert_entry,
            "target": convert_target,
            "important": convert_important,
            "note": convert_note,
            "warning": convert_warning,
            "topic": convert_topic,
            "math_block": convert_math_block
        }

        node_properties = node.get("properties")
        rst_type = node_properties.get("rst_type") if node_properties is not None else None
        tag_name = node.get("tagName")
        if rst_type or tag_name in tag_handlers:
            return tag_handlers[rst_type or tag_name](node)
        return ""

    def convert_topic(node: LayoutElement) -> str:
        properties = node.get("properties")
        classes = properties.get("classes")[0]
        text = convert_hast_children(node.get("children", []))

        return f".. {classes}:: {text}"

    def convert_math_block(node: LayoutElement) -> str:
        # names = node.get("properties").get("names")
        code = node.get("children")[0]
        code_text = convert_to_rst(code.get("children")[0], segments)
        is_multiline = code_text.count('\n') > 0

        result_text = code_text
        if is_multiline:
            result_text = "\n   " + "   ".join(code_text.splitlines(True)) + "\n"
        else:
            result_text = " " + result_text + "\n"

        return ".. math::" + result_text

    def convert_strong(node: LayoutElement) -> str:
        properties = node.get("properties")
        separator = properties.get("separator", "**")
        text = convert_hast_children(node.get("children", []))
        return f"{separator}{text}{separator}"

    def convert_literal(node: LayoutElement) -> str:
        text = convert_hast_children(node.get("children", []))
        return f"``{text}``"

    def convert_emphasis(node: LayoutElement) -> str:
        text = convert_hast_children(node.get("children", []))
        return f"*{text}*"

    def convert_text(node: LayoutElement) -> str:
        return node.get("value", "")

    def convert_image(node: LayoutElement) -> str:

        properties = node.get("properties", "")
        rst_string = ""
        if properties:
            src = properties.get('src', '')
            width = properties.get('width', '')
            alt = properties.get('alt', '')
            align = properties.get('align', None)
            rst_string = f".. image:: {src}\n  :width: {width}\n  :alt: {alt}"
            if align:
                rst_string = rst_string + "\n  :align: " + align

        return rst_string

    def convert_reference(node: LayoutElement) -> str:
        href = node["properties"].get("href", "")
        text = convert_hast_children(node.get("children", []))
        return "`" + text + " <" + href + ">`__"

    def convert_segment(node: LayoutSegment) -> str:
        segment_id = node.get("id")
        segment = next((seg for seg in segments if seg["id"] == segment_id), None)

        if segment is None:
            return "Segment not found"

        hast_children = parse_string_to_hast_structure(segment)
        return convert_hast_children(hast_children)

    def convert_hast_children(children: List) -> str:
        result_string = ""
        if len(children) > 0:
            for hast_child in children:
                if hast_child["type"] == "text":
                    result_string += convert_text(hast_child)
                else:
                    result_string += convert_element(hast_child)
        return result_string

    def convert_h(node: LayoutElement) -> str:
        text = convert_to_rst(node.get("children", [{}])[0], segments)
        separator = node.get('properties').get("separator", "-")

        if separator is None:
            return text

        level = separator * len(text)
        header_type = node.get('properties').get('header_type')

        if header_type == 'section':
            return f"{text}\n{level}\n"
        elif header_type == 'document':
            return f".. title:: {text}\n"
        else:
            return f"{level}\n{text}\n{level}\n"

    def convert_comment(node: LayoutElement) -> str:
        text = convert_to_rst(node.get("children", [{}])[0], segments)
        separator = node.get('properties').get("separator", "..")
        return f"{separator} {text}"

    def convert_p(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(children) + "\n"

    def convert_section(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(children)

    def convert_ul(node: LayoutElement) -> str:
        items = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(items)

    def convert_li(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        separator = node.get('properties').get("separator", "-")
        return separator + " " + "\n  ".join(children)

    def convert_pre(node: LayoutElement) -> str:
        if node.get("children"):
            return "::\n\n  " + convert_to_rst(node["children"][0], segments)
        else:
            return "::\n\n"

    def convert_field_list(node: LayoutElement) -> str:
        items = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n\n".join(items)

    def convert_field(node: LayoutElement) -> str:
        tr = node.get("children")[0].get("children")[0]
        if tr.get("tagName") == "tr":
            tr_children = tr.get("children")
            field_name = convert_to_rst(tr_children[0].get("children")[0], segments)
            field_body = convert_to_rst(tr_children[1].get("children")[0].get("children")[0], segments)
            return f"\n:{field_name}: {field_body}\n"
        else:
            name = convert_to_rst(node.get('children', [{}])[0], segments)
            body = convert_to_rst(node.get('children', [{}])[1], segments)
            return f"{name}:\n  {body}"

    def convert_system_message(node: LayoutElement) -> str:
        return convert_to_rst(node.get("children", [{}])[0], segments)

    def convert_table(node: LayoutElement) -> str:
        list_table = node.get('properties').get("list_table", "")

        if list_table != None:
            children = [convert_to_rst(child, segments) for child in node.get("children", [])]
            return list_table + "\n" + "".join(children)

        else:
            def get_table_dimensions(table_node):
                max_cols = 0
                rows = []

                for tgroup in table_node['children']:
                    for tbody in tgroup['children']:
                        if tbody['tagName'] in ['thead', 'tbody']:
                            rows.extend(tbody['children'])

                max_rows = len(rows)
                for row in rows:
                    col_count = 0
                    for entry in row['children']:
                        morecols = int(entry['properties'].get('morecols', 0))
                        col_count += 1 + morecols
                    max_cols = max(max_cols, col_count)

                return max_rows, max_cols

            def build_table_array(table_node, rows, cols):
                table_array = [['' for _ in range(cols)] for _ in range(rows)]
                row_idx = 0

                for tgroup in table_node['children']:
                    for tbody in tgroup['children']:
                        if tbody['tagName'] in ['thead', 'tbody']:
                            for row in tbody['children']:
                                col_idx = 0
                                for entry in row['children']:
                                    while table_array[row_idx][col_idx] != '':
                                        col_idx += 1
                                    cell_text = convert_entry_Table(entry)
                                    morecols = int(entry['properties'].get('morecols', 0))
                                    morerows = int(entry['properties'].get('morerows', 0))
                                    for i in range(morerows + 1):
                                        for j in range(morecols + 1):
                                            if i == 0 and j == 0:
                                                table_array[row_idx + i][col_idx + j] = cell_text
                                    col_idx += morecols + 1
                                row_idx += 1

                return table_array

            def restore_table(table_node):
                max_rows, max_cols = get_table_dimensions(table_node)
                table_array = build_table_array(table_node, max_rows, max_cols)

                col_widths = [max(len(cell) for cell in col) for col in zip(*table_array)]

                def build_separator(char, widths):
                    return '+' + '+'.join([char * (w + 2) for w in widths]) + '+'

                horizontal_sep = build_separator('-', col_widths)
                header_sep = build_separator('=', col_widths)

                table_lines = []

                table_lines.append(horizontal_sep)

                for i, row in enumerate(table_array):
                    line = '| ' + ' | '.join(f"{cell:<{col_widths[j]}}" for j, cell in enumerate(row)) + ' |'
                    table_lines.append(line)
                    if i == 0:
                        table_lines.append(header_sep)
                    else:
                        table_lines.append(horizontal_sep)

                return '\n'.join(table_lines)

            return restore_table(node)

    def convert_tgroup(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "".join(children)

    def convert_thead(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(children)

    def convert_tbody(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "".join(children)

    def convert_row(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "   * - " + "     - ".join(children)

    def convert_entry(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(children)

    def convert_entry_Table(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "".join(children).replace('\n', ' ').strip()

    def convert_target(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return "\n".join(children) + "\n"

    def convert_important(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        return ".. important:: " + "\n".join(children) + "\n"

    def convert_note(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        children_text = "\n".join(children).replace("\n", "\n   ")
        return ".. note::\n   " + children_text + "\n"

    def convert_warning(node: LayoutElement) -> str:
        children = [convert_to_rst(child, segments) for child in node.get("children", [])]
        children_text = "\n".join(children).replace("\n", "\n   ")
        return ".. warning::\n   " + children_text + "\n"

    handlers = {
        "root": convert_root,
        "element": convert_element,
        "text": convert_text,
        "segment": convert_segment,
    }

    if node_type in handlers:
        return handlers[node_type](node)
    else:
        return ""


def strong(tag: str, content: str, properties: Dict[str, Callable[[str], str]]) -> str:
    separator = properties[tag]['separator']

    return f"{separator}{content}{separator}"


def reference(tag: str, content: str, properties: Dict[str, Callable[[str], str]]) -> str:
    url = properties[tag]['href']

    return f"`{content} {url}`__"


def literal(tag: str, content: str, properties: Dict[str, Callable[[str], str]]) -> str:
    return f"``{content}``"


def emphasis(tag: str, content: str, properties: Dict[str, Callable[[str], str]]) -> str:
    return f"*{content}*"


def parse_string_to_hast_structure(segment: Segment) -> List[LayoutElement]:
    text = segment.get("text", "")
    stack = []
    current_text = ""
    properties = {}

    allowed_tags_regex = re.compile(r'^\/?[a-zA-Z-:]+\d+$')

    i = 0
    while i < len(text):
        if text[i] == "{" and allowed_tags_regex.match(text[i + 1:text.index("}", i + 1)]):
            if current_text:
                stack.append({
                    "type": "text",
                    "value": current_text,
                })
                current_text = ""

            closing_index = text.index("}", i + 1)
            tag_with_index = text[i + 1:closing_index]

            heading_tag_regex = re.compile(r'^(\/)?h(\d)*$')
            tag = heading_tag_regex.sub('', tag_with_index) if heading_tag_regex.match(tag_with_index) else tag_with_index.replace(re.compile(r'\d').findall(tag_with_index)[-1], '')

            if tag.startswith("/"):
                closing_tag = tag[1:]
                elements = []

                while stack:
                    element = stack.pop()
                    if element["type"] == "element" and element["tagName"] == closing_tag:
                        element["children"] = elements
                        stack.append(element)
                        break
                    elements.insert(0, element)
            else:
                if segment["tags"]:
                    tag_attributes = segment["tags"].get(tag_with_index, {})
                    for tag_attr_key, tag_attr in tag_attributes.items():
                        is_stringified_object = (
                                isinstance(tag_attr, str) and
                                ((tag_attr.startswith("{") and tag_attr.endswith("}")) or
                                 (tag_attr.startswith("[") and tag_attr.endswith("]")))
                        )
                        if is_stringified_object:
                            tag_attributes[tag_attr_key] = json.loads(tag_attr)
                    properties = segment["tags"][tag_with_index]

                element = {
                    "type": "element",
                    "tagName": tag,
                    "properties": properties,
                    "children": [],
                }

                stack.append(element)

            i = closing_index
        else:
            current_text += text[i]
        i += 1

    if current_text:
        stack.append({
            "type": "text",
            "value": current_text,
        })

    return stack