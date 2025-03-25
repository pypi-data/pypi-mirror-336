from langchain_core.runnables import chain
from core.utils import get_llm
from services.generation_service import generate_fusion_query
from services.prompt_service import prepare_prompt
from services.retrieval_service import get_fusion_retriever_chain


def user_query():
    return 'Difference between quantum computing and classical computing?'


collection_name = 'quantum_computing'


@chain
def qa(input):
    query_gen = generate_fusion_query()
    retrieval_chain = get_fusion_retriever_chain(collection_name, query_gen)

    docs = retrieval_chain.invoke(input)

    # prepare prompt
    prompt = prepare_prompt()
    # format prompt
    formatted = prompt.invoke({"context": docs, "question": input})

    llm = get_llm()
    # generate answer
    answer = llm.invoke(formatted)
    return answer


# run it
result = qa.invoke(user_query())
print(result.content)
