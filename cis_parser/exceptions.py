class CISParserException(Exception):
    pass


class ParseMachineException(CISParserException):
    pass


class PDFParsingException(ParseMachineException):
    pass


class BadPDFException(PDFParsingException):

    def __str__(self):
        return 'Something wrong with PDF file'


class InvalidSearchInPDFException(PDFParsingException):

    def __str__(self):
        return 'Something wrong with searching process in PDF file'


class NoPDFFileException(PDFParsingException):

    def __str__(self):
        return 'There is no such PDF file'


class HTMLParsingException(ParseMachineException):

    def __str__(self):
        return 'There is something wrong with html parsing'


if __name__ == '__main__':
    pass
