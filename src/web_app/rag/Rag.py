import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from ollama import Client
from ollama import AsyncClient  # Para hacer el cliente asíncrono
from storage.ChromaVectorStore import ChromaVectorStore
import ollama, logging, os


class Rag:
    
    def __init__(self, host_ollama='localhost', port=11434, model="llama3", chroma_host='localhost', asincrono=False):
        self._inicia_logs()
        
        self.ChromaDB = ChromaVectorStore(host=chroma_host, host_Ollama=host_ollama)
        
        self.model = model
        url_ollama = f"http://{host_ollama}:{port}"
        
        if asincrono:
            self.clientOllama = AsyncClient(host=url_ollama)
        else:
            self.clientOllama = Client(host=url_ollama)
        
        
    def queryllm(self, query):
        """
        Realiza una consulta al modelo de lenguaje.
        
        Args:
            query (str): La consulta que se le hará al modelo de lenguaje.
            
        Returns:
            str: La respuesta del modelo de lenguaje.
        """
        try:
            contexto = self.ChromaDB.get_documents(query)
            self.logger.info("Contexto recuperado de la base de datos Chroma.")
        except Exception as e:
            self.logger.error(f"Error al recuperar contexto de la base de datos Chroma: {e}")
            return "Lo siento, por problemas técnicos no puedo responder a tu pregunta en este momento.\nInténtelo más tarde.\n\nGracias."
        
        #prompt = f"Pregunta: {query}\n\nContexto (responde solo sobre el contenido del texto entregado): {contexto}\n\nLa Respuesta siempre en Español"
        
        
        prompt = (
            f"Pregunta: {query}\n\n"
            f"Contexto (Responde solo utilizando la información del texto proporcionado): {contexto}\n\n"
            "Instrucciones:\n"
            "1. Responde solo utilizando la información proporcionada en el contexto.\n"
            "2. No añadas información externa o inventada.\n"
            "3. La respuesta debe estar completamente en español.\n\n"
            #"Respuesta:"
        )
        try:
            respuestalln = self.clientOllama.chat(model="llama3", 
                                    messages=[{"role": "system", "content": prompt}],
                                    options={"temperature": 0})
            self.logger.info("Respuesta obtenida del modelo de lenguaje.")
            
            return respuestalln['message']['content']
        except Exception as e:
            self.logger.error(f"Error al obtener respuesta del modelo de lenguaje: {e}")
            return "Lo siento, por problemas técnicos no puedo responder a tu pregunta en este momento.\nInténtelo más tarde.\n\nGracias."
    
    async def queryllm_stream(self, query):
        """
        Realiza una consulta al modelo de lenguaje de manera asincrónica y devuelve la respuesta en partes.
        
        Args:
            query (str): La consulta que se le hará al modelo de lenguaje.
            
        Yields:
            str: Partes de la respuesta del modelo de lenguaje.
        """
        try:
            contexto = self.ChromaDB.get_documents(query)
            self.logger.info("Contexto recuperado de la base de datos Chroma.")
        except Exception as e:
            self.logger.error(f"Error al recuperar contexto de la base de datos Chroma: {e}")
            yield "Lo siento, por problemas tecnicos no puedo responder a tu pregunta en este momento.\nIntentelo mas tarde.\n\nGracias."
            return
        
        prompt = (
            f"Pregunta: {query}\n\n"
            f"Contexto (Responde solo utilizando la información del texto proporcionado): {contexto}\n\n"
            "Instrucciones:\n"
            "1. Responde solo utilizando la información proporcionada en el contexto.\n"
            "2. No añadas información externa o inventada.\n"
            "3. La respuesta debe estar completamente en español.\n\n"
        )

        try:
            async for part in (await self.clientOllama.chat(model="llama3", 
                                                     messages=[{"role": "system", "content": prompt}],
                                                    options={"temperature": 0}, 
                                                     stream=True)):
                yield part['message']['content']
        except Exception as e:
            self.logger.error(f"Error al obtener respuesta del modelo de lenguaje: {e}")
            yield "Lo siento, por problemas tecnicos no puedo responder a tu pregunta en este momento.\nIntentelo mas tarde.\n\nGracias."
    
    def info_llm(self):
        return ollama.show('llama3')
    
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



# Ejemplo de uso Asincrono:
# async def main():
#     llm = Rag(asincrono=True)
#     query = "Crea un resumen con los requisitos de las ayudas al transporte de los alumnos que hacen FP"

#     async for respuesta in llm.queryllm_stream(query):
#         print(respuesta)

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())

#Ejemplo de uso NO Asincrono:
# if __name__ == '__main__':
#     llm = Rag()
#     query = "¿Qué es un loro?"

#     respuesta = llm.queryllm(query)

#     print(respuesta)
