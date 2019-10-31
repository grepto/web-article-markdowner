import os

import html2text

from scrapper import get_content
from image_casher import cash_images


def generate_md_from_url(page_url: str):
    slug, html = get_content(page_url)

    html = cash_images(html, slug)

    h = html2text.HTML2Text()
    h.body_width = 80
    md_text = h.handle(html)

    with open(os.path.join(slug, f'{slug}.md'), 'w') as md_file:
        md_file.write(md_text)
