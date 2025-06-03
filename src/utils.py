import os
from conversions import markdown_to_html_node

def generate_page(from_path, template_path, to_path, basepath="/"):
    print(f"Generating page from {from_path} -> {to_path} with basepath '{basepath}'")

    # Read markdown content
    with open(from_path, "r") as f:
        markdown = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html(basepath=basepath)

    # Read the HTML template
    with open(template_path, "r") as f:
        template = f.read()

    # Replace the {{ Content }} placeholder
    final_html = template.replace("{{ Content }}", content_html)

    # Write final HTML to output file
    with open(to_path, "w") as f:
        f.write(final_html)
