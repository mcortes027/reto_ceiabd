import streamlit as st
import time

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.Usuario import Usuario
from database.Usuario import DaoUser
from utils.UtilidadesBack import UtilidadesBack

st.set_page_config(
  page_title = "Registro de usuarios - ChatBOC",
  page_icon = "🇵🇱",
  initial_sidebar_state = "collapsed"
)

# Lista de tipos de usos:
lista_usos = ["Ocasional", "Académico", "Profesional", "Otros usos"]

# Imágen cabecera:
st.image("images/cabeceraboc.png")


# Formulario del registro:
with st.form(key="register_form"):
    
  # Cabecera del formulario:
  st.write("### Registro de usuarios:")

  # Campos del formulario:
  user_email = st.text_input("Email:", max_chars=50).strip()
  user_password = st.text_input("Contraseña:", type="password", max_chars=25).strip()
  user_username = st.text_input("Nombre de usuario:", max_chars=15).strip()
  user_edad = st.number_input("Edad:", step=1, min_value=1, max_value=100)
  user_uso = st.selectbox("¿Qué uso le darás a esta aplicación?", lista_usos)
  user_telefono = st.text_input("Teléfono:", max_chars=12).strip()
  user_direccion = st.text_input("Dirección:", max_chars=100).strip()
  user_localidad = st.text_input("Localidad:", max_chars=100).strip()
  user_cp = st.number_input("Código postal:", step=1, max_value=99999)

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Registrar")


# Dividir el ancho de la página en 3 columnas:
col_f1, col_f2, col_f3 = st.columns([3, 4, 3])

# Columna 2 (Footer):
with col_f2:
  st.markdown('''Hecho con ❤️ por el __Equipo A__.''')


# Validar que se envian los datos:
if submitted:

  # Crear un objeto de la clase 'Usuario:
  nuevo_usuario = Usuario(
    id = 1, 
    username = user_username, 
    password = user_password, 
    email = user_email, 
    direccion = user_direccion, 
    localidad = user_localidad, 
    telefono = user_telefono, 
    uso = user_uso, 
    cp = user_cp, 
    edad = user_edad
  )

  # Instanciar objeto 'DaoUser':
  dao = DaoUser(host='localhost', user='root', password='test_pass')

  # Validar que el nuevo usuario ha sido registrado con éxito en la base de datos:
  comprobar_registro = dao.registrar_usuario(nuevo_usuario)

  # Si se ha registrado con éxito:
  if comprobar_registro:
    
    time.sleep(1)
    # Redirigir al usuario al home:
    st.switch_page("Home.py")
  else:
    # Imprimir diálogo de error en el registro:
    st.error(f"El usuario no ha podido ser registrado con éxito.", icon="❗")

else:
  pass
