from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import chromadb, logging, os

class ChromaVectorStore:
    def __init__(self, host="localhost", port=8000, collection_name="ChatBOC_BD_Vector"):
        
        self._inicia_logs()
        
        self.host = host
        self.port = port
        self.collection_name = collection_name

        self.vectorstore = None
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1024, chunk_overlap=128, length_function=len)

        
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """
        Inicializa la conexión con la base de datos Chroma.

        Inicializa la base de datos Chroma. 
      
        Raises:
            ValueError: Si no se puede conectar al servidor de Chroma.
        """
        try:
            self.client = chromadb.HttpClient(host=self.host, port=self.port)
            self.logger.info("Conexión exitosa con el servidor de Chroma")
            self.vectorstore = Chroma(client=self.client, embedding_function=self.embeddings, collection_name=self.collection_name)
            self.logger.info("Base de datos Chroma inicializada.")
        except ValueError as e:
            self.logger.error("Error: No se pudo conectar al servidor de Chroma.")
            self.logger.error(e)
                
            

    def add_documento(self, documento):
        """
        Añade un documento a la base de datos Chroma, dividiendo el documento en chunks.

        Parámetros:
        - documento: El documento que se va a añadir a la base de datos Chroma.

        """
        try:
            docs_chuncks = self.text_splitter.split_documents(documento)
            self.logger.info("Documento dividido en chunks.")
            self.vectorstore = Chroma.from_documents(documents=docs_chuncks, embedding=self.embeddings, client=self.client, collection_name=self.collection_name)
            self.logger.info("Documento añadido a la base de datos Chroma.")
        except ValueError:
            self.logger.error("Error al añadir el documento a la base de datos Chroma.")
            self.logger.error(ValueError)
    
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
        try:
            retrieved_docs = self.vectorstore.as_retriever().invoke(query)
            self.logger.info("OK - Documentos recuperados de la base de datos Chroma.")
            return self._combine_docs(retrieved_docs)
        except ValueError:
            self.logger.error("Error al recuperar los documentos de la base de datos Chroma.")
            self.logger.error(ValueError)
            return None
    
    def _inicia_logs(self):
        """
        Inicializa los registros de log.

        Crea un directorio de registros llamado "Log_System" si no existe.
        Configura el registro de eventos en un archivo llamado "chroma.log" dentro del directorio de registros.
        Establece el nivel de registro en INFO.
        Utiliza el formato de registro: '%(asctime)s %(levelname)s %(name)s %(message)s'.
        Utiliza el formato de fecha: '%m/%d/%Y %I:%M:%S %p'.
        """
        log_dir = "Log_System"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=os.path.join(log_dir, 'system.log'), 
                            level=logging.INFO, 
                            format='%(asctime)s %(levelname)s %(name)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        
        self.logger = logging.getLogger(__name__)

               
                
#ejemplo de uso
#if __name__ == '__main__':
# chromavector = ChromaVectorStore()
# print(chromavector.client.list_collections())


    #loader = PyPDFLoader('./src/database/boc_7.pdf')
    #paginas = loader.load()

    #chromavector.add_documento(paginas)

    #text = chromavector.get_documents("Información pública del acuerdo provisional de modificación de la Tasa por prestación del Servicio de Recogidade Basura")

    #print(text)

