import streamlit as st

st.set_page_config(
  page_title = 'Login',
  page_icon = '💢',
)

# Variables (Prueba sin BD):
actual_email = actual_password = "1234"


# Formulario del login:
with st.form(key="login_form"):

  # Cabecera del formulario:
  st.write("### Iniciar sesión:")

  # Campos del formulario:
  email = st.text_input("Email:").strip()
  password = st.text_input("Contraseña:", type="password").strip()

  # Botón enviar datos formulario:
  submitted = st.form_submit_button("Iniciar sesión")

# Validar que se envian los datos:
if submitted:

  # Validar email/password (Provisional):
  if email == actual_email and password == actual_password:
    # Guardar los datos del usuario (Session State API):
    st.session_state['email'] = email
    st.session_state['password'] = password

    st.success('Login successfully', icon='✅')
    st.write(submitted)
  else:
    st.error("Mensaje error login", icon="❗")
    st.write(submitted)

else:
  pass
