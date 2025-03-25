
from langchain_postgres.vectorstores import PGVector
from core.document_utils import get_unique_union, reciprocal_rank_fusion
from core.utils import get_connection_string, get_embeddings_model


def get_vectorstore(collection_name):
    vectorstore = PGVector.from_existing_index(
        collection_name=collection_name,
        embedding=get_embeddings_model(),
        connection=get_connection_string()
    )
    return vectorstore


def create_retriever(collection_name):
    db = get_vectorstore(collection_name)
    # create retriever to retrieve 2 relevant document
    return db.as_retriever(search_kwargs={"k": 2})


def parse_queries_output(message):
    return message.content.split('\n')


def retrieve_relevant_documents(collection_name, query: str):
    retriever = create_retriever(collection_name)

    # fetch relevant documents
    docs = retriever.invoke(query)
    return docs


def get_retriever_chain(collection_name, query_gen):
    retriever = create_retriever(collection_name)

    retrieval_chain = query_gen | retriever.batch | get_unique_union
    return retrieval_chain


def get_fusion_retriever_chain(collection_name, query_gen):
    retriever = create_retriever(collection_name)

    retrieval_chain = query_gen | retriever.batch | reciprocal_rank_fusion
    return retrieval_chain


def get_hyde_retriever_chain(collection_name, query_gen):
    retriever = create_retriever(collection_name)

    retrieval_chain = query_gen | retriever
    return retrieval_chain
