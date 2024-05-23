import streamlit as st

st.set_page_config(
  page_title = 'Login',
  page_icon = '💢',
)

# Variables (Prueba):
actual_email = actual_password = "1234"


# Group multiple widgets:
with st.form(key='login_form'):

  st.write('### Login:')
  email = st.text_input('Email:').strip()
  password = st.text_input('Contraseña:').strip()
  
  submit = st.form_submit_button('Login')

if submit and email == actual_email and password == actual_password:
  # If the form is submitted and the email and password are correct,
  # clear the form/container and display a success message
  st.success('Login successfully', icon='✅')
elif submit and email != actual_email and password != actual_password:
  st.error('Login failed', icon='🚨')
else:
  pass