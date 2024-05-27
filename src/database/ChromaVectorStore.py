from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama, chromadb

class ChromaVectorStore:
    def __init__(self, host="localhost", port=8000, collection_name="default"):
        self.host = host
        self.port = port
        self.collection_name = collection_name

        self.vectorstore = None
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1024, chunk_overlap=0, length_function=len)

        
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """
        Inicializa la base de datos Chroma.

        Este método se utiliza para inicializar la base de datos Chroma. 
        Establece una conexión con el servidor de Chroma utilizando el host y el puerto especificados.
        Si la conexión es exitosa, se crea una instancia de Chroma y se asigna a la variable vectorstore.
        La función de embedding especificada también se asigna a la instancia de Chroma.

        Raises:
            ValueError: Si no se puede conectar al servidor de Chroma.

        """
        try:
            self.client = chromadb.HttpClient(host=self.host, port=self.port)
            print("Conexión exitosa con el servidor de Chroma") #Logging
            self.vectorstore = Chroma(client=self.client, embedding_function=self.embeddings)
            print("Base de datos Chroma inicializada.") #Logging
        except ValueError:
            print("Error: No se pudo conectar al servidor de Chroma.") #Looging
            print(ValueError) #Logging
                
            

    def add_documento(self, documento):
        """
        Añade un documento a la base de datos Chroma, dividiendo el documento en chunks.

        Parámetros:
        - documento: El documento que se va a añadir a la base de datos Chroma.

        """
        try:
            docs_chuncks = self.text_splitter.split_documents(documento)
            print("Documento dividido en chunks.") #Logging
            self.vectorstore = Chroma.from_documents(documents=docs_chuncks, embedding=self.embeddings, client=self.client)
            print("Documento añadido a la base de datos Chroma.") #Logging
        except ValueError:
            print("Error al añadir el documento a la base de datos Chroma.") #Logging
            print(ValueError) #Logging
    
    def add_list_documentos(self, documentos):
        """
        Añade una lista de documentos a la base de datos Chroma.
        """
        for documento in documentos:
            self.add_documento(documento)
    
     
    def _combine_docs(self, docs):
        """
        Combina los documentos en una sola cadena de texto.

        Args:
            docs (list): Una lista de documentos.

        Returns:
            str: La cadena de texto que contiene la combinación de los documentos.
        """
        combined_docs = ""
        for doc in docs:
            combined_docs += doc.page_content + "\n"
        return combined_docs.rstrip('\n')
    
    def get_documents(self, query):
        """
        Devuelve los documentos que coinciden con la query en un solo string, que sera el que pasemos al modelo LLM.
        Es decir esta función es la que le da el constexto al LLM.
        """        
        retrieved_docs = self.vectorstore.as_retriever().invoke(query)
        return self._combine_docs(retrieved_docs)
    
        

                
#ejemplo de uso
# chromavector = ChromaVectorStore()


# loader = PyPDFLoader('./src/database/boc_7.pdf')
# paginas = loader.load()

# chromavector.add_documento(paginas)

# text = chromavector.get_documents("Información pública del acuerdo provisional de modifica-ción de la Tasa por prestación del Servicio de Recogidade Basura")

# print(text)

