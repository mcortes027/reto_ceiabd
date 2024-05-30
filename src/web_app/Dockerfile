# Use an official Python runtime as a parent image
# hacer imagen con: docker build -t ceiabda_gui:latest .
# ejecutar imagen con: docker run -p --name ceiabda_gui 8501:8501 ceiabda_gui:latest
# Fichero mantenido por: Manolo Corte
FROM python:3.11-slim-buster

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