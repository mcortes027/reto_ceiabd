import subprocess
import time
import config as cfg
import os 
import sys

try:
    entorno = sys.argv[1:][0] 
    print(f"Se ha detectado el entorno:{entorno}")
    variables_entorno = cfg.entornos[entorno]
    os.environ['VOLUMEN_CHROMADB'] = variables_entorno['volumen_chromadb']
    print(f"Se ha asignado el path VOLUMEN_CHROMADB:{variables_entorno['volumen_chromadb']}")
    os.environ['VOLUMEN_OLLAMA'] = variables_entorno['volumen_ollama']
    print(f"Se ha asignado el path VOLUMEN_OLLAMA:{variables_entorno['volumen_ollama']}")
    os.environ['VOLUMEN_MYSQL'] = variables_entorno['volumen_mysql']
    print(f"Se ha asignado el path VOLUMEN_MYSQL:{variables_entorno['volumen_mysql']}")
except:
    print("Por favor recuerda pasar como argumento el nombre del entorno en el que estás desplegando")
    print("El entorno ha de estar definido en config.py")
# Run docker-compose up -d
subprocess.run(["docker-compose", "up", "-d"], check=True)

# Wait for 5 seconds
time.sleep(20)

# Run docker exec
subprocess.run(["docker", "exec", "-it","despliegues_ollama_1", "ollama", "pull", "llama3"], check=True)
