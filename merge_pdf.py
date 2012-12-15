from pyPdf import PdfFileWriter, PdfFileReader
from subprocess import *
import sys
import os

output = PdfFileWriter()
input1 = PdfFileReader(file(sys.argv[1], "rb"))

watermark_text_start = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
watermark_text = ""

# print the title of document1.pdf
print "title = %s" % (input1.getDocumentInfo().title)

if(len(input1.getDocumentInfo().title)>0):
    watermark_text = input1.getDocumentInfo().title
else:
    pdf_contents = Popen(["pdftotext", sys.argv[1], "-"], stdout=PIPE).communicate()[0]
    (watermark_text, watermark_text_mid, watermark_text_post) = pdf_contents.partition("\n")

watermark_result = watermark_text_start + watermark_text + ": http://quiteconfused.dyndns.org/" + watermark_text.replace(" ", "_") + ".tar.gz"

print "Watermark Result: %s" % watermark_text

watermark_file = file("watermark.txt", "wb")
watermark_file.write(watermark_result)
watermark_file.close()


result = Popen(["python", "./text2pdf.py", "./watermark.txt", "-o", "./watermark.pdf"], stdout=PIPE).communicate()[0]

watermark = PdfFileReader(file("watermark.pdf", "rb"))

current_page = 0
while(current_page < input1.getNumPages()):
    temp_page = input1.getPage(current_page)
    temp_page.mergePage(watermark.getPage(0))
    output.addPage(temp_page)
    current_page += 1

newfile = file(sys.argv[2], "wb")
output.write(newfile)
newfile.close()
