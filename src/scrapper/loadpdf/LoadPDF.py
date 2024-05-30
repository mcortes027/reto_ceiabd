from langchain_community.document_loaders import PyPDFLoader
from tqdm import tqdm
import os, logging

class LoadPDF:
    """
    Clase que convierte archivos PDF a texto
    """
    
    def __init__(self, carpeta_pdf='../data_default', bloque_datos=10000):
        
        self._inicia_logs()
        
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
        start_index = self.current_index
        end_index = min(self.current_index + self.bloque_datos, len(self.pdf_files)) # Evitar desbordamiento
        pdf_texts = []

        for i in tqdm(range(start_index, end_index)):
            pdf_file = self.pdf_files[i]
            # if not bd.get_cargado(pdf_file): <--------------------------------------------------------------------- TODO
            try:
                loader = PyPDFLoader(pdf_file)
                pdf_texts.append(loader.load())
                # bd.set_cargado(pdf_file)     <--------------------------------------------------------------------- TODO
            except Exception as e:
                self.errores.append((pdf_file, str(e)))

        self.current_index = end_index
        return pdf_texts 
        
    def load_bloque(self):
        """
        Ejecutar la carga en bloques hasta completar todos los archivos
        
        Como tenemos control de ficheros cargados, cada vez que se ejecute 
        este método se cargará el siguiente bloque
        """
        texts = self._load_()
        
        self.logger.info(f'Procesado bloque hasta índice: {self.current_index}')
        return texts
    
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
                
    def _inicia_logs(self):
        """
        Inicializa los registros de log.

        Crea un directorio de registros llamado "Log_System" si no existe.
        Configura el registro de eventos en un archivo llamado "system.log" dentro del directorio de registros.
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


# Ejemplo de uso:
#if __name__ == '__main__':
    # loader = LoadPDF(carpeta_pdf='../data', bloque_datos=10)
    # docs = loader.load_bloque()
    # print(f'Número de errores: {loader.count_errors()}')
    # loader.show_errors()
    # print(f'Número de documentos cargados: {len(docs)}')
    # print(f'Número de archivos PDF en la carpeta: {len(loader.pdf_files)}')
    #print(docs[0])
