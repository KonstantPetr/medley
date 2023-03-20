import json

from urllib.request import urlretrieve

# файл настроек представляет собой json-файл, содержащий список списков, со следующими составляющими:
# настройки для прямого ввода данных строки - "raw_data"
# настройки для парса html списки - ["URL", "xpath_tag", ("regexp_0", "regexp_1", "replace_match")]
# настройки для парса pdf словари - {"URL": ["regexp_start", "regexp_end"]}


class SetUp:

    def __init__(self, settings=None, pdf_search_vector=None, pdf_paths=None, html_search_vector=None):
        self.settings = settings
        self.pdf_search_vector = pdf_search_vector
        self.pdf_paths = pdf_paths
        self.html_search_vector = html_search_vector

    def get_settings(self):
        with open('settings.json', 'r', encoding='utf-8') as settings_file:
            self.settings = json.load(settings_file)

        return self.settings

    def get_html_search_vector(self):
        self.html_search_vector = []
        for bank_settings in self.settings:
            self.html_search_vector.append([])
            for bank_setting in bank_settings:
                if type(bank_setting) == list:
                    self.html_search_vector[self.settings.index(bank_settings)].append(bank_setting)
                elif type(bank_setting) == dict:
                    self.html_search_vector[self.settings.index(bank_settings)].append('pdf')
                else:
                    self.html_search_vector[self.settings.index(bank_settings)].append('raw_data')

        return self.html_search_vector

    def get_pdf_search_vector(self):
        self.pdf_search_vector = {}
        for bank_settings in self.settings:
            pdf_search_list_for_bank = []
            for bank_setting in bank_settings:
                if type(bank_setting) == dict:
                    pdf_search_list_for_bank += list(bank_setting.values())
            self.pdf_search_vector[self.settings.index(bank_settings)] = pdf_search_list_for_bank

        return self.pdf_search_vector

    def get_pdf_files(self):
        self.pdf_paths = {}
        for bank_settings in self.settings:
            for bank_setting in bank_settings:
                if type(bank_setting) == dict:
                    destination = f'storage/{self.settings.index(bank_settings)}.pdf'
                    url = ''.join(map(str, list((bank_setting.keys()))))
                    urlretrieve(url, destination)
                    self.pdf_paths[self.settings.index(bank_settings)] = destination

        return self.pdf_paths


if __name__ == '__main__':

    set_up = SetUp()
    set_up.get_settings()
    set_up.get_html_search_vector()
    set_up.get_pdf_search_vector()
    set_up.get_pdf_files()

    print(f'html_search_vector = {set_up.html_search_vector}')
    print(f'pdf_search_vector = {set_up.pdf_search_vector}')
    print(f'pdf_paths = {set_up.pdf_paths}')
    print(f'settings = {set_up.settings}')
