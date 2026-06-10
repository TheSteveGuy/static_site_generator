import os

from markdown_blocks import markdown_to_html_node
from pathlib import Path


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    content_from_file = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    content_template_file = template_file.read()
    template_file.close()

    node = markdown_to_html_node(content_from_file)
    html = node.to_html()

    title = extract_title(content_from_file)
    content_template_file = content_template_file.replace("{{ Title }}", title)
    content_template_file = content_template_file.replace("{{ Content }}", html)

    destination_directory_path = os.path.dirname(dest_path)
    if destination_directory_path != "":
        os.makedirs(destination_directory_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(content_template_file)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[2:]
    raise Exception("There is no header")



