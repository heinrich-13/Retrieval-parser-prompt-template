from dotenv import load_dotenv
load_dotenv()

from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.retrieval import create_retrieval_chain

def kry_dokumente_van_web(url):
    loader = WebBaseLoader(url)
    loader.requests_kwargs = {'verify':False}
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    splitDocs = splitter.split_documents(docs)

    return splitDocs

def maak_db(docs):
    embedding = OpenAIEmbeddings()
    vectorStore = FAISS.from_documents(docs, embedding)
    return vectorStore

def maak_ketting(vectorStore):
    ollama_klient = ChatOllama(
      model="llama3.2:3b",
      temperature=0.5,
      verbose=True
    )

    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question with accuracy:
    Context: {context}
    Question: {input}
    """)

    chain = create_stuff_documents_chain(
      llm=ollama_klient,
      prompt=prompt
    )

    retriever = vectorStore.as_retriever()
    
    retrievel_chain = create_retrieval_chain(
        retriever,
        chain
    )
    return retrievel_chain
    
docs = kry_dokumente_van_web("https://webactivated.co.za")
vectorStore = maak_db(docs)
chain = maak_ketting(vectorStore)

response = chain.invoke({
    "input": "What is WebActivated?",
})

print(response["context"])