import streamlit as st

st.set_page_config(
  page_title = 'ChatBOC',
  page_icon = '💢',
)

# Formulario del login:
with st.form(key="register_form"):
    
  # Cabecera del formulario:
  st.write("### Registrar usuario:")

  # Campos del formulario:
  email = st.text_input("Email:").strip()
  password = st.text_input("Contraseña:", type="password").strip()
  username = st.text_input("Nombre de usuario:").strip()
  telefono = st.text_input("Teléfono:").strip()
  uso = st.text_input("Tipo de uso:").strip()
  direccion = st.text_input("Dirección:").strip()
  localidad = st.text_input("Localidad:").strip()
  cp = st.text_input("Código postal:").strip()

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Registro")