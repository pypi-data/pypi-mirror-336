import os
from typing import Iterator, Union, Type, Callable

from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import UnstructuredFileLoader, BSHTMLLoader, CSVLoader

FILE_LOADER_TYPE = Union[
    Type[UnstructuredFileLoader], Type[TextLoader], Type[BSHTMLLoader], Type[CSVLoader]
]


def load_folder_recursively(path: str, files_regex, loader_cls: FILE_LOADER_TYPE = TextLoader):
    return load_folder_recursively_with_metadata(path, files_regex, None, loader_cls)


def load_folder_recursively_with_metadata(path: str, files_regex, metadata_fn: Callable[[Document], Document] = None,
                                          loader_cls: FILE_LOADER_TYPE = TextLoader):
    documents = []

    for root, dirs, files in os.walk(path, topdown=True):
        loader = DirectoryLoader(root, glob=files_regex, loader_cls=loader_cls, loader_kwargs={'encoding': 'utf-8'})
        folder_docs = loader.load()
        for doc in folder_docs:
            if metadata_fn is not None:
                doc = metadata_fn(doc)
            documents.append(doc)
        for dir_name in dirs:
            load_folder_recursively_with_metadata(os.path.join(root, dir_name), files_regex, loader_cls)

    return documents


def load_folder(path: str, files_regex, loader: FILE_LOADER_TYPE = TextLoader):
    return load_folder_with_metadata(path, files_regex, None, loader)


def load_folder_with_metadata(path: str, files_regex, metadata_fn: Callable[[Document], Document] = None,
                              loader: FILE_LOADER_TYPE = TextLoader):
    documents = []

    loader = DirectoryLoader(path, glob=files_regex, loader_cls=loader, loader_kwargs={'encoding': 'utf-8'})
    folder_docs = loader.load()
    for doc in folder_docs:
        if metadata_fn is not None:
            doc = metadata_fn(doc)
        documents.append(doc)

    return documents


def split_documents(documents: Iterator[Document], chunk_size=1000, chunk_overlay=200):
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=chunk_size, chunk_overlap=chunk_overlay)
    chunks = text_splitter.split_documents(documents)

    print(f"{len(chunks)} documents splitted.")
    return chunks


def create_splitter(chunk_size=1000, chunk_overlay=200):
    return CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlay)


def add_metadata(documents: Iterator[Document], key: str, value):
    for doc in documents:
        doc.metadata[key] = value
    return documents


def load_single(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    loaded_docs = loader.load()
    return loaded_docs[0]


def read_file_to_string(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def remove_duplicates_by_property(objects, property_name):
    seen = set()
    unique_objects = []
    for obj in objects:
        value = getattr(obj, property_name, None)
        if value not in seen:
            seen.add(value)
            unique_objects.append(obj)
    return unique_objects
