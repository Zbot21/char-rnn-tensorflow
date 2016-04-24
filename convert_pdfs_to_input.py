__author__ = 'chris'

#http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from os import listdir
from os.path import isfile, join
import os


def conv(path):
    try:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        pages = PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)
        for page in pages:
            interpreter.process_page(page)
        fp.close()
        device.close()
        string = retstr.getvalue()
        retstr.close()
        return string
    except:
        return ""

with open("input.txt", "w") as outfile:
    mypath = os.path.join("/", "home", "chris", "docDb", "resources", "pdfs")
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for my_file in onlyfiles:
        pdf_path = os.path.join(mypath, my_file)
        print(pdf_path)
        text = conv(pdf_path)
        outfile.write(text)