import os

from exceptions import NoPDFFileException
from get_settings import SetUp


def clear_pdf(pdf_paths):
    for pdf_path in pdf_paths:
        if os.path.isfile(pdf_paths[pdf_path]):
            os.remove(pdf_paths[pdf_path])
        else:
            raise NoPDFFileException


def format_currency(out_data):

    for i, bank_data in enumerate(out_data):
        for out_key in bank_data:
            if type(bank_data[out_key]) == list:
                for k, elem in enumerate(out_data[i][out_key]):
                    out_data[i][out_key][k] = out_data[i][out_key][k].replace('₸', 'KZT')
            else:
                out_data[i][out_key] = out_data[i][out_key].replace('₸', 'KZT')

    return out_data


def format_types(out_data):

    for i, bank_data in enumerate(out_data):
        for bank_data_unit_id in bank_data:
            if type(bank_data[bank_data_unit_id]) == list and len(bank_data[bank_data_unit_id]) == 1:
                out_data[i][bank_data_unit_id] = str(bank_data[bank_data_unit_id][0])
        if len(out_data[i]['time_opening'].split()) != 1:
            out_data[i]['time_opening'] = out_data[i]['time_opening'].split()
        out_data[i]['terms_reg'] = \
            {'time_opening': out_data[i]['time_opening'], 'description': out_data[i]['description']}
        out_data[i].pop('time_opening', 'description')

    return out_data


if __name__ == '__main__':

    set_up = SetUp()
    set_up.get_settings()
    set_up.get_html_search_vector()
    set_up.get_pdf_search_vector()
    set_up.get_pdf_files()

    print(f'html_search_vector = {set_up.html_search_vector}')
    print(f'pdf_search_vector = {set_up.pdf_search_vector}')
    print(f'pdf_paths = {set_up.pdf_paths}')

    clear_pdf(set_up.pdf_paths)
