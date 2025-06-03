import re

def extract_markdown_images(text):
    """
    Extracts markdown image syntax: ![alt text](url)
    Returns a list of (alt, url) tuples.
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    """
    Extracts markdown link syntax: [anchor text](url)
    Returns a list of (anchor, url) tuples.
    Does not match image links.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

