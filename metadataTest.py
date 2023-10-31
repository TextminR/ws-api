import PyPDF2

pdf_file_path = 'docs/test.pdf'
dict_text = {}

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(open(pdf_file_path, 'rb'))
print(pdf_reader.metadata.creation_date_raw)

pdf_reader.stream.close()