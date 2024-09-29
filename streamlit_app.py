from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
import os
from langchain.vectorstores import Pinecone
import pinecone
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from huggingface_hub import InferenceClient
from langchain import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import streamlit as st
load_dotenv()

loader = TextLoader('data/hostel_data.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=4)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings()

pinecone.init(
    api_key= os.getenv('API_KEY_PINECONE'),
    environment='gcp-starter'
)

index_name = "arya-data-base"

if index_name not in pinecone.list_indexes():
  pinecone.create_index(name=index_name, metric="cosine", dimension=768)
  docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
else:
  docsearch = Pinecone.from_existing_index(index_name, embeddings)




repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
  repo_id=repo_id, 
  model_kwargs={"temperature": 0.8, "top_k": 50}, 
  huggingfacehub_api_token=os.getenv('HUGGING_FACE_API')
)

template = """
You Hostel warden. These Human will ask you a questions about the Arya Bhatt Hostel. 
Use following piece of context to answer the question. 
If you don't know the answer, just say you don't know. 
Keep the answer within 1 sentences and concise.

Question: {question}
Answer: 

"""

prompt = PromptTemplate(
  template=template, 
  input_variables=["context", "question"]
)

rag_chain = (
  {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
  | prompt 
  | llm
  | StrOutputParser() 
)

class ChatBot():
  load_dotenv()
  loader = TextLoader('data/hostel_data.txt')
  documents = loader.load()

  rag_chain = (
    {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
    | prompt 
    | llm
    | StrOutputParser() 
  )

bot = ChatBot()

st.set_page_config(page_title="Arya AI")
with st.sidebar:
    st.title('Arya-AI (Offical Bot of Arya-Bhatt Hostel)')

def generate_response(input):
    result = bot.rag_chain.invoke(input)
    return result

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, This is ARYA Developed and Maintain by Himanshu Gangwar"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer from my Data Base ."):
            response = generate_response(input) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)