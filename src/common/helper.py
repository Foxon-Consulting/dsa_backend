from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.llms import CTransformers
import os


# Extract text from PDF
def load_pdf(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    return documents


# Generate directory tree
def generate_tree(starting_directory):
    tree = ""
    for root, directories, files in os.walk(starting_directory):
        tree += f"Directory: {root}\n"

    if tree == "":
        raise ValueError("The directory is empty")

    return tree


# Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=20
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# Download embedding model
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings


# Models factory
def gpt4():
    return ChatOpenAI()


def llama2_chat():
    return CTransformers(
        model="../../models/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        config={"max_new_tokens": 512, "temperature": 0.8},
    )


def llm_factory(llm_name):
    if llm_name == "GPT-4":
        return gpt4()
    elif llm_name == "llama2-chat":
        return llama2_chat()
    else:
        raise ValueError(f"Unknown LLM: {llm_name}")
