from PyPDF2 import PdfFileWriter, PdfFileReader

file_name = input("파일 이름을 입력하세요(확장자 미포함하여 입력): ")
output_file_name = input("변환한 파일 이름은 무엇으로 하시겠어요?(확장자 미포함하여 입력): ")

pdf_file = PdfFileReader(open(file_name + ".pdf", "rb"))
pdf_file_for_left = PdfFileReader(open(file_name + ".pdf", "rb"))
pdf_file_for_right = PdfFileReader(open(file_name + ".pdf", "rb"))
output_pdf_file = PdfFileWriter()

print("total page is", pdf_file.getNumPages())

full_width_size = 0.0
for i in range(pdf_file.getNumPages()):
    page = pdf_file.getPage(i)
    
    if full_width_size < page.mediaBox.upperRight[0].as_numeric():
        full_width_size = page.mediaBox.upperRight[0]

print("full width size is", full_width_size)

for i in range(pdf_file.getNumPages()):
    print("this is", i, "page.")
    print("upperRight is", pdf_file.getPage(i).mediaBox.upperRight[0])
    if(full_width_size != pdf_file.getPage(i).mediaBox.upperRight[0]):
        page = pdf_file.getPage(i)
        output_pdf_file.addPage(page)
        continue

    print("cutting work...")
    # print(pdf_file.getPage(i))
    page_left = pdf_file_for_left.getPage(i)
    page_right = pdf_file_for_right.getPage(i)    
    
    # left
    page_left.cropBox.lowerLeft = (0, 0)
    page_left.cropBox.upperRight = (page_left.mediaBox.upperRight[0] / 2, page_left.mediaBox.upperRight[1])
    output_pdf_file.addPage(page_left)

    # right
    page_right.cropBox.lowerLeft = (page_right.mediaBox.upperRight[0] / 2, 0)
    page_right.cropBox.upperRight = (page_right.mediaBox.upperRight[0], page_right.mediaBox.upperRight[1])
    output_pdf_file.addPage(page_right)

output_stream = open(output_file_name + ".pdf", "wb")
output_pdf_file.write(output_stream)
output_stream.close()