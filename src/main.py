import os
import sys
import shutil
from utils import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        content_entry_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(content_entry_path):
            # Recurse into subdirectories
            dest_entry_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(content_entry_path, template_path, dest_entry_path, basepath)
        elif os.path.isfile(content_entry_path) and entry.endswith(".md"):
            # Convert .md path to .html path
            relative_path = os.path.relpath(content_entry_path, dir_path_content)
            relative_html_path = relative_path[:-3] + ".html"
            output_path = os.path.join(dest_dir_path, relative_html_path)

            # Make sure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"Generating page from {content_entry_path} to {output_path} using {template_path}")
            generate_page(content_entry_path, template_path, output_path, basepath)

def copy_static_files(static_dir, dest_dir):
    if os.path.exists(dest_dir):
        print(f"Removing existing contents of {dest_dir}")
        shutil.rmtree(dest_dir)
    print(f"Copying static files from {static_dir} to {dest_dir}")
    shutil.copytree(static_dir, dest_dir)

def main():
    # Get basepath from CLI argument or default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.endswith("/"):
        basepath += "/"

    content_dir = "content"
    template_path = "template.html"
    docs_dir = "docs"

    # Remove old docs directory and recreate
    if os.path.exists(docs_dir):
        print(f"Removing existing contents of {docs_dir}")
        shutil.rmtree(docs_dir)
    os.makedirs(docs_dir, exist_ok=True)

    # Copy static files into docs (for GitHub Pages)
    copy_static_files("static", docs_dir)

    # Generate all pages recursively, passing basepath
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)

if __name__ == "__main__":
    main()
