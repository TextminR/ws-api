# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline
# import PyPDF2
#
#
# def extractFromPDF(pdf):
#     dict_text = []
#
#     # Create a PDF reader object
#     pdf_reader = PyPDF2.PdfReader(pdf.file)
#     # print(pdf_reader.metadata.author)
#
#     # Initialize an empty string to store the extracted text
#     pdf_text = ''
#
#     # Iterate through each page in the PDF
#     for page_num in range(len(pdf_reader.pages)):
#         # Extract text from the current page
#         page = pdf_reader.pages[page_num]
#         pdf_text += page.extract_text()
#
#     # Close the PDF file
#     pdf_reader.stream.close()
#
#     tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
#     model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
#
#     nlp = pipeline("ner", model=model, tokenizer=tokenizer)
#
#     # ner_results = nlp(pdf_text)
#
#     # split_strings is a list that conatins the seperated strings of the original input.
#     split_strings = pdf_text.split('--')
#
#     # Iterating through every string-element.
#     # enumerate ==> storing strings in dynamicly created variables
#     for i, part in enumerate(split_strings, start=1):
#         fname = ""
#         sname = ""
#         part = part.strip()  # Remove leading/trailing spaces
#         part = part.replace('\n', '')
#         variable_name = f"text{i}"
#
#         ner_results = nlp(part)
#
#         authors = [{'entity': entry['entity'], 'score': entry['score'], 'word': entry['word']} for entry in ner_results
#                    if entry['entity'] in ['B-PER', 'I-PER']]
#
#         for auth in authors:
#             if auth['entity'] == 'I-PER':
#                 sname = sname + auth['word'].replace('##', '')
#             if auth['entity'] == 'B-PER':
#                 fname = auth['word']
#
#         information = {
#             "text": part,
#             "author": fname + " " + sname
#         }
#
#         dict_text.append(information)
#
#     return dict_text
