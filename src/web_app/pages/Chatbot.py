import streamlit as st
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.Rag import Rag

st.set_page_config(
  page_title = "Chatbot - ChatBOC",
  page_icon = "🇵🇱",
  initial_sidebar_state = "collapsed",
  layout = "wide",
)

# Si el usuario ha iniciado sesión:
if "email" in st.session_state:

  st.markdown('''<center><h2>ChatBoc<h2></center>''', unsafe_allow_html=True)

  # Instanciar la clase 'Rag':
  llm = Rag(host=os.environ['OLLAMA_HOST'])

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

    # powerbi.log(prompt)

    # Mostrar el mensaje del asistente en el chat:
    with st.chat_message("assistant"):
      st.markdown(respuesta)
    # Añadir el mensaje del asistente al historial:
    st.session_state.historial_msg.append({"role": "assistant", "content": respuesta})

else:
  # Si no ha iniciado sesión, redirigir al home:
  st.switch_page("Home.py")
