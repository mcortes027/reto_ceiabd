import sys
import os

# Añade el directorio 'src' al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BDChroma import BDChroma
from scrapper.LoadPDF import LoadPDF

class ChromaVectorStore:
    def __init__(self, host="localhost", port=8000, carpeta_pdf='../data', bloque_datos=2):
        self.host = host
        self.port = port
        self.carpeta_pdf = carpeta_pdf
        self.bloque_datos = bloque_datos
        
        self.vectorstore = None
        
        self.loadPDF = LoadPDF(carpeta_pdf=self.carpeta_pdf, bloque_datos=self.bloque_datos)
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """
        Inicializa la base de datos Chroma.
        """
        try:
            self.vectorstore = BDChroma(collection_name="chatBOC-chroma", host=self.host, port=self.port)
        except:
            print("Error: El servidor de Chroma no está disponible.")

    def add_documents(self):
        """
        Agrega los documentos PDF a la base de datos Chroma.
        """
        pdf_texts = self.loadPDF.load_bloque()
       
        #self.vectorstore.add_documents(pdf_texts)
        
        for pdf_text in enumerate(pdf_texts):
            self.vectorstore.add_documents(pdf_text)
            
            
        
        
#ejemplo de uso
chromavector = ChromaVectorStore()

chromavector.add_documents()