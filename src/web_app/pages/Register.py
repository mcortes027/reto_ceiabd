import streamlit as st
import time

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.Usuario import Usuario
from database.Usuario import DaoUser
from utils.UtilidadesBack import UtilidadesBack

HOST_MYSQL = os.environ["HOST_MYSQL"]
USER_MYSQL = os.environ["USER_MYSQL"]
PASSWORD_MYSQL = os.environ["PASSWORD_MYSQL"]

def validar_usuario(user_email, user_password, user_username, user_edad, user_telefono, user_direccion, user_localidad, user_cp, user_uso):
    if not UtilidadesBack.validar_email(user_email):
        st.error(f"El email introducido no es válido.", icon="❗")
        return False

    validar_pass = UtilidadesBack.validar_password(user_password, min_caracteres=8, max_caracteres=25)
    if not validar_pass[0]:
        st.error(validar_pass[1], icon="❗")
        return False

    if not (0 < len(user_username) <= 15):
        st.error(f"El nombre de usuario introducido es demasiado corto o largo.", icon="❗")
        return False

    if not (0 < user_edad <= 100):
        st.error(f"La edad introducida no es válida.", icon="❗")
        return False

    if not (0 < len(user_telefono) <= 12):
        st.error(f"La longitud del teléfono introducido es demasiado corta o larga.", icon="❗")
        return False

    if not (0 < len(user_direccion) <= 100):
        st.error(f"La longitud de la dirección introducida es demasiado corta o larga.", icon="❗")
        return False

    if not (0 < len(user_localidad) <= 100):
        st.error(f"La longitud de la localidad introducida es demasiado corta o larga.", icon="❗")
        return False

    if not UtilidadesBack.validar_codigo_postal(user_cp):
        st.error(f"El código postal introducido no tiene un formato válido.", icon="❗")
        return False

    return True


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
  user_cp = st.text_input("Código postal:", max_chars=5)

  # Dividir el ancho de la página en 3 columnas:
  col_r1, col_r2, col_r3 = st.columns([4, 2, 4])

  # Columna 2 (Registrarse):
  with col_r2:
    # Botón enviar datos formulario:
    submitted = st.form_submit_button("Registrarse")


# Dividir el ancho de la página en 3 columnas:
col_f1, col_f2, col_f3 = st.columns([3, 4, 3])

# Columna 2 (Footer):
with col_f2:
  st.markdown('''Hecho con ❤️ por el __Equipo A__.''')


if submitted:
    if validar_usuario(user_email, user_password, user_username, user_edad, user_telefono, user_direccion, user_localidad, user_cp, user_uso):
        nuevo_usuario = Usuario(
            id=1,
            username=user_username,
            password=user_password,
            email=user_email,
            direccion=user_direccion,
            localidad=user_localidad,
            telefono=user_telefono,
            uso=user_uso,
            cp=user_cp,
            edad=user_edad
        )

        dao = DaoUser(host=HOST_MYSQL, user=USER_MYSQL, password=PASSWORD_MYSQL)
        comprobar_registro = dao.registrar_usuario(nuevo_usuario)

        if comprobar_registro:
            time.sleep(1)
            st.switch_page("Home.py")
        else:
            st.error(f"El usuario no ha podido ser registrado en la Base de Datos con éxito.", icon="❗")
