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
from langchain.llms import HuggingFaceHub
import pinecone

pinecone.init(api_key="PINECONE_API_KEY")
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

index_name = "langchain-demo"

if index_name not in pinecone.list_indexes():
  
  pinecone.create_index(name=index_name, metric="cosine", dimension=768)
  docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
else:
  
  docsearch = Pinecone.from_existing_index(index_name, embeddings)



template = """
You are a Arya a bot of hostel. These Human will ask you a questions about the hostel. 
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
llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API") 
)


rag_chain = (
  {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
  | prompt 
  | llm 
  | StrOutputParser() 
)
class ChatBot():
  loader = TextLoader('data/hostel_data.txt')
  documents = loader.load()
  rag_chain = (
    {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
    | prompt 
    | llm
    | StrOutputParser() 
  )

bot = ChatBot()
user_input = input("Ask me anything: ")
result = bot.rag_chain.invoke(user_input)
print(result)
