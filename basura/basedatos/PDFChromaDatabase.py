from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
import ollama
import chromadb
from chromadb.config import Settings

class PDFChromaDatabase:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.client_settings = Settings( chroma_server_host= self.host, chroma_server_http_port= self.port)
        
        self.vectorstore = None
        
        self.embeddings = OllamaEmbeddings(model="llama3")
        
        self.text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1024,
            chunk_overlap=0,
            length_function=len
        )
        
    def connect_to_chroma(self):
        self.vectorstore = Chroma( client_settings=self.client_settings)
        
    def add_pdf_to_database(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        paginas = loader.load()
        docs = self.text_splitter.split_documents(paginas)
        if self.vectorstore is None:
            self.connect_to_chroma()
        self.vectorstore.add_documents(docs, embedding=self.embeddings)
        
    def retrieve_documents(self, question):
        retriever = self.vectorstore.as_retriever()
        retrieved_docs = retriever.invoke(question)
        return self.combine_docs(retrieved_docs)
        
    @staticmethod
    def combine_docs(docs):
        return "\n".join([doc.page_content for doc in docs])

# Uso de la clase
pdf_db = PDFChromaDatabase()

# Agregar un PDF a la base de datos
pdf_db.add_pdf_to_database('./src/database/boc_6.pdf')

# Recuperar documentos relacionados con una pregunta
question = "¿Cuál es la información más relevante?"
formatted_context = pdf_db.retrieve_documents(question)

print(formatted_context)


