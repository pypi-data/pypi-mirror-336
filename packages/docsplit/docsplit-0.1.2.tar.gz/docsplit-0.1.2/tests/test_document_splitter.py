from docsplit.handlers.document_splitter import DocumentHandler

handler = DocumentHandler()
payload = {
    'data': [{
        'doc_id': 'doc1',
        'doc_path': '/home/nikhil/Downloads/UI-2.3 (Medical Certificate) & Salary_Schedule_Form & Service_Letter.pdf',
        'split_format': 'jpg',
        'doc_name': 'doc.pdf'
    }],
    'retain_splitted_documents': True
}

# payload = {
#     'doc_path_list': ['/home/nikhil/Downloads/sample1.heic', '/home/nikhil/Downloads/image.png', '/home/nikhil/Downloads/CV.pdf'],
#     'action': 'merge'
# }

result = handler.process_documents(payload)
# print(result)