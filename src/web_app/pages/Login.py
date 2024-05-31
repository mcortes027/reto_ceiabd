import streamlit as st
import time

st.set_page_config(
  page_title = "Inicio de sesión - ChatBOC",
  page_icon = "🇵🇱",
  initial_sidebar_state = "collapsed",
)

# Variables (Prueba sin BD):
actual_email = actual_password = "1234"

# Imágen cabecera:
st.image("images/cabeceraboc.png")


# Formulario del login:
with st.form(key="login_form"):

  # Cabecera del formulario:
  st.write("### Iniciar sesión:")

  # Campos del formulario:
  email = st.text_input("Email:").strip()
  password = st.text_input("Contraseña:", type="password").strip()

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Iniciar sesión")


# Dividir el ancho de la página en 3 columnas:
col_f1, col_f2, col_f3 = st.columns([3, 4, 3])

# Columna 2 (Footer):
with col_f2:
  st.markdown('''Hecho con ❤️ por el __Equipo A__.''')


# Validar que se envian los datos:
if submitted:

  # Validar email/password (Provisional):
  if email == actual_email and password == actual_password:
    # Guardar el email del usuario (Session State API):
    st.session_state["email"] = email

    time.sleep(1)
    # Redirigir al usuario al chatbot:
    st.switch_page("pages/Chatbot.py")

  else:
    # Imprimir diálogo de error login (Provisional):
    st.error("Mensaje de error login.", icon="❗")

else:
  pass
