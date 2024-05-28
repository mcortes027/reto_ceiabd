import streamlit as st
import time

st.set_page_config(
  page_title = "Registro de usuarios - ChatBOC",
  page_icon = "🇵🇱",
)

# Lista de tipos de usos:
lista_usos = ["Ocasional", "Académico", "Profesional", "Otros usos"]
# Variable que controla el éxito del registro:
exito_registro = True # (Provisional: Verdadero por defecto.)


# Formulario del login:
with st.form(key="register_form"):
    
  # Cabecera del formulario:
  st.write("### Registro de usuarios:")

  # Campos del formulario:
  email = st.text_input("Email:").strip()
  password = st.text_input("Contraseña:", type="password").strip()
  username = st.text_input("Nombre de usuario:").strip()
  edad = st.number_input("Edad:", step=1)
  uso = st.selectbox("¿Qué uso le darás a esta aplicación?", lista_usos)
  telefono = st.number_input("Teléfono:", step=1)
  direccion = st.text_input("Dirección:").strip()
  localidad = st.text_input("Localidad:").strip()
  cp = st.number_input("Código postal:", step=1)

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Registrar")


# Validar que se envian los datos:
if submitted:

  # Validar que se ha registrado en BD el usuario con éxito:
  if exito_registro:
    
    time.sleep(1)
    # Redirigir al usuario al home:
    st.switch_page("Home.py")
  else:
    # Imprimir diálogo de error en el registro:
    st.error(f"El usuario no ha podido ser registrado con éxito.", icon="❗")

else:
  pass
