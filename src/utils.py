import os
import markdown
import re

def generate_page(content_path, template_path, output_path, basepath="/"):
    with open(content_path, "r") as f:
        markdown_content = f.read()

    html_content = markdown.markdown(markdown_content)

    # Fix href/src inside the generated HTML (from markdown)
    def fix_paths(match):
        attr, url = match.groups()
        if url.startswith(("http://", "https://", "mailto:", "#", basepath)):
            return f'{attr}="{url}"'
        # Otherwise, prefix with basepath
        return f'{attr}="{basepath.rstrip("/")}/{url.lstrip("/")}"'

    html_content = re.sub(r'(href|src)="([^"]+)"', fix_paths, html_content)

    with open(template_path, "r") as f:
        template = f.read()

    # Also fix href/src in the template
    template = re.sub(r'(href|src)="([^"]+)"', fix_paths, template)

    full_html = template.replace("{{ content }}", html_content)

    with open(output_path, "w") as f:
        f.write(full_html)
