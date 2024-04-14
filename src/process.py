from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

def createConversationChain(vectordb):
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    llm = HuggingFaceEndpoint(
        repo_id=repo_id, max_length=128, temperature=0.3, token="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"
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    template = """
    Answer the Question only based on the context provided. If the answer is not found in the context, just say 'Information Not Available'
    Question: \n{question}\n
    Context : \n{context}\n

    Answer: """
    prompt = PromptTemplate.from_template(template)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain


def getVectorStore(chunks):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb  = Chroma.from_texts(chunks, embedding_function)
    return vectordb

def getChunks(text):
    print(text)
    text_splitter = CharacterTextSplitter(
        separator=".", 
        chunk_size=400, 
        chunk_overlap=50,
    )
    chunks = text_splitter.split_text(text)
    return chunks
