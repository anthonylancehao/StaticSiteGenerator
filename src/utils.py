import os
import markdown
import re

def generate_page(content_path, template_path, output_path, basepath="/"):
    with open(content_path, "r") as f:
        markdown_content = f.read()

    html_content = markdown.markdown(markdown_content)

    # Prefix all src/href with basepath
    def prefix_path(match):
        prefix = match.group(1)
        path = match.group(2)
        # Only prefix relative paths (not http, https, mailto, or anchors)
        if path.startswith(("http", "https", "mailto:", "#", basepath)):
            return match.group(0)
        return f'{prefix}="{basepath.rstrip("/")}/{path.lstrip("/")}"'

    html_content = re.sub(r'(src|href)="([^"]+)"', prefix_path, html_content)

    with open(template_path, "r") as f:
        template = f.read()

    full_html = template.replace("{{ content }}", html_content)

    with open(output_path, "w") as f:
        f.write(full_html)
