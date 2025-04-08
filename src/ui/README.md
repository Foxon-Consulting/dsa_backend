# Document Sorting Assistant - Interface Streamlit

Ce fichier `streamlit_entrypoint.py` fournit une interface utilisateur web pour l'application Document Sorting Assistant.

## Fonctionnalités

- Téléchargement de documents (PDF, DOCX, TXT, etc.)
- Suggestion automatique de noms de fichiers basée sur le contenu
- Sélection des répertoires cibles
- Suggestion du répertoire le plus approprié pour classer le document
- Affichage des logs de traitement

## Prérequis

- Python 3.8+
- Streamlit
- Les dépendances de la bibliothèque principale

## Installation

Assurez-vous que les dépendances nécessaires sont installées :

```bash
pip install .
pip install .[streamlit]
```

## Utilisation

Pour démarrer l'interface Streamlit :

```bash
streamlit run src/ui/streamlit_entrypoint.py
```

L'application sera accessible dans votre navigateur à l'adresse `http://localhost:8501`.

## Guide d'utilisation

1. Téléchargez un document en utilisant le champ de téléchargement
2. Cliquez sur "Process File" pour obtenir une suggestion de nom basée sur le contenu
3. Sélectionnez un répertoire racine pour afficher les sous-répertoires disponibles
4. Cliquez sur "Process Directory" pour obtenir une suggestion de répertoire où classer le document
5. Consultez les logs pour voir l'historique des traitements
