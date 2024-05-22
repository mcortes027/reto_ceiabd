import time
from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm import tqdm
import os

class ScrapperBOC:
    """
    Clase para descargar documentos del Boletín Oficial de Cantabria (BOC).

    Args:
        url_base_boc (str): La URL base del BOC.

    Attributes:
        _url_base_boc (str): La URL base del BOC.
        _error_descarga (list): Lista de URLs que fallaron al descargar.
        _path (str): Ruta de directorio para guardar los archivos descargados.
        _tiempo_total (float): Tiempo total de descarga en minutos.
        _procesos (int): Número de procesos concurrentes para la descarga.
        _boc_start (int): Número de documento inicial.
        _boc_end (int): Número de documento final.
        _paciencia (int): Número de errores permitidos antes de detener la descarga.
        
    Methods:
        _check_url(url): Verifica si una URL es válida.
        _download_document(url, file_path): Descarga un documento desde una URL y lo guarda en un archivo.
        _process_url(i): Procesa una URL para descargar el documento correspondiente.
        run(start, end): Ejecuta la descarga de documentos en un rango específico.
        continua_download(cuantos): Continúa la descarga de archivos desde el último descargado.
        tiempo_de_descargar(): Obtiene el tiempo total de descarga.
        get_error_descarga(): Obtiene la lista de URLs que fallaron al descargar.
        last_download(): Obtiene el último documento descargado.

    """

    def __init__(self, url, procesos=10, carpeta='default_boc', start=1, end=1, paciencia=20):
        """
        Constructor de la clase BocDownloader.
        
        Args:
            url (_type_): URL base del BOC.
            procesos (int, optional): Numero de procesos concurrentes. Por defecto es 10.
            carpeta (str, optional): Ruta de directorio para guardar los archivos descargados. Por defecto es 'default_boc'.
            start (int, optional): Número de documento inicial. Por defecto es 1.
            end (int, optional): Número de documento final. Por defecto es 1.
            paciencia (int, optional): Número de errores permitidos antes de detener la descarga. Por defecto es 20.
        """
        self._url_base_boc = url
        self._error_descarga = []
        self._path = carpeta
        self._tiempo_total = 0
        self._procesos = procesos
        self._boc_start = start
        self._boc_end = end
        self._paciencia = paciencia
    
    def _check_url(self, url):
        """
        Verifica si una URL es válida.

        Args:
            url (str): La URL a verificar.

        Returns:
            bool: True si la URL es válida, False en caso contrario.
        """
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _download_document(self, url, file_path):
        """
        Descarga un documento desde una URL y lo guarda en un archivo.

        Args:
            url (str): La URL del documento a descargar.
            file_path (str): La ruta del archivo donde se guardará el documento.
        """
        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)


    def _process_url(self, i):
        """
        Procesa una URL para descargar el documento correspondiente.

        Args:
            i (int): El número de documento a descargar.
        """
        if self._check_url(self._url_base_boc + str(i)):
            self._download_document(self._url_base_boc + str(i), f"{self._path}/boc_{i}.pdf")
        else:
            self._error_descarga.append(self._url_base_boc)
        
         # Si hay más de 20 errores, lanza una excepción
        if len(self._error_descarga) > self._paciencia:
            raise Exception(f"Más de {self._paciencia} errores en la descarga. Deteniendo la descarga.")

            
    
    def run(self):
        """
        Ejecuta la descarga de documentos en un rango específico.

        Args:
            start (int): El número de documento inicial.
            end (int): El número de documento final.
        """
        if not os.path.exists(self._path):
            os.makedirs(self._path)
            
        self._error_descarga.clear() #limpia la lista de errores
        
        self._tiempo_total = 0
        
        tiempo_inicio = time.time()
  
        try:
            with ThreadPoolExecutor(max_workers=self._procesos) as executor:
                list(tqdm(executor.map(self._process_url, range(self._boc_start, self._boc_end)), initial=self._boc_start, total=self._boc_end-1))
        except Exception as e:
            print(f"Error: {e}")
        
        tiempo_final = time.time()

        self._tiempo_total = (tiempo_final - tiempo_inicio)
        
        if len(self._error_descarga) != 0:
            print(f"Descargas fallidas: {self._error_descarga}")
    
    def continua_download(self, cuantos=1000):
        """
        Continúa la descarga de archivos desde el último descargado.

        Este método se utiliza para continuar la descarga de archivos desde el último archivo descargado. 
        Toma como parámetro opcional 'cuantos', que indica el número de archivos a descargar a partir del último descargado.

        Parámetros:
        - cuantos (int): El número de archivos a descargar. Por defecto es 1000.

        """
        self._boc_start = self.last_download() + 1
        self._boc_end = self._boc_start + cuantos
        
        self.run()
            
    #----------- Métodos para obtener información de la descarga ------------
    
    def tiempo_de_descargar(self):
        """
        Obtiene el tiempo total de descarga.

        Returns:
            float: El tiempo total de descarga en minutos.
        """
        if self._tiempo_total == 0:
            return "No se ha descargado ningún documento.", None
        elif self._tiempo_total < 60: #segundos
            return round(self._tiempo_total,2), 'seg'
        elif self._tiempo_total < 3600: #minutos
            return round(self._tiempo_total/60,2), 'min'
        elif self._tiempo_total < 86400: #horas
            return round(self._tiempo_total/3600,2), 'horas'
        elif self._tiempo_total < 2592000: #días
            return round(self._tiempo_total/86400,2), 'días'
    
    def get_error_descarga(self):
        """
        Obtiene la lista de URLs que fallaron al descargar.

        Returns:
            list: La lista de URLs que fallaron al descargar.
        """
        return self._error_descarga
    
    def last_download(self):
        """
        Obtiene el último documento descargado.

        Returns:
            int: El número del último documento descargado.
        """
        return len(os.listdir(self._path))
    
    
    
def main():
    url_base_boc = "https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob="
    bocdown = ScrapperBOC(url_base_boc,procesos=20, carpeta='./data', start=1, end=10000)
    bocdown.run()
    tiempo, unidad = bocdown.tiempo_de_descargar()
    print(f"Tiempo total: {tiempo} {unidad} y se han descargado {bocdown.last_download()} documentos.") 
    
    # Continuar la descarga
    bocdown.continua_download(10000)
    tiempo, unidad = bocdown.tiempo_de_descargar()
    print(f"Tiempo total: {tiempo} {unidad} y se han descargado {bocdown.last_download()} documentos.")
    

if __name__ == "__main__":
    main()
    