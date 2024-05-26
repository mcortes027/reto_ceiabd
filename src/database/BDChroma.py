import chromadb
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class CustomEmbeddingFunction:
    def __init__(self, model_name):
        self.embedding_model = OllamaEmbeddings(model=model_name)

    def __call__(self, input):
        return self.embedding_model.embed(input)

class BDChroma:
   def __init__(self, host, port, collection_name):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client = None
        self._init_conexion()
        
        self.retriever = None
        self.embedding = CustomEmbeddingFunction(model_name="llama3")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=128)
        
        self.create_collection(self.collection_name)
        
   def _init_conexion(self):
      
      try:
         self.client = chromadb.HttpClient(host=self.host, port=self.port)
         #print("Conexión exitosa con el servidor de Chroma")
      except ValueError:
         print("Error: No se pudo conectar al servidor de Chroma.")
   
   def is_collection_exists(self, collection_name):
      
      collections = self.client.list_collections()
      for collection in collections:
         if collection.name == collection_name:
               return True
      return False
   
   def create_collection(self, collection_name):
      
      if not self.is_collection_exists(collection_name):
         self.client.create_collection(collection_name, embedding_function=self.embedding)
         print(f"La colección {collection_name} ha sido creada.")
      else:
         print(f"La colección {collection_name} ya existe.")
         
   def delete_collection(self, collection_name):
      
      if self.is_collection_exists(collection_name):
         self.client.delete_collection(collection_name)
         print(f"La colección {collection_name} ha sido eliminada.")
      else:
         print(f"La colección {collection_name} no existe.")
         
   def __str__(self) -> str:
      if self.client is None:
         return f"Host: {self.host}, Port: {self.port}, Collection: {self.collection_name}, Conexión: No establecida"

      
      return f"Host: {self.host}, Port: {self.port}, Collection: {self.collection_name} ->> {self.is_collection_exists(self.collection_name)}"
   
   def add_document(self, document):
      
      if self.is_collection_exists(self.collection_name):
         collection = self.client.get_or_create_collection(self.collection_name)
         
         if collection is not None:
      
            chunks = self.splitter.split_text(document.page_content)

            # Crear una lista de documentos a partir de los fragmentos
            docs = [Document(page_content=chunk, metadata=document.metadata) for chunk in chunks]

            # Añadir cada fragmento a la colección
            for doc in docs:
               doc_id = str(hash(doc.page_content))
               collection.add(
                  ids=[doc_id],
                  documents=[doc.page_content],
                  metadatas=[doc.metadata]
               )
            
            print("Documento añadido correctamente.")
         else:
            print("Error: No se pudo obtener la colección.")

        
    
    
    
    
prueba = BDChroma('localhost', 8000, 'chroma_chatBOC')

prueba.add_document("Hola, ¿cómo estás?")






