import argparse

from md_generator import generate_md_from_url

parser = argparse.ArgumentParser(description='Web-article to markdown converter')
parser.add_argument('url', help='URL for article to need be scrapped and markdowned')
args = parser.parse_args()

if __name__ == '__main__':
    generate_md_from_url(args.url)
