from umihico.string import numberize, numberize_int
from umihico.io_ import save_as_txt
from time import sleep
from pprint import pprint
from traceback import print_exc
from skipping_asins import skipping_asins
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
Chrome.xpath = Chrome.find_element_by_xpath
Chrome.xpaths = Chrome.find_elements_by_xpath
import itertools
import sys


def _gen_logined_chrome():
    chrome_options = ChromeOptions()
    # chrome_options.add_argument("--test-type")
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--headless')
    c = Chrome(chrome_options=chrome_options)
    c.get("https://read.amazon.co.jp/notebook")
    for i in itertools.count():
        if len(c.xpaths("//input[@id='ap_email']")) + len(c.xpaths("//input[@id='ap_password']")) == 0:
            break
        sleep(1)
    if c.xpaths("//input[@id='continue' and @type='submit']"):
        c.xpath("//input[@id='continue' and @type='submit']").click()
        for i in itertools.count():
            if not c.xpaths("//input[@name='code' and @type='text']"):
                break
                sleep(1)
                print("waiting your code input.", i, 'seconds')
    return c


def _iter_click_each_pages(c):
    action = ActionChains(c)
    clicked_titles = set()
    increased = True
    while increased:
        increased = False
        h2s = c.xpaths("//div[@id='library-section']//a[.//h2]")
        for h2 in h2s:
            if h2.text not in clicked_titles:
                increased = True
                clicked_titles.add(h2.text)
                h2.click()
                action.move_to_element(h2).perform()
                yield None


def _wait_loading(c):
    sleep(2)
    while len(c.xpaths("//div[@id='annotation-scroller']//div[@class='a-column a-span5']/h3")) == 0:
        sleep(1)
        ("wating...")


def _get_basic_info(c):
    amazon_url = c.xpath(
        "//a[./span/img[@class='kp-notebook-cover-image-border']]").get_attribute('href')
    asin = amazon_url.split('/')[-1]
    amazon_image_url = f"http://images-jp.amazon.com/images/P/{asin}.09.MZZZZZZZ.jpg"
    title, author, date = [
        c.xpaths(
            "//div[@id='annotation-scroller']//div[@class='a-column a-span5']/" + xpath)[i].text
        for xpath, i in zip(["h3", "p", 'span/span'], [0, 1, 0])]
    return amazon_url, asin, amazon_image_url, title, author, date


def _scraping_each(c):
    _wait_loading(c)
    amazon_url, asin, amazon_image_url, title, author, date = _get_basic_info(
        c)
    if asin in skipping_asins:
        print("skipped", title, author)
        return
    elements_increased = True
    action = ActionChains(c)
    highlights = {}
    while elements_increased:
        elements_increased = False
        elements = c.xpaths("//div[@id='kp-notebook-annotations']/div")
        # elements = elements[:len(elements) - 1]
        for e in elements:
            try:
                highlight = ''
                place_num = ''
                highlight = e.find_element_by_xpath(
                    ".//span[@id='highlight']").text
                place_num = numberize_int(
                    e.find_element_by_xpath(".//span[@id='annotationHighlightHeader']").text)
            except (Exception, ) as err:
                (e.text)
                print(err)
            else:
                if place_num not in highlights:
                    elements_increased = True
                    highlights[place_num] = highlight
        action.move_to_element(elements[-1]).perform()
        print("len(highlights)", len(highlights))
        sleep(2)
    data = {
        'amazon_url': amazon_url,
        'asin': asin,
        'amazon_image_url': amazon_image_url,
        'author': author,
        'booktitle': title,
        'date': date,
        'highlights': highlights, }
    pprint(data)
    filename = 'txt/' + asin + '.txt'
    save_as_txt(filename, data)


def scraping(scraping_book_amount=None):
    c = _gen_logined_chrome()
    for i, _ in enumerate(_iter_click_each_pages(c)):
        if i > scraping_book_amount:
            break
        try:
            _scraping_each(c)
        except (Exception, ) as e:
            print_exc()


if __name__ == '__main__':

    scraping_book_amount = int(sys.argv[1]) if len(sys.argv) >= 2 else None
    scraping(scraping_book_amount)
