from conversions import markdown_to_html_node
from htmlnode import HTMLNode

def generate_page(input_path, template_path, output_path, basepath=""):
    print(f"Generating page from {input_path} -> {output_path} using {template_path}")
    with open(input_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown, basepath)
    html = html_node.to_html()

    output = template.replace("{{ content }}", html)

    with open(output_path, "w") as f:
        f.write(output)
