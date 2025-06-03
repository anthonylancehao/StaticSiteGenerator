import markdown

def extract_title(markdown_text):
    # Simple heuristic: get first markdown header line (# Title)
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"

def markdown_to_html(md_text):
    return markdown.markdown(md_text)

def generate_page(content_path, template_path, output_path, basepath="/"):
    with open(content_path, "r") as f:
        content_md = f.read()

    content_html = markdown_to_html(content_md)

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(content_md)
    page_html = template.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", content_html)

    # Normalize basepath to end with /
    if basepath != "/":
        if not basepath.endswith("/"):
            basepath += "/"
        page_html = page_html.replace('href="/', f'href="{basepath}')
        page_html = page_html.replace('src="/', f'src="{basepath}')

    with open(output_path, "w") as f:
        f.write(page_html)
