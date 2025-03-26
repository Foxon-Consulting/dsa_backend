# Document Sorting Assistant

## Installation

```bash
# Installation rapide de l'environnement
./setup.sh
```

Ce script va:
- Créer un environnement virtuel Python `.venv`
- Activer l'environnement virtuel
- Installer le package Python DSA: `pip install -e .`
- Installer les dépendances FastAPI: `pip install .[fastapi]`

## Lancement de l'application

### 1. Interface Streamlit (pour le développement/débogage)

Streamlit offre une interface graphique intuitive pour tester les fonctionnalités:

```bash
# Méthode 1: Via la commande configurée dans pyproject.toml
docsort

# Méthode 2: Lancement direct de l'application Streamlit
streamlit run src/ui/streamlit_entrypoint.py
```

L'interface Streamlit permet de:
- Télécharger des fichiers PDF individuels ou des dossiers zippés
- Obtenir des suggestions automatiques de noms de fichiers
- Classer automatiquement les documents dans les dossiers appropriés
- Tester différents modèles LLM (Claude, Deepseek, GPT)

### 2. API FastAPI (pour la production)

Pour déployer l'application en production via une API REST:

```bash
# Depuis la racine du projet
uvicorn src.app.api.main:app --reload

# Alternative: créer un fichier main.py à la racine et exécuter
uvicorn main:app --reload
```

L'API FastAPI expose plusieurs endpoints:
- `/suggest-filename`: Suggère un nom pour un fichier PDF
- `/suggest-path`: Suggère un chemin de classement pour un PDF
- `/move-and-rename`: Déplace et renomme automatiquement un fichier

Accédez à la documentation interactive à l'adresse: http://localhost:8000/docs

## Fonctionnalités principales

- Analyse intelligente de documents PDF
- Suggestions automatisées de noms et chemins de classement
- Plusieurs modèles LLM disponibles
- Interface utilisateur conviviale ou API REST
- Traitement automatisé des documents
