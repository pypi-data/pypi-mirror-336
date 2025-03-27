from langchain.schema import Document


def folder_as_category(doc: Document) -> Document:
    category = doc.metadata['source'].rsplit('/', 2)[-2]
    doc.metadata["category"] = category
    return doc
