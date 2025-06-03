import os
import markdown

def generate_page(content_path, template_path, output_path, basepath="/"):
    with open(content_path, 'r') as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)

    with open(template_path, 'r') as f:
        template = f.read()

    output = template.replace("{{ Title }}", "Your Page Title")
    output = output.replace("{{ Content }}", html_content)

    # Replace absolute paths with basepath to fix links/images on GitHub Pages
    output = output.replace('href="/', f'href="{basepath}')
    output = output.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(output)
