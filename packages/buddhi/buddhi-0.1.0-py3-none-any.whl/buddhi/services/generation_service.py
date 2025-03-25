

from langchain_postgres import PGVector
from core.utils import get_llm
from services.prompt_service import get_hyde_prompt, get_perspectives_prompt, get_fusion_rag_prompt
from services.retrieval_service import parse_queries_output
from langchain_core.output_parsers import StrOutputParser


def generate_query():
    prompt = get_perspectives_prompt()
    llm = get_llm()

    query_gen = prompt | llm | parse_queries_output
    return query_gen


def generate_fusion_query():
    prompt = get_fusion_rag_prompt()
    llm = get_llm()

    query_gen = prompt | llm | parse_queries_output
    return query_gen


def generate_hyde_query():
    prompt = get_hyde_prompt()
    llm = get_llm()

    query_gen = prompt | llm | StrOutputParser()
    return query_gen
