
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection_string():
    return os.environ.get("CONNECTION_STRING")


def get_embeddings_model():
    return OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))


def get_llm():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=os.environ.get("OPENAI_API_KEY"))
