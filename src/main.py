from textnode import TextNode, TextType
import logging
import os
import shutil
import sys
from functions import *

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("#") and not line.startswith("##"):
            return line[1:].strip()
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as contents_file:
        contents = contents_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    converted = markdown_to_html_node(contents)
    html_contents = converted.to_html()
    try:
        title = extract_title(contents)
    except Exception:
        title = "Untitled"
    replaced_title = template.replace("{{ Title }}", title)
    replaced_content = replaced_title.replace("{{ Content }}", html_contents)
    replaced_content = replaced_content.replace('href="/', f'href="{basepath}')
    replaced_content = replaced_content.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(replaced_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, dest_path, basepath)
            continue

        if os.path.isfile(entry_path) and entry_path.endswith(".md"):
            dest_html_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(entry_path, template_path, dest_html_path, basepath)

def from_source_to_dest(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    for entry in os.listdir(dest_path):
        entry_path = os.path.join(dest_path, entry)
        if os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
        else:
            os.remove(entry_path)

    for entry in os.listdir(source_path):
        source_entry = os.path.join(source_path, entry)
        dest_entry = os.path.join(dest_path, entry)
        if os.path.isdir(source_entry):
            logging.info("Copying directory %s -> %s", source_entry, dest_entry)
            shutil.copytree(source_entry, dest_entry)
        else:
            logging.info("Copying file %s -> %s", source_entry, dest_entry)
            shutil.copy2(source_entry, dest_entry)

def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    from_source_to_dest("static/", "docs/")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
