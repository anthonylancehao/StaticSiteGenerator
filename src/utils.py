import os
import markdown
import re

def generate_page(content_path, template_path, output_path, basepath="/"):
    with open(content_path, "r") as f:
        markdown_content = f.read()

    html_content = markdown.markdown(markdown_content)

    # Inject basepath into href/src if not absolute
    def add_basepath(match):
        attr, url = match.groups()
        if url.startswith(("http://", "https://", "mailto:", "#", basepath)):
            return f'{attr}="{url}"'
        return f'{attr}="{basepath.rstrip("/")}/{url.lstrip("/")}"'

    html_content = re.sub(r'(href|src)="([^"]+)"', add_basepath, html_content)

    with open(template_path, "r") as f:
        template = f.read()

    full_html = template.replace("{{ content }}", html_content)

    with open(output_path, "w") as f:
        f.write(full_html)
