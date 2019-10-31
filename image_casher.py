import ssl
import uuid
import os

import requests
import urllib
from PIL import Image
from bs4 import BeautifulSoup


def cash_images(html: str, base_dir: str) -> str:
    WEBP_CONVERT_FORMAT = 'png'
    IMG_DIR = '_img'

    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    ssl._create_default_https_context = ssl._create_unverified_context

    for img in img_tags:
        img_url = img['src']
        img_type = urllib.request.urlopen(img_url).info().get_content_type()
        _, img_ext = img_type.split('/')
        file_name = f'img_{uuid.uuid4().hex}.{img_ext}'
        file_path = os.path.join(IMG_DIR, file_name)
        base_path = os.path.join(base_dir, file_path)
        response = requests.get(img['src'])
        response.raise_for_status()

        os.makedirs(os.path.dirname(base_path), exist_ok=True)
        with open(base_path, 'wb') as file:
            file.write(response.content)

        if img_ext == 'webp':
            im = Image.open(base_path).convert('RGB')
            os.remove(base_path)
            file_name = f'{os.path.splitext(file_name)[0]}.{WEBP_CONVERT_FORMAT}'
            file_path = os.path.join(IMG_DIR, file_name)
            base_path = os.path.join(base_dir, file_path)
            im.save(base_path, WEBP_CONVERT_FORMAT)

        img['src'] = file_path

    return str(soup)
