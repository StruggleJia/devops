import os
from os import walk
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

def get_pdf_list():
    r = []
    for (dirpath, dirnames, filenames) in walk("../input"):
        for i in filenames:
            info = {}
            if i.endswith(".pdf") or i.endswith(".PDF"):
                info['d'] = dirpath
                info['f'] = i
                r.append(info)
    return r

canvas_width = 566
# Create the watermark from an image
c = canvas.Canvas('bin/sample-watermark.pdf')
c.drawImage('../watermarker/logo.png', 0, 0, 612, 792,
            mask='auto', preserveAspectRatio=True)
#c.drawString(canvas_width - 500, 12, "Downloaded from https://diplomate.greybits.in/ - Contributed By Sumit Rawat")
c.save()

# large watermark sample for high res PDFs
# canvas_width = 566
# Create the watermark from an image
# c = canvas.Canvas('bin/sample-watermark--large.pdf')
# c.drawImage('bin/logo.png', canvas_width+int((canvas_width-1200)/2), 100, width=1200, height=1200,
#             mask='auto', preserveAspectRatio=True)
# c.drawString(canvas_width - 500, 12, "Downloaded from https://diplomate.greybits.in/")
# c.save()


right_pdf_list = get_pdf_list()

print("\nRIGHT PDFs : ")
for booklet_name in right_pdf_list:
    try:
        watermark = PdfFileReader(open("bin/sample-watermark.pdf", "rb"), strict=False)
        # large_watermark = PdfFileReader(open("bin/sample-watermark--large.pdf", "rb"))
        output_file = PdfFileWriter()
        input_file = PdfFileReader(open(booklet_name['d'] + "/" + booklet_name['f'], "rb"), strict=False)
        page_count = input_file.getNumPages()

        # Go through all the left-watermarker file pages to add a watermark to them
        for page_number in range(page_count):
            print(booklet_name['f'] + ": Watermarking page {} of {}".format(page_number, page_count - 1))

            input_page = input_file.getPage(page_number)
            # setting a pdf scale to avoid creating different watermarks 
            input_page.scaleTo(width=612,height=792)

            # changing watermark according to PDF size 
            # print(list(input_page.mediaBox))
            # if list(input_page.mediaBox)[3] > 1500:
            #     input_page.mergePage(large_watermark.getPage(0))
            # else:
            #     input_page.mergePage(watermark.getPage(0))
            input_page.mergePage(watermark.getPage(0))
            output_file.addPage(input_page)
        newoutdir = booklet_name['d'].replace("input","output")
        if not os.path.exists(newoutdir):
            os.makedirs(newoutdir)
        with open(newoutdir + "/" + booklet_name['f'], "wb") as outputStream:
            output_file.write(outputStream)
    except Exception as e:
        print(e)
        continue
