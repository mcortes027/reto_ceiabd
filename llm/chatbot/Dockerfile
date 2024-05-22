# Esta imagen de Docker es un wrapper de la oficial de Chrome
# Importa código auxiliar de Python (jupyter), instala lo que esté en requirements.txt (si el fichero existe en este directorio)
# Para construir la imagen, ejecutar el siguiente comando en la carpeta llm/chatbot: docker build -t ceiabd_equipoa_chatbot:latest . 
# Fichero Mantenido por Manolo Corte

FROM jupyter/base-notebook as base 
WORKDIR /codigo
COPY ./*.py /codigo
RUN : \
    && apt-get update \
    && apt-get install -y python3-pip \
    && :
# COPY requirements.txt . <-- Descomentar si hay algo en requirements.txt
# RUN pip3 install -r /codigo/requirements.txt <-- Descomentar si hay algo en requirements.txt

FROM base as notebooks 
WORKDIR /home/equipoa/work
COPY ./*.ipynb . 