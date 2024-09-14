import re, os, shutil
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(markdown):
    heading_pattern = r"^#{1,6}"
    code_pattern = r"```.*?```"
    quote_pattern = r"^>"
    unordered_pattern = r"(^[\*\-\+] +.*(\n|$))+"
    ordered_pattern = r"(^\d+\. +.*(\n|$))+"

    if re.match(heading_pattern, markdown):
        found = re.findall(heading_pattern, markdown)[0]
        return f"heading {len(found)}"
    elif re.match(code_pattern, markdown):
        return "code"
    elif re.match(quote_pattern, markdown):
        return "quote"
    elif re.search(unordered_pattern, markdown, re.MULTILINE):
        return "unordered_list"
    elif re.search(ordered_pattern, markdown, re.MULTILINE):
        return "ordered_list"
    else:
        return "pharagraph"


def map_markdown_to_html(type, text):
    if len(type.split(" ")) > 1:
        level = 0
        for char in text:
            if char == "#":
                level += 1
            else:
                break
        if level + 1 >= len(text):
            raise ValueError(f"Invalid heading level: {level}")
        new_text = text[level + 1 :]
        new_children = text_to_children(new_text)
        return ParentNode(f"h{level}", new_children)
    elif type == "quote":
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("Invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)
    elif type == "code":
        if not text.startswith("```") or not text.endswith("```"):
            raise ValueError("Invalid code text")
        text = text[4:-3]
        children = text_to_children(text)
        code = ParentNode("code", children)
        return ParentNode("pre", [code])
    elif type == "ordered_list":
        items = text.split("\n")
        html_items = []
        for item in items:
            cur_text = item[3:]
            children = text_to_children(cur_text)
            html_items.append(ParentNode("li", children))

        return ParentNode("ol", html_items)
    elif type == "unordered_list":
        items = text.split("\n")
        html_items = []
        for item in items:
            cur_text = item[2:]
            children = text_to_children(cur_text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ul", html_items)
    else:
        lines = text.split("\n")
        paragraph = " ".join(lines)
        children = text_to_children(paragraph)
        return ParentNode("p", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block_type(block)
        html_node = map_markdown_to_html(type, block)
        children.append(html_node)
    return ParentNode("div", children, None)


text_type_to_html_tag = {
    "text": "",
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img",
}


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    titles = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading 1":
            titles.append(block.replace("#", "").strip())

    if len(titles) == 0:
        raise Exception("No title")

    return titles[0]


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)


def generate_pages_recursive(dir_path_content, template_path, des_dir_path):
    if not os.path.exists(des_dir_path):
        os.mkdir(des_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(des_dir_path, filename)
        if os.path.isfile(from_path):
            print(from_path, dest_path)
            base = os.path.splitext(dest_path)[0]
            generate_page(from_path, template_path, base + ".html")
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
