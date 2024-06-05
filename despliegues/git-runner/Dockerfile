# Dockerfile para un GitHub Runner
#
# Este Dockerfile se utiliza para crear una imagen de contenedor para un GitHub Runner.
# Un GitHub Runner es una instancia de ejecución que se utiliza para ejecutar trabajos en un repositorio de GitHub.
# Esta imagen de contenedor se puede utilizar para configurar y ejecutar un GitHub Runner en un entorno de contenedorizado.
#
# Para obtener más información sobre los GitHub Runners, consulte la documentación oficial de GitHub.
#
# Autor: [Manolo Corte]
# Versión: 1.0
#
# Uso:
#   - Construir la imagen del contenedor:
#       docker build -t mcortes027/ceiabda_runner:latest .
#
#   - Ejecutar el contenedor:
#       docker run -it --name mcortes027/ceiabda_runner:latest (Sin volúmenes ya que es de test)
#
#   - Configurar el GitHub Runner:
#       [Variables debajo]
#
#
# Nota: Asegúrese de proporcionar los valores adecuados para la configuración y ejecución del GitHub Runner.
FROM debian:bookworm-slim


ARG RUNNER_VERSION="2.316.1"

# SOBRE LOS DIRS DE BACKUPS
ENV VOLUMEN_MYSQL="/mysql"
ENV VOLUMEN_CHROMADB="/chromadb"
ENV VOLUMEN_BACKUPS="/backups"

ENV GITHUB_PERSONAL_TOKEN "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"
ENV GITHUB_OWNER "mcortes027"
ENV GITHUB_REPOSITORY "reto_ceiabd"

# Instalo la CLI de Docker ya que la necesito para hacer despliegues. 
RUN apt-get update && \
    apt-get install -y ca-certificates curl gnupg && \ 
    apt-get install -y git
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg
# Install Python
RUN apt-get install -y python3 python3-pip


# Add the repository to Apt sources:
RUN echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update

# I only install the CLI, we will run docker in another container!
RUN apt-get install -y docker-ce-cli

# Install the GitHub Actions Runner 
RUN apt-get update && apt-get install -y sudo jq

RUN useradd -m github && \
  usermod -aG sudo github && \
  echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER github
WORKDIR /actions-runner
RUN curl -Ls https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz | tar xz \
  && sudo ./bin/installdependencies.sh

COPY --chown=github:github entrypoint.sh  /actions-runner/entrypoint.sh
RUN sudo chmod u+x /actions-runner/entrypoint.sh

#working folder for the runner 
RUN sudo mkdir /work 
RUN sudo chown -R github:github /work

# Clone the repository and build the docker images
RUN git clone https://$GITHUB_OWNER:$GITHUB_PERSONAL_TOKEN@github.com/$GITHUB_OWNER/$GITHUB_REPOSITORY.git /work
RUN sudo apt-get install -y zip 
#USER root 
# We need to run docker commands
ENTRYPOINT ["/actions-runner/entrypoint.sh"]
