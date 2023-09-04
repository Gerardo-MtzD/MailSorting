import PyPDF2
import json
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfFileReader

class get_pdf:
    def __init__(self,pdf,drop_names):
        self.read_pdf=PdfFileReader(open(pdf,"rb"))
        self.pdf_text=self.read_pdf.getDocumentInfo()
        print(self.pdf_text)
        self.drop_names=drop_names
        if self.pdf_text == None:
            self.drop_names=pdf
        self.get_info()
        print(self.drop_names)

    def get_info(self):
        print('P')
