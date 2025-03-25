# DocSplit

A Python package for document splitting and conversion

## Installation

```bash
pip install docsplit
```

## Usage

```python
from docsplit.handlers.document_splitter import DocumentHandler

handler = DocumentHandler()
payload = {
    'data': [{
        'doc_id': 'doc1',
        'doc_path': '/path/to/document.pdf',
        'split_format': 'jpg'
    }],
    'action': 'split'
}

result = handler.process_documents(payload)
```


```python
from docsplit.handlers.document_splitter import DocumentHandler

handler = DocumentHandler()
payload = {
    'doc_path_list': ['/path/to/document1.pdf', '/path/to/document2.pdf'],
    'action': 'merge'
}

result = handler.process_documents(payload)
```

