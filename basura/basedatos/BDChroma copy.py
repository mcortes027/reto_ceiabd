import requests
from langchain_community.vectorstores import Chroma
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from chromadb.config import Settings


class BDChroma:
    def __init__(self, collection_name, host="localhost", port=8000):
        self.collection_name = collection_name
        self.host = host
        self.port = port
        
        self.embeddings = OllamaEmbeddings(model="llama3")

        self.client_settings = Settings( chroma_server_host= self.host, chroma_server_http_port= self.port)
        self.vectorstore = None
        # self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        #     chunk_size=1024, chunk_overlap=128
        # )
        self.text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1024,
            chunk_overlap=128,
            length_function=len
        )
        
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """
        Inicializa el vectorstore de Chroma si el servidor está disponible.

        Este método inicializa el vectorstore de Chroma si el servidor está disponible. 
        Utiliza la clase Chroma para crear una instancia del vectorstore, pasando el nombre de la colección y la URL del servidor Chroma como parámetros.

        Si el servidor no está disponible, se imprime un mensaje de error.
        """
        if self._is_server_available():
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                client_settings=self.client_settings
            )
            
            print("Conexión exitosa con el servidor de Chroma y la colección creada.")
        else:
            print("Error: El servidor de Chroma no está disponible.")

    def _is_server_available(self):
        """
        Verifica si el servidor de Chroma está disponible.

        Returns:
            bool: True si el servidor está disponible, False en caso contrario.
        """
        try:
            url = f'http://{self.host}:{self.port}/api/v1/databases/default_database'
            response = requests.get(url)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    def add_documents(self, data):
        """
        Divide los documentos y los agrega a la base de datos Chroma.
        """
        print("Agregando documentos a la base de datos Chroma...")

        #if self.vectorstore:
        doc_splits = self.text_splitter.split_documents(data)
        self.vectorstore.add_documents(documents=doc_splits, embedding= self.embeddings)
        print("Documentos agregados con éxito.")
        #    return True
        #else:
        #    print("Error: No se pueden agregar documentos porque el servidor de Chroma no está disponible.")
        #    return False

    def get_retriever(self):
        """
        Devuelve el retriever para la base de datos actual-> (recuperador de documentos)

        Returns:
            El objeto retriever para la base de datos actual si está disponible, None en caso contrario.
        """
        if self.vectorstore:
            return self.vectorstore.as_retriever()
        else:
            print("Error: No se puede obtener el retriever porque el servidor de Chroma no está disponible.")
            return None



# ---------- Uso de la clase BDChroma ----------
# Inicializa la base de datos
bd_chroma = BDChroma(collection_name="chatBOC-chroma")


bd_chroma.add_documents([{"page_content": "Este es un nuevo documento", "metadata": {"source": "source1"}}])

"""
# Agrega documentos a la base de datos
data = [{"content": "Este es un nuevo documento", "metadata": {"source": "source1"}}]
bd_chroma.add_documents(data)

# Recupera el retriever
retriever = bd_chroma.get_retriever()
"""

# import chromadb
# chroma_client = None
# try:
#     chroma_client = chromadb.HttpClient(host="localhost", port=8000)
# except:
#     print("Error: No se puede conectar con el servidor de Chroma.")

# if chroma_client:
#     print("Conexión exitosa con el servidor de Chroma.")


#chroma_db = chromadb.BDChroma(collection_name="rag-chroma")
