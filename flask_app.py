from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import pinecone

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('API_KEY_PINECONE'),
    environment='gcp-starter'
)

# Data loading and splitting
loader = TextLoader('data/hostel_data.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
docs = text_splitter.split_documents(documents)

# Create embeddings and index in Pinecone
embeddings = HuggingFaceEmbeddings()
index_name = "arya-data-base"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, metric="cosine", dimension=768)
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
else:
    docsearch = Pinecone.from_existing_index(index_name, embeddings)

# Set up LLM from HuggingFace
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=repo_id, 
    model_kwargs={"temperature": 0.8, "top_k": 50}, 
    huggingfacehub_api_token=os.getenv('HUGGING_FACE_API')
)

# Prompt template
template = """
You are a Hostel warden. Humans will ask you questions about the Arya Bhatt Hostel. 
Use the following context to answer the question. 
If you don't know the answer, just say you don't know. 
Keep the answer within 1 sentence and concise.

Question: {question}
Answer:
"""
prompt = PromptTemplate(
    template=template, 
    input_variables=["context", "question"]
)

# RAG chain
rag_chain = (
    {"context": docsearch.as_retriever(), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    
    # Get response from the bot using the RAG chain
    response = rag_chain.invoke(user_input)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
