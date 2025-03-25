from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector
from core.utils import get_connection_string, get_embeddings_model


def read_document(file_path):
    loader = TextLoader(file_path)
    return loader.load()


def process_chunks(file_path):
    raw_documents = read_document(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(raw_documents)


def create_embeddings_and_upsert(file_path, collection_name="raptai"):
    documents = process_chunks(file_path)
    connection = get_connection_string()
    embeddings_model = get_embeddings_model()
    return PGVector.from_documents(
        documents, embeddings_model, connection=connection, collection_name=collection_name)
