import streamlit as st

st.set_page_config(
  page_title = "Inicio - ChatBOC",
  page_icon = "🇵🇱",
)

# Imágen cabecera
st.image("images/cabeceraboc.png")

# Dividir el ancho de la página en 3 columnas:
col_b1, col_b2, col_b3 = st.columns([2, 2, 7])

# Columna 1 (Botón registro):
with col_b1:
  if st.button("Registro"):
    st.switch_page("pages/Register.py")

# Columna 2 (Botón inicio sesión):
with col_b2:
  if st.button("Iniciar sesión"):
    st.switch_page("pages/Login.py")
