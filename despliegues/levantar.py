import subprocess
import time

# Run docker-compose up -d
subprocess.run(["docker-compose", "up", "-d"], check=True)

# Wait for 5 seconds
time.sleep(5)

# Run docker exec
subprocess.run(["docker", "exec", "-it","despliegues-ollama-1", "ollama", "pull", "llama3"], check=True)