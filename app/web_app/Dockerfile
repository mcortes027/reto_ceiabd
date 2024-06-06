# Use an official Python runtime as a parent image
# hacer imagen con: docker build -t mcortes027/ceiabda_gui:latest . 
# ejecutar imagen con: docker run -p --name ceiabda_gui 8501:8501 mcortes027/ceiabda_gui:latest
# Fichero mantenido por: Manolo Corte
FROM python:3.11.5-bookworm

ENV CHROMA_HOST="172.18.0.2"
ENV OLLAMA_HOST="172.18.0.3"
ENV HOST_MYSQL="172.18.0.4"
ENV USER_MYSQL="root"
ENV PASSWORD_MYSQL="test_pass"

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./docker/requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD streamlit run Home.py
