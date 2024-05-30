# Use an official Python runtime as a parent image
# hacer imagen con: docker build -t mcortes027/ceiabda_scrapper:latest .
# ejecutar imagen con: docker run --name ceiabda_scrapper mcortes027/ceiabda_scrapper:latest --network despliegues_red_llm -v /reto_ceiabda_produccion/pdfs:/app/data
# Fichero mantenido por: Manolo Corte
FROM python:3.11-slim-buster as base 

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./docker/requirements.txt

# Run streamlit when the container launches
CMD python  MainScrapperDiario.py
