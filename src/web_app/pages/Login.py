import streamlit as st
import time

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.Usuario import DaoUser

st.set_page_config(
  page_title = "Inicio de sesión - ChatBOC",
  page_icon = "🇵🇱",
  initial_sidebar_state = "collapsed",
)

# Imágen cabecera:
st.image("images/cabeceraboc.png")


# Formulario del login:
with st.form(key="login_form"):

  # Cabecera del formulario:
  st.write("### Iniciar sesión:")

  # Campos del formulario:
  user_email = st.text_input("Email:").strip()
  user_password = st.text_input("Contraseña:", type="password").strip()

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Iniciar sesión")


# Dividir el ancho de la página en 3 columnas:
col_f1, col_f2, col_f3 = st.columns([3, 4, 3])

# Columna 2 (Footer):
with col_f2:
  st.markdown('''Hecho con ❤️ por el __Equipo A__.''')


# Validar que se envian los datos:
if submitted:

    # Instanciar objeto 'DaoUser':
    dao = DaoUser(host='localhost', user='root', password='test_pass')

    # Validar que los datos de login son correctos en la base de datos:
    comprobar_login = dao.check_login(user_email, user_password)
    
    # Si se ha logueado con éxito:
    if (comprobar_login):
      # Guardar el email del usuario (Session State API):
      st.session_state["user_email"] = user_email
      time.sleep(1)
      # Redirigir al usuario al chatbot:
      st.switch_page("pages/Chatbot.py")
    else:
      # Imprimir diálogo de error login (Provisional):
      st.error("El email o la contraseña introducidos son incorrectos.", icon="❗")

else:
  pass
