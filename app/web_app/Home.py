import streamlit as st

st.set_page_config(
  page_title = "Inicio - ChatBOC",
  page_icon = "🇵🇱",
  initial_sidebar_state = "collapsed"
)

# Imágen cabecera:
st.image("images/cabeceraboc.png")

# Dividir el ancho de la página en 4 columnas:
col_b1, col_b2, col_b3, col_b4 = st.columns([3, 2, 2, 3])

# Columna 2 (Botón registro):
with col_b2:
  if st.button("Registro"):
    st.switch_page("pages/Register.py")

# Columna 3 (Botón inicio sesión):
with col_b3:
  if st.button("Iniciar sesión"):
    st.switch_page("pages/Login.py")

# Divisor de texto:
st.divider()

# Texto ChatBOC:
st.markdown('''
            ## ¿Qúe es ChatBOC?  
            ChatBOC es un chatbot diseñado para brindar asistencia y responder preguntas relacionadas con la normativa legal del Boletín Oficial de Cantabria ([BOC](https://boc.cantabria.es)).  
            Utiliza el modelo de lenguaje [Llama 3](https://llama.meta.com/llama3) para comprender y responder las consultas de los usuarios de una manera efectiva.
            ''')

# Texto "Quienes somos":
st.markdown('''
            ## Quienes somos:
            * __José Ramón Blanco Gutiérrez__ _(Coordinador / Desarrollador)_
            * __Aarón Saiz Guerra__ _(Portavoz / Desarrollador)_
            * __Manolo Corte Salazar__ _(Secretario / Desarrollador)_
            * __Iosu Ramos Martínez__ _(Desarrollador)_
            * __Juan Carlos González Fernández__ _(Desarrollador)_
            ''')

# Continuación del texto "Quienes somos":
st.markdown('''
            Nosotros somos un grupo de estudiantes del Curso de Especialización en Inteligencia Artificial y Big Data ([CEIABD](https://www.todofp.es/que-estudiar/loe/informatica-comunicaciones/ce-inteligencia-artificial-bigdata.html)) del [IES Miguel Herrero Pereda](https://www.educantabria.es/web/ies-miguel-herrero-pereda).
            ''')

# Divisor de texto:
st.divider()

# Dividir el ancho de la página en 3 columnas:
col_f1, col_f2, col_f3 = st.columns([3, 4, 3])

# Columna 2 (Footer):
with col_f2:
  st.markdown('''Hecho con ❤️ por el __Equipo A__.''')
  