# Document Sorting Assistant

Un assistant intelligent pour organiser et classer vos documents automatiquement en utilisant l'IA.

## Fonctionnalités

- Suggestion de noms de fichiers basée sur le contenu
- Classification automatique des documents
- Interface utilisateur Streamlit
- API REST avec FastAPI
- Support Docker pour le déploiement

## Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Docker (optionnel, pour le déploiement)

## Installation

### Installation de base
```bash
pip install .
```

### Installation avec interface utilisateur Streamlit
```bash
pip install .[streamlit]
```

### Installation avec API FastAPI
```bash
pip install .[fastapi]
```

### Installation pour le développement
```bash
pip install .[ci,cd]
```

## Utilisation

### Interface en ligne de commande (CLI)
```bash
# Suggérer un nom de fichier
suggest_filename -f <filename>

# Suggérer un répertoire
suggest_directory -f <filename> -d <directory1> -d <directory2> ...
```

### Interface utilisateur Streamlit
```bash
run_ui
```

### API FastAPI
```bash
run_api
```

## Déploiement

### Déploiement local avec Docker
```bash
# Construire l'image Docker
docker build . -t dsa

# Lancer avec docker-compose
docker-compose up
```

## Développement

### Tests
```bash
# Installer les dépendances de test
pip install .[ci]

# Exécuter les tests
pytest
```

### Linting
```bash
# Vérifier le style de code
black .
flake8
```

### Packaging
```bash
# Construire le package Python
python -m build

# Publier sur PyPI (nécessite un compte)
twine upload dist/*
```

## Configuration

Le projet utilise un fichier `.env` pour la configuration. Copiez `.env.example` vers `.env` et modifiez les variables selon vos besoins.

## Contribution

Les contributions sont les bienvenues ! Veuillez consulter les directives de contribution dans le dossier `.github`.

## Licence

[À définir]

## Contact

Pour toute question ou suggestion, contactez [Louis](mailto:louis.dalonis@gmail.com).

## Packaging
### Python package
python -m build

### docker image
docker build . -t dsa

## Deploying
### Locally
  docker-compose

### Terraform (in progress)
