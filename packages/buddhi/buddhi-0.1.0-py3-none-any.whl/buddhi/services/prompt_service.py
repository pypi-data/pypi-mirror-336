
from langchain_core.prompts import ChatPromptTemplate


def prepare_prompt():
    # format prompt
    prompt = ChatPromptTemplate.from_template(
        """Answer the question based only on the following context: {context} Question: {question} """
    )
    return prompt


def get_perspectives_prompt():
    prompt = ChatPromptTemplate.from_template("""You are an AI language 
    model assistant. Your task is to generate five different versions of the 
    given user question to retrieve relevant documents from a vector database. 
    By generating multiple perspectives on the user question, your goal is to 
    help the user overcome some of the limitations of the distance-based 
    similarity search. Provide these alternative questions separated by 
    newlines. Original question: {question}""")

    return prompt


def get_fusion_rag_prompt():

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant that generates multiple search queries 
        based on a single input query. \n Generate multiple search queries 
        related to: {question} \n Output (4 queries):""")
    return prompt


def get_hyde_prompt():
    prompt = ChatPromptTemplate.from_template(
        """Please write a passage to answer the question.\n Question: {question} \n Passage:""")
    return prompt
