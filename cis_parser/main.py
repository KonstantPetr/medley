from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from get_settings import SetUp
from html_parse import HTMLParser
from pdf_parse import PDFParser
from out_machine import compose_out_data, dump_to_json
from extensions import clear_pdf, format_currency, format_types


def run_parser():

    # настройка из файла
    set_up = SetUp()
    set_up.get_settings()
    set_up.get_html_search_vector()
    set_up.get_pdf_search_vector()
    set_up.get_pdf_files()

    # парсинг html
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

    # парсинг pdf
    pdf_out_data_vector = {}

    for pdf_search_list_id in set_up.pdf_search_vector:
        pdf_path = set_up.pdf_paths[pdf_search_list_id]
        pdf_search_list = set_up.pdf_search_vector[pdf_search_list_id]

        pdf_parser = PDFParser(pdf_path, pdf_search_list)
        pdf_parser.extract_text_from_pdf()
        pdf_parser.parse_pdf()
        pdf_out_data_vector[pdf_search_list_id] = pdf_parser.pdf_out_data_list

    clear_pdf(set_up.pdf_paths)

    # вывод данных в файл
    out_filename = f'out_data/out{datetime.now().strftime("%d-%m-%Y")}.json'
    out_data = compose_out_data(html_out_data_vector, pdf_out_data_vector, set_up.settings)
    format_currency(out_data)
    format_types(out_data)
    dump_to_json(out_filename, out_data)

    return 'parsing complete'


if __name__ == '__main__':

    # запуск
    print(parsing := run_parser())
