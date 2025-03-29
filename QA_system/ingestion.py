from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock

import os
import boto3

# Initialize Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Fetch available models
bedrock_model_client = boto3.client("bedrock", region_name="us-east-1")
available_models = bedrock_model_client.list_foundation_models()["modelSummaries"]

# Filter models that support text embedding
embedding_models = [model["modelId"] for model in available_models if "embed" in model["modelId"]]

# Select an appropriate model or default to a known one
MODEL_ID = "amazon.titan-embed-text-v2:0"

  # Already granted access


# Initialize Bedrock embeddings
bedrock_embeddings = BedrockEmbeddings(model_id=MODEL_ID, client=bedrock)

def data_ingestion():
    """Loads PDF documents and splits them into text chunks."""
    loader = PyPDFDirectoryLoader("./data")
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    return docs

def get_vector_store(docs):
    """Creates FAISS vector store and saves locally."""
    vector_store_faiss = FAISS.from_documents(docs, bedrock_embeddings)
    vector_store_faiss.save_local("faiss_index")
    return vector_store_faiss

if __name__ == "__main__":
    docs = data_ingestion()
    get_vector_store(docs)
