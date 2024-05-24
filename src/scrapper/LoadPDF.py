from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from tqdm import tqdm
import os

class LoadPDF:
    """
    Clase que convierte archivos PDF a texto
    """
    
    def __init__(self, carpeta_pdf='../data/pdf', bloque_datos=10000):
        self._path_pdf = carpeta_pdf
        self.bloque_datos = bloque_datos
        
        self.errores = []               # Lista para almacenar errores
        self.pdf_files = []             # Lista de archivos PDF en la carpeta
        self.current_index = 1          # Índice de archivo actual
        self._listar_archivos_pdf()     # Listar archivos PDF en la carpeta
    
    def _listar_archivos_pdf(self):
        """
        Lista todos los archivos PDF en la carpeta y los almacena en la lista self.pdf_files
        """
        archivos = os.listdir(self._path_pdf)
        archivos_pdf = []
        for archivo in archivos:
            if archivo.endswith('.pdf'):
                ruta_completa = os.path.join(self._path_pdf, archivo)
                archivos_pdf.append(ruta_completa)
        self.pdf_files = sorted(archivos_pdf)
        
    def _load_(self):
        """
        Cargamos los archivos PDF de la carpeta en bloques
        """
         # Cargar los siguientes `self.bloque_datos` archivos PDF
        start_index = self.current_index
        end_index = min(self.current_index + self.bloque_datos, len(self.pdf_files)) # Evitar desbordamiento
        pdf_texts = []

        for i in tqdm(range(start_index, end_index)):
            pdf_file = self.pdf_files[i]
            try:
                loader = PyPDFLoader(pdf_file)
                pdf_texts.append(loader.load())
            except Exception as e:
                self.errores.append((pdf_file, str(e)))

        self.current_index = end_index
        return pdf_texts 
        
    def load(self):
        """
        Ejecutar la carga en bloques hasta completar todos los archivos
        
        Como tenemos control de ficheros cargados, cada vez que se ejecute 
        este método se cargará el siguiente bloque
        """
       
        texts = self._load_()
        # Aquí puedes realizar cualquier procesamiento adicional con los textos cargados
        # Por ejemplo, guardarlos en un archivo, enviarlos a otro sistema, etc.
        print(f'Procesado bloque hasta índice: {self.current_index}')
        return texts

    def continua_load(self):
        """
        Continuar cargando desde donde se quedó
        """
        return self._load_()
    
    def count_errors(self):
        """
        Obtener el numero de ficheros con errores de carga
        """
        return len(self.errores)
    
    def show_errors(self):
        """
        Mostrar los errores de carga
        """
        for pdf_file, error in self.errores:
            print(f'Error en archivo: {pdf_file}')
            print(f'Error: {error}')
            print('---')


# Ejemplo de uso:
# loader = LoadPDF(carpeta_pdf='./data', bloque_datos=10)
# docs = loader.load()
# print(f'Número de errores: {loader.count_errors()}')
# loader.show_errors()
