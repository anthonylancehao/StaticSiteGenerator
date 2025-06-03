import os
import shutil
import sys
from utils import generate_page

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

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

def main():
    # Use basepath from CLI, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    docs_dir = "docs"
    static_dir = "static"
    content_dir = "content"
    template_path = "template.html"

    # Clear docs directory
    if os.path.exists(docs_dir):
        print(f"Removing existing contents of {docs_dir}")
        shutil.rmtree(docs_dir)
    os.makedirs(docs_dir)

    # Copy static files
    print(f"Copying static files from {static_dir} to {docs_dir}")
    copy_static(static_dir, docs_dir)

    # Generate pages recursively
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)

if __name__ == "__main__":
    main()
