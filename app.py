import json
import os
import sys
import boto3
import streamlit as st

from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS

from QA_system.ingestion import data_ingestion, get_vector_store
from QA_system.retrivalandgeneration import get_llama2_llm, get_response_llm

# Initialize AWS Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime")

# ✅ Correct embedding model for FAISS
bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",  
    client=bedrock
)

# ✅ Correct text generation model
def get_llama2_llm():
    llm = Bedrock(
        model_id="amazon.titan-text-express-v1",  # ✅ Use Titan LLM for text generation
        client=bedrock
    )
    return llm

def main():
    st.set_page_config(page_title="QA with Doc")
    st.header("QA with Doc using LangChain and AWS Bedrock")

    user_question = st.text_input("Ask a question from the PDF files:")

    with st.sidebar:
        st.title("Update or Create the Vector Store")

        if st.button("Update Vectors"):
            with st.spinner("Processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("Vector store updated successfully!")

        if st.button("Run LLM Query"):
            if user_question.strip() == "":
                st.warning("Please enter a question before running the model.")
            else:
                with st.spinner("Processing..."):
                    # ✅ Load FAISS index with correct embedding model
                    faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
                    
                    # ✅ Load the correct text generation model
                    llm = get_llama2_llm()
                    
                    # ✅ Get response
                    response = get_response_llm(llm, faiss_index, user_question)
                    st.write(response)
                    st.success("Done!")

if __name__ == "__main__":
    main()
