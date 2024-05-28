import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.ChromaVectorStore import ChromaVectorStore
import ollama


class rag:
    def __init__(self):
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
        prompt = f"Pregunta: {query}\n\nContexto (responde solo sobre el contenido del texto entregado): {contexto}\n\nLa Respuesta siempre en Español"
        respuestalln = ollama.chat(model="llama3", 
                                   messages=[{"role": "system", "content": prompt}],
                                   options={"temperature": 0})
        
        return respuestalln['messages']['content']