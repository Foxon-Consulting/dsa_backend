from pathlib import Path
from crewai import LLM
from typing import List
import os
import mimetypes
import PyPDF2
import io


MODEL = "gpt-3.5-turbo"

RENAME_OPENAI_API_KEY = LLM(api_key=os.getenv("OPENAI_API_KEY"), model=MODEL)


def get_tree(root_folder: Path) -> List[Path]:
    """
    Retourne une liste de tous les sous-dossiers dans le dossier racine.
    Cette fonction ne crée PAS de dossiers, elle liste seulement ceux qui existent.
    """
    try:
        if not root_folder.exists():
            print(f"Warning: Root folder {root_folder} does not exist")
            return (
                []
            )  # Retourner une liste vide si le dossier racine n'existe pas

        # Récupérer tous les dossiers et sous-dossiers
        tree = [p for p in root_folder.rglob("*") if p.is_dir()]

        # Assurez-vous d'inclure le dossier racine lui-même
        if root_folder not in tree and root_folder.is_dir():
            tree.insert(0, root_folder)

        print(f"Directory tree for {root_folder}: {[str(p) for p in tree]}")
        return tree
    except Exception as e:
        print(f"Error getting directory tree: {str(e)}")
        # En cas d'erreur, retourner au moins le dossier racine s'il existe
        return (
            [root_folder]
            if root_folder.exists() and root_folder.is_dir()
            else []
        )


def is_valid_pdf(file_path: Path) -> bool:
    """
    Vérifie si le fichier est un PDF valide en utilisant plusieurs méthodes.
    """
    try:
        # Si le fichier n'existe pas, ce n'est pas un PDF valide
        if not file_path.exists():
            print(f"File does not exist: {file_path}")
            return False

        # Tenter de lire les premiers octets pour détecter la signature PDF
        with open(file_path, "rb") as f:
            header = f.read(1024)  # Lire le début du fichier

            # Vérifier si le fichier commence par la signature PDF (%PDF-)
            if not header.startswith(b"%PDF-"):
                print(f"File {file_path} does not have PDF signature")
                return False

            try:
                # Si nous avons détecté la signature PDF, essayons d'ouvrir avec PyPDF2
                f.seek(0)  # Retourner au début du fichier
                reader = PyPDF2.PdfReader(f)
                # Si nous pouvons accéder à la structure du document, c'est un PDF valide
                page_count = len(reader.pages)
                print(
                    f"File {file_path} is a valid PDF with {page_count} pages"
                )
                return page_count > 0
            except Exception as e:
                print(f"Error reading PDF structure for {file_path}: {str(e)}")
                return False

    except Exception as e:
        print(f"Error checking PDF {file_path}: {str(e)}")
        return False


def get_suggested_file_name(
    source_file_path: Path, llm: LLM = RENAME_OPENAI_API_KEY
) -> str:
    """
    Rename the file using the RenameCrew class.
    """
    print(f"Processing file for name suggestion: {source_file_path}")

    # Vérifier si le fichier est un PDF valide
    if not is_valid_pdf(source_file_path):
        print(
            f"File {source_file_path} is not a valid PDF, returning original name"
        )
        return (
            source_file_path.name
        )  # Retourner le nom original en cas de fichier non PDF

    try:
        from dsa.crews import RenameCrew
        from crewai_tools import PDFSearchTool

        search_tool = PDFSearchTool(pdf=str(source_file_path))
        log_file_name = (
            type(search_tool).__name__ + "_" + llm.model + "_log.txt"
        )

        rename_custom_crew = RenameCrew(
            [search_tool], llm, output_log_file=log_file_name
        )
        final_name = rename_custom_crew.kickoff().raw

        return final_name
    except Exception as e:
        print(f"Error in get_suggested_file_name: {str(e)}")
        # En cas d'erreur, retourner le nom original avec un préfixe pour indiquer l'échec
        return "error_" + source_file_path.name


def get_suggested_path(
    root_folder: Path, source_file_path: Path, llm: LLM = RENAME_OPENAI_API_KEY
) -> str:
    """
    Get the suggested path for the file using the SortCrew class.
    """
    print(
        f"Processing file for path suggestion: {source_file_path}, root folder: {root_folder}"
    )

    # Vérifier si le fichier est un PDF valide
    if not is_valid_pdf(source_file_path):
        print(
            f"File {source_file_path} is not a valid PDF, returning root folder path"
        )
        return str(
            root_folder
        )  # Retourner le dossier racine en cas de fichier non PDF

    try:
        from dsa.crews import SortCrew
        from crewai_tools import PDFSearchTool

        # Vérifier si le dossier racine existe
        if not root_folder.exists():
            print(
                f"Root folder {root_folder} does not exist. Using as root folder."
            )
            return str(root_folder)

        # Obtenir l'arborescence des dossiers disponibles
        directory_tree = get_tree(root_folder)

        if not directory_tree:
            print(
                f"No valid directories found in {root_folder}. Using root folder as default."
            )
            return str(root_folder)

        print(f"Available directories: {[str(d) for d in directory_tree]}")

        # Créer l'outil de recherche PDF
        search_tool = PDFSearchTool(pdf=str(source_file_path))
        log_file_name = (
            type(search_tool).__name__ + "_" + llm.model + "_log.txt"
        )

        # Initialiser la Crew avec l'arborescence de dossiers disponibles
        sort_custom_crew = SortCrew(
            [search_tool], llm, directory_tree, output_log_file=log_file_name
        )

        # Obtenir la suggestion
        suggested_path = sort_custom_crew.kickoff().raw

        # Vérifier si le chemin suggéré existe dans l'arborescence
        suggested_exists = False
        for dir_path in directory_tree:
            if str(suggested_path) == str(dir_path):
                suggested_exists = True
                break

        if not suggested_exists:
            print(
                f"Suggested path '{suggested_path}' is not in the available directory tree."
            )
            # Essayer de trouver une correspondance partielle
            best_match = None
            best_match_score = 0
            for dir_path in directory_tree:
                # Calculer un score simple de correspondance (plus c'est long, meilleur c'est)
                if str(suggested_path).lower() in str(dir_path).lower():
                    match_length = len(str(suggested_path))
                    if match_length > best_match_score:
                        best_match = dir_path
                        best_match_score = match_length

            if best_match:
                print(f"Found best matching directory: {best_match}")
                return str(best_match)

            print(
                f"No matching directory found. Using root folder: {root_folder}"
            )
            return str(root_folder)

        print(f"Valid suggested path: {suggested_path}")
        return suggested_path
    except Exception as e:
        print(f"Error in get_suggested_path: {str(e)}")
        # En cas d'erreur, retourner le dossier racine
        return str(root_folder)
