import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from get_settings import SetUp


class HTMLParser:

    def __init__(self, _html_search_list, _driver, _chrome_options, _url_cache, _html_out_data_list=None):
        self.html_search_list = _html_search_list
        self.driver = _driver
        self.chrome_options = _chrome_options
        self.url_cache = _url_cache
        self.html_out_data_list = _html_out_data_list

    def parse_html(self):

        self.html_out_data_list = []

        url = self.html_search_list[0]
        xpath_tag = self.html_search_list[1]

        try:
            if url != self.url_cache:
                self.driver.get(url)
            element = self.driver.find_element('xpath', xpath_tag)
            html_out_data_item = element.text
            if html_out_data_item.find('\n\n') != -1:
                html_out_data_item = html_out_data_item.replace('\n\n', '; ')
            try:
                regexp_0 = self.html_search_list[2]
                regexp_1 = self.html_search_list[3]
                html_out_data_item = re.sub(rf'{regexp_0}', f'{regexp_1}', html_out_data_item)
            except IndexError:
                pass
            try:
                replace_match = self.html_search_list[4]
                html_out_data_item = html_out_data_item.replace(replace_match, 'Полное named_bank:')
            except IndexError:
                pass

        except NoSuchElementException:
            html_out_data_item = 'неизвестно'

        self.html_out_data_list.append(html_out_data_item)

        return self.html_out_data_list


if __name__ == '__main__':

    set_up = SetUp()
    set_up.get_settings()
    set_up.get_html_search_vector()

    html_out_data_vector = {}
    html_out_data_list = []

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=chrome_options)
    url_cache = ''

    for html_search_list_id in set_up.html_search_vector:
        for html_search_list in html_search_list_id:
            if type(html_search_list) == list:
                html_parser = HTMLParser(html_search_list, driver, chrome_options, url_cache)
                html_parser.parse_html()
                html_out_data_list.append(html_parser.html_out_data_list)
                url_cache = html_search_list[0]
            else:
                html_out_data_list.append('raw or pdf')
        html_out_data_vector[set_up.html_search_vector.index(html_search_list_id)] = html_out_data_list

    print(f'html_out_data_vector = {html_out_data_vector}')
