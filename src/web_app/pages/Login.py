import streamlit as st
import time
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import backend.ControlUsuarios as ControlUsuarios

st.set_page_config(
  page_title = "Inicio de sesión - ChatBOC",
  page_icon = "🇵🇱",
)

# Variables (Prueba sin BD):
actual_email = actual_password = "1234"

# Dividir el ancho de la página en 3 columnas:
col_b1, col_b2, col_b3 = st.columns([4, 2, 4])

# Columna 2 (Botón home):
with col_b2:
  if st.button("Inicio", type="primary"):
    st.switch_page("Home.py")


# Formulario del login:
with st.form(key="login_form"):

  # Cabecera del formulario:
  st.write("### Iniciar sesión:")

  # Campos del formulario:
  email = st.text_input("Email:", max_chars=50).strip()
  password = st.text_input("Contraseña:", type="password", max_chars=25).strip()

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Iniciar sesión")


# Dividir el ancho de la página en 3 columnas:
col_f1, col_f2, col_f3 = st.columns([3, 4, 3])

# Columna 2 (Footer):
with col_f2:
  st.markdown('''Hecho con ❤️ por  el __Equipo A__.''')


# Validar que se envian los datos:
if submitted:

  # Validar que los datos de login son correctos en la BD:
  comprobar_login = ControlUsuarios.check_login(email=email, password=password)

  # Comprobar códigos del login:
  match (comprobar_login):
    # Login correcto:
    case 0:
      # Guardar el email del usuario (Session State API):
      st.session_state["email"] = email

      time.sleep(1)

      # Redirigir al usuario al chatbot:
      st.switch_page("pages/Chatbot.py")

    # Login incorrecto:
    case 1 | 2:
      # Imprimir diálogo de error login (Provisional):
      st.error("Email o contraseña incorrecta.", icon="❗")

else:
  pass
