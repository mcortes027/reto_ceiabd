import streamlit as st
import asyncio
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.Rag import Rag
from database.PowerBI import PowerBI

CHROMA_HOST = os.environ.get("CHROMA_HOST")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST")

HOST_MYSQL = os.environ["HOST_MYSQL"]
USER_MYSQL = os.environ["USER_MYSQL"]
PASSWORD_MYSQL = os.environ["PASSWORD_MYSQL"]

async def mostrar_respuesta_asincrona(prompt, container):
    """Genera y muestra la respuesta del asistente de manera asincrónica."""
    # Instanciar la clase 'Rag'
    llm = Rag(host_ollama=OLLAMA_HOST, chroma_host=CHROMA_HOST, asincrono=True)

    # Generar la respuesta del asistente de manera asincrónica
    respuesta_completa = ""
    async for parte in llm.queryllm_stream(prompt):
        respuesta_completa += parte
        container.markdown(respuesta_completa)
        await asyncio.sleep(0.1)  # Pequeña pausa para simular el streaming
    return respuesta_completa

async def actualizar_respuesta(prompt):
    # Crear un contenedor para la respuesta del asistente
    with st.chat_message("assistant"):
        respuesta_placeholder = st.empty()
        respuesta_completa = await mostrar_respuesta_asincrona(prompt, respuesta_placeholder)
    
    st.session_state.historial_msg.append({"role": "assistant", "content": respuesta_completa})

    # Recuperar el email del usuario de la (Session State API):
    user_email = st.session_state["user_email"]

    # Instanciar objeto 'PowerBI':
    powerbi = PowerBI(host=HOST_MYSQL, user=USER_MYSQL, password=PASSWORD_MYSQL)

    # Insertar la pregunta y el email del usuario en la base de datos:
    powerbi.NuevoRegistro(prompt, user_email)

def run_async_task(task):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task)
    loop.close()

st.set_page_config(
  page_title = "ChatBOC - Proyecto IA y Big Data",
  page_icon = "🇵🇱",
  initial_sidebar_state = "collapsed",
  layout = "wide",
)

st.markdown(
    """
    <style>
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: inherit; /* Utiliza el color de fondo de la web */
        padding: 5px; /* Reducir el padding para hacer el footer menos alto */
        text-align: center;
        z-index: 1000;
        box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* Sombra opcional para destacar el footer */
    }
    .content {
        margin-bottom: 40px; /* Ajuste para el pie de página */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Pie de página fijo
st.markdown('''
  <div class="fixed-footer">
      <p>Hecho con ❤️ por el Equipo IA</p>
  </div>
  ''', unsafe_allow_html=True)

# Si el usuario ha iniciado sesión:
if "user_email" in st.session_state:

  st.markdown('''<center><h2>ChatBOC<h2></center>''', unsafe_allow_html=True)

  # Inicializar el historial de mensajes si no existe en la (Session State API):
  if "historial_msg" not in st.session_state:
    st.session_state.historial_msg = []

  # Cargar el histórico de mensajes de la (Session State API):
  for mensaje in st.session_state.historial_msg:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

  # Si el usuario ha insertado un prompt:
  if prompt := st.chat_input("Introduce tu mensaje aquí:"):
    
    # Mostrar el mensaje del usuario en el chat:
    with st.chat_message("user"):
      st.markdown(prompt)
    # Añadir el mensaje del usuario al historial:
    st.session_state.historial_msg.append({"role": "user", "content": prompt})

    # Ejecutar la tarea asincrónica usando una función auxiliar
    run_async_task(actualizar_respuesta(prompt))

else:
  # Si no ha iniciado sesión, redirigir al home:
  st.switch_page("Home.py")
