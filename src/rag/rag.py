import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.ChromaVectorStore import ChromaVectorStore
import ollama, logging


class Rag:
    def __init__(self):
        self._inicia_logs()
        self.ChromaDB = ChromaVectorStore()
        
        
    def queryllm(self, query):
        """
        Realiza una consulta al modelo de lenguaje.
        
        Args:
            query (str): La consulta que se le hará al modelo de lenguaje.
            
        Returns:
            str: La respuesta del modelo de lenguaje.
        """
        contexto = self.ChromaDB.get_documents(query)
        self.logger.info("Contexto recuperado de la base de datos Chroma.")
        
        prompt = f"Pregunta: {query}\n\nContexto (responde solo sobre el contenido del texto entregado): {contexto}\n\nLa Respuesta siempre en Español"

        respuestalln = ollama.chat(model="llama3", 
                                   messages=[{"role": "system", "content": prompt}],
                                   options={"temperature": 0})
        self.logger.info("Respuesta obtenida del modelo de lenguaje.")
        
        return respuestalln['message']['content']
    
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
# if __name__ == '__main__':
#     llm = rag()
#     query = "Creame un resumen de la Información pública del acuerdo provisional de modificación de la Tasa por prestación del Servicio de Recogida de Basura"

#     respuesta = llm.queryllm(query)

#     print(respuesta)
