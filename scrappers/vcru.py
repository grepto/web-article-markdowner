from slugify import slugify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

CHROME_BINARY_LOCATION = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROME_WEBDRIVER_LOCATION = '/Applications/chromedriver'


def get_content_vcru(page_url: str) -> tuple:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = CHROME_BINARY_LOCATION

    driver = webdriver.Chrome(executable_path=CHROME_WEBDRIVER_LOCATION, options=chrome_options)
    driver.get(page_url)

    content_images = driver.find_elements_by_class_name('content-image')  # Скролим страницу чтобы JS сгенерил img тэги
    actions = ActionChains(driver)
    for content_image in content_images:
        actions.move_to_element(content_image).perform()

    page = driver.page_source
    driver.close()

    soup = BeautifulSoup(page, 'html.parser')

    removing_tags = [soup.find('div', class_='layout--a l-flex l-fa-center l-mv-20'),
                     soup.find('div', class_='content__write-suggestion'),
                     soup.find('div', class_='andropov_tweet andropov_tweet--instagram'), ]
    removing_tags.extend(soup.findAll(lambda tag: tag.name == 'div' and (not tag.contents or tag.contents == ['\n'])))

    for tag in removing_tags:
        if tag:
            tag.decompose()

    header_html = soup.find("h1", {"class": "content-header__title"})
    content_html = soup.find('div', {'class': 'content content--full'})

    source_tag = soup.new_tag('p')
    source_tag.string = 'Первоисточник: '
    link_tag = soup.new_tag('a', href=page_url)
    link_tag.string = soup.find('title').get_text()
    source_tag.insert(1, link_tag)

    result_html = f'{source_tag}{header_html}{content_html}'

    slug = slugify(header_html.get_text())

    return slug, result_html
