import tldextract

from scrappers.vcru import get_content_vcru

SUPPORTED_SITES = {
    'vc.ru': get_content_vcru
}


def get_content(page_url: str) -> tuple:
    _, domain, suffix = tldextract.extract(page_url)
    tld = f'{domain}.{suffix}'

    return SUPPORTED_SITES[tld](page_url)
