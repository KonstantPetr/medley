import io
import re

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from get_settings import SetUp


class PDFParser:

    def __init__(self, _pdf_path, _pdf_search_list, pdf_text=None, pdf_out_data_list=None):
        self.pdf_path = _pdf_path
        self.pdf_search_list = _pdf_search_list
        self.pdf_text = pdf_text
        self.pdf_out_data_list = pdf_out_data_list

    def extract_text_from_pdf(self):

        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(self.pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            self.pdf_text = fake_file_handle.getvalue()

        converter.close()
        fake_file_handle.close()

        return self.pdf_text

    def parse_pdf(self):

        self.pdf_out_data_list = []

        for reg_expr_list in self.pdf_search_list:

            try:
                start_pos = re.search(rf'{reg_expr_list[0]}', self.pdf_text).span()[1]
                end_pos = re.search(rf'{reg_expr_list[1]}', self.pdf_text).span()[0]
                self.pdf_out_data_list.append(self.pdf_text[start_pos:end_pos])

            except TypeError or SyntaxError or ValueError:
                self.pdf_out_data_list.append('no_data_found')

        return self.pdf_out_data_list


if __name__ == '__main__':

    set_up = SetUp()
    set_up.get_settings()
    set_up.get_pdf_search_vector()
    set_up.get_pdf_files()
    set_up.get_html_search_vector()

    pdf_out_data_vector = {}
    for pdf_search_list_id in set_up.pdf_search_vector:

        pdf_path = set_up.pdf_paths[pdf_search_list_id]
        pdf_search_list = set_up.pdf_search_vector[pdf_search_list_id]

        pdf_parser = PDFParser(pdf_path, pdf_search_list)
        pdf_parser.extract_text_from_pdf()
        pdf_parser.parse_pdf()
        pdf_out_data_vector[pdf_search_list_id] = pdf_parser.pdf_out_data_list

    print(f'pdf_out_data_vector = {pdf_out_data_vector}')
