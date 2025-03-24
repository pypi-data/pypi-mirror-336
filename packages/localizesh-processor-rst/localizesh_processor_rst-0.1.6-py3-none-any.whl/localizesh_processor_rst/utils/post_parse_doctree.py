from docutils import nodes


def get_separator_from_line(text: str, node: nodes.Node) -> [str, bool]:
    if node.line:
        line_num = node.line - 1
        line_num_above = node.line - 3
        spliced_lines = text.splitlines()
        line = spliced_lines[line_num]
        is_section_title = line.strip() != spliced_lines[line_num_above].strip()
        separator = line.strip()[0]
        return [separator, is_section_title]
    else:
        return [None, False]

def get_marker_list_from_line(text: str, node: nodes.Node) -> str:
    if node.line:
        line_num = node.line - 1
        line = text.splitlines()[line_num]
        separator = line.strip().split(' ', 1)[0]
        return separator
    else:
        return None

def post_parse_doctree(text: str, doctree: nodes.document) -> nodes.document:
    for node in doctree.traverse():
        if isinstance(node, nodes.topic):
            node
        elif isinstance(node, nodes.title):
            [separator, is_section_title] = get_separator_from_line(text, node)
            node['separator'] = separator
            if is_section_title:
                node['header_type'] = 'section'

        elif isinstance(node, nodes.list_item):
            node['separator'] = get_marker_list_from_line(text, node)

        elif isinstance(node, nodes.table):
            if node.source != "<string>":
                colspecs = [col.attributes.get('colwidth', '') for col in node.traverse(nodes.colspec)]
                thead = node.next_node(nodes.thead)
                header_rows = len(thead) if thead else 0
                directive_text = ".. list-table::\n"
                directive_text += f"   :header-rows: {header_rows}\n"
                directive_text += f"   :widths: {' '.join(map(str, colspecs))}\n"
                node['list-table'] = directive_text

    return doctree

