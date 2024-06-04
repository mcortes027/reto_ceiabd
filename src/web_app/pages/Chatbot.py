import streamlit as st
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.Rag import Rag
from database.PowerBI import PowerBI

CHROMA_HOST = "localhost" # os.environ.get("CHROMA_HOST")
OLLAMA_HOST = "localhost" # os.environ.get("OLLAMA_HOST")

HOST_MYSQL = 'localhost' # os.environ["HOST_MYSQL"]
USER_MYSQL = 'root' # os.environ["USER_MYSQL"]
PASSWORD_MYSQL = 'test_pass' # os.environ["PASSWORD_MYSQL"]


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
      <p>Hecho con ❤️ por el Equipo A</p>
  </div>
  ''', unsafe_allow_html=True)


# Si el usuario ha iniciado sesión:
if "user_email" in st.session_state:

  #st.markdown('''<center><h2>ChatBOC<h2></center>''', unsafe_allow_html=True)
  # Contenido principal con margen ajustado para evitar superposición con el encabezado y pie de página
  st.markdown('<div class="content">', unsafe_allow_html=True)

  # Instanciar la clase 'Rag':
  llm = Rag(host_ollama=OLLAMA_HOST, host_chroma=CHROMA_HOST)

  # Inicializar el historial de mensajes si no existe en la (Session State API):
  if "historial_msg" not in st.session_state:
    st.session_state.historial_msg = []

  # Cargar el histórico de mensajes de la (Session State API):
  for mensaje in st.session_state.historial_msg:

    # Escribir en el chat los mensajes del historial:
    match mensaje["role"]:
      case "user":
        with st.chat_message("user"):
          st.markdown(mensaje["content"])
      case "assistant":
        with st.chat_message("assistant"):
          st.markdown(mensaje["content"])

  # Si el usuario ha insertado un prompt:
  if prompt := st.chat_input("Introduce tu mensaje aquí:"):
    
    # Mostrar el mensaje del usuario en el chat:
    with st.chat_message("user"):
      st.markdown(prompt)
    # Añadir el mensaje del usuario al historial:
    st.session_state.historial_msg.append({"role": "user", "content": prompt})

    # Generar la respuesta del asistente preguntando al LLM: 
    respuesta = llm.queryllm(prompt)

    # Recuperar el email del usuario de la (Session State API):
    user_email = st.session_state["user_email"]

    # Instanciar objeto 'PowerBI':
    powerbi = PowerBI(host=HOST_MYSQL, user=USER_MYSQL, password=PASSWORD_MYSQL)

    # Insertar la pregunta y el email del usuario en la base de datos:
    powerbi.NuevoRegistro(prompt, user_email)

    # Mostrar el mensaje del asistente en el chat:
    with st.chat_message("assistant"):
      st.markdown(respuesta)
    # Añadir el mensaje del asistente al historial:
    st.session_state.historial_msg.append({"role": "assistant", "content": respuesta})

else:
  # Si no ha iniciado sesión, redirigir al home:
  st.switch_page("Home.py")
