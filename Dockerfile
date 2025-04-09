FROM python:3.12 as builder

WORKDIR /app

# x-release-please-start-version
ARG PREFIX="dsa_backend-0.1.0"
# x-release-please-end

# Copie des fichiers nécessaires pour construire le wheel
COPY pyproject.toml README.md ./
COPY MANIFEST.in ./
COPY src/ ./src/

# Installation des dépendances de build et construction du wheel
RUN pip install --no-cache-dir build wheel setuptools
RUN python -m build --wheel

# Deuxième étape: installation et exécution
FROM python:3.12-slim

WORKDIR /app

# x-release-please-start-version
ARG PREFIX="dsa_backend_assistant-0.1.0"
# x-release-please-end

# Copie du wheel depuis l'étape de build
COPY --from=builder /app/dist/${PREFIX}-py3-none-any.whl ./

# Installation du wheel avec l'extra "fastapi"
RUN pip install --no-cache-dir --upgrade ${PREFIX}-py3-none-any.whl[fastapi]

# Exposition du port pour uvicorn
EXPOSE 8000

# Commande de démarrage
CMD ["run_api"]
