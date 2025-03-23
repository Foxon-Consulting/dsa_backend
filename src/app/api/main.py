import fastapi
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List
from dsa import get_suggested_file_name, get_suggested_path, get_tree
import shutil
import os
import tempfile
import traceback
import re

app = FastAPI(title="Document Sorting Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DirectoryTreeResponse(BaseModel):
    tree: List[Path]


class DirectoryTreeRequest(BaseModel):
    root_folder: Path


class FileNameRequest(BaseModel):
    file_path: str


class FilePathRequest(BaseModel):
    root_folder: str
    file_path: str


class SuggestionResponse(BaseModel):
    suggestion: str


class MoveAndRenameRequest(BaseModel):
    new_name: str
    new_path: str


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_msg = str(exc)
    traceback_str = traceback.format_exc()
    print(f"Global exception: {error_msg}\n{traceback_str}")
    return JSONResponse(status_code=500, content={"detail": error_msg})


@app.get("/")
def read_root():
    return {"message": "Welcome to Document Sorting Assistant API"}


@app.get("/get-tree", response_model=DirectoryTreeResponse)
def get_tree_endpoint(request: DirectoryTreeRequest):
    try:
        tree_result = get_tree(request.root_folder)
        return DirectoryTreeResponse(tree=tree_result)
    except Exception as e:
        print(f"Error in get_tree: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error getting tree: {str(e)}"
        )


@app.post("/suggest-filename")
async def suggest_filename(file: UploadFile = File(...)):
    temp_path = None
    temp_file = None
    try:
        # Créer un fichier temporaire pour stocker le fichier uploadé
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=f"_{file.filename}"
        )
        temp_path = temp_file.name
        temp_file.close()  # Fermer le fichier pour éviter les erreurs d'accès

        # Écrire le contenu du fichier par morceaux pour éviter les problèmes de mémoire
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Réinitialiser le fichier pour une utilisation ultérieure
        await file.seek(0)

        # Utiliser ce fichier temporaire comme entrée pour get_suggested_file_name
        suggested_name = get_suggested_file_name(Path(temp_path))

        return SuggestionResponse(suggestion=suggested_name)
    except Exception as e:
        print(f"Error in suggest_filename: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}"
        )
    finally:
        # Supprimer le fichier temporaire
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                print(f"Successfully deleted temp file: {temp_path}")
            except Exception as e:
                print(f"Failed to delete temp file: {str(e)}")


@app.post("/suggest-path")
async def suggest_path(
    file: UploadFile = File(...), root_folder: str = Form(...)
):
    temp_path = None
    temp_file = None
    try:
        # Déterminer le chemin absolu du dossier racine fourni par l'utilisateur
        if not os.path.isabs(root_folder):
            root_path = Path(os.getcwd()) / root_folder
        else:
            root_path = Path(root_folder)

        print(f"Using user-provided output directory: {root_path}")

        # Vérifier si le dossier existe
        if not root_path.exists() or not root_path.is_dir():
            print(
                f"Warning: User-provided directory {root_path} does not exist"
            )
            return JSONResponse(
                status_code=404,
                content={
                    "detail": f"Output directory does not exist: {root_folder}",
                    "suggestion": str(root_path),
                },
            )

        # Créer un fichier temporaire pour stocker le fichier uploadé
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=f"_{file.filename}"
        )
        temp_path = temp_file.name
        temp_file.close()  # Fermer le fichier pour éviter les erreurs d'accès

        # Écrire le contenu du fichier par morceaux pour éviter les problèmes de mémoire
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Réinitialiser le fichier pour une utilisation ultérieure
        await file.seek(0)

        # Utiliser ce fichier temporaire comme entrée pour get_suggested_path
        try:
            suggested_path = get_suggested_path(root_path, Path(temp_path))

            # Vérifier si le chemin suggéré est valide et existe
            suggested_path_obj = Path(suggested_path)
            if (
                not suggested_path_obj.exists()
                or not suggested_path_obj.is_dir()
            ):
                print(
                    f"Warning: Suggested path '{suggested_path}' does not exist, using root folder"
                )
                suggested_path = str(root_path)

            print(f"Suggested path for {file.filename}: {suggested_path}")
            return SuggestionResponse(suggestion=suggested_path)
        except Exception as e:
            print(f"Error getting suggested path: {str(e)}")
            # En cas d'erreur, retourner le dossier racine
            return SuggestionResponse(suggestion=str(root_path))
    except Exception as e:
        print(f"Error in suggest_path: {str(e)}")
        traceback.print_exc()
        # En cas d'erreur globale, retourner le dossier root_folder tel quel
        return SuggestionResponse(suggestion=root_folder)
    finally:
        # Supprimer le fichier temporaire
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                print(f"Successfully deleted temp file: {temp_path}")
            except Exception as e:
                print(f"Failed to delete temp file: {str(e)}")


@app.post("/move-and-rename")
async def move_and_rename_file(
    file: UploadFile = File(...),
    new_name: str = Form(...),
    new_path: str = Form(...),
):
    try:
        print(f"Moving file {file.filename} to {new_path}/{new_name}")

        # Vérifier si le chemin fourni est valide
        path_obj = Path(new_path)

        # Vérifier si le répertoire existe
        if not os.path.exists(new_path):
            # Si le dossier n'existe pas, demander à l'utilisateur s'il souhaite le créer
            # Pour l'instant, nous créons automatiquement le dossier, mais nous pourrions
            # ajouter une option pour demander confirmation à l'utilisateur dans le futur
            print(f"Directory {new_path} does not exist. Creating it.")
            try:
                os.makedirs(new_path, exist_ok=True)
                print(f"Directory created: {new_path}")
            except Exception as e:
                print(f"Failed to create directory {new_path}: {str(e)}")
                # Si nous ne pouvons pas créer le dossier, utiliser le dossier parent s'il existe
                parent_dir = os.path.dirname(new_path)
                if os.path.exists(parent_dir):
                    new_path = parent_dir
                    print(f"Using parent directory instead: {new_path}")
                else:
                    # Si même le dossier parent n'existe pas, essayer d'utiliser le répertoire courant
                    new_path = os.getcwd()
                    print(f"Using current directory instead: {new_path}")

        # Vérifier à nouveau si le répertoire existe après les tentatives de création/fallback
        if not os.path.exists(new_path):
            error_msg = f"Cannot access or create directory {new_path}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        # Construct the full target path
        target_path = os.path.join(new_path, new_name)

        # Vérifier si le fichier existe déjà
        if os.path.exists(target_path):
            # Ajouter un suffixe au nom du fichier
            base_name, extension = os.path.splitext(new_name)
            counter = 1
            while os.path.exists(target_path):
                new_name_with_counter = f"{base_name}_{counter}{extension}"
                target_path = os.path.join(new_path, new_name_with_counter)
                counter += 1
            print(f"File already exists. Using new name: {target_path}")

        # Save the uploaded file to the target location
        content = await file.read()
        with open(target_path, "wb") as f:
            f.write(content)

        return {
            "message": f"File moved and renamed successfully to {target_path}",
            "target_path": target_path,
            "new_name": os.path.basename(target_path),
            "new_path": os.path.dirname(target_path),
        }
    except Exception as e:
        print(f"Error in move_and_rename_file: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}"
        )


@app.post("/explore-directory")
async def explore_directory(root_folder: str = Form(...)):
    try:
        print(f"Exploring directory tree for: {root_folder}")

        # Nettoyer le chemin fourni au cas où il contiendrait des éléments comme "path.txt"
        # qui peuvent être ajoutés par erreur lors de l'extraction du chemin par certains navigateurs
        clean_folder = root_folder

        # Supprimer "path.txt" ou tout autre fichier potentiellement ajouté à la fin du chemin
        if os.path.isfile(root_folder):
            print(
                f"Warning: Received a file path instead of a directory: {root_folder}"
            )
            clean_folder = os.path.dirname(root_folder)
            print(f"Using parent directory instead: {clean_folder}")

        # Vérifier spécifiquement le cas de path.txt
        if clean_folder.endswith("path.txt"):
            clean_folder = clean_folder[:-8]  # Enlever "path.txt"
            print(f"Removed path.txt from the end of the path: {clean_folder}")

        # Corriger les problèmes de nom d'utilisateur sur Windows
        if os.name == "nt":  # Windows
            # Vérifier si le chemin semble contenir un utilisateur Windows générique
            windows_path_pattern = r"^[A-Z]:\\Users\\(?:User|Username)\\(.+)$"
            matches = re.search(
                windows_path_pattern, clean_folder, re.IGNORECASE
            )
            if matches:
                # Obtenir le vrai chemin utilisateur
                documents_subpath = matches.group(1)
                real_user_folder = os.path.expanduser(
                    "~"
                )  # Obtient le chemin réel de l'utilisateur actuel
                corrected_path = os.path.join(
                    real_user_folder, documents_subpath
                )
                print(
                    f"Corrected user path from {clean_folder} to {corrected_path}"
                )
                clean_folder = corrected_path

        # Déterminer le chemin absolu du dossier racine fourni par l'utilisateur
        if not os.path.isabs(clean_folder):
            root_path = Path(os.getcwd()) / clean_folder
        else:
            root_path = Path(clean_folder)

        print(f"Using user-provided output directory: {root_path}")

        # Vérifier si le dossier existe
        if not root_path.exists() or not root_path.is_dir():
            print(
                f"Warning: User-provided directory {root_path} does not exist"
            )

            # Vérifier s'il y a des parties du chemin qui existent
            parent_path = root_path
            while (
                parent_path != parent_path.parent and not parent_path.exists()
            ):
                parent_path = parent_path.parent

            if parent_path.exists() and parent_path.is_dir():
                print(f"Found valid parent directory: {parent_path}")
                root_path = parent_path

                # Retourner cette information mais avec un avertissement
                directory_tree = get_tree(root_path)
                formatted_tree = (
                    [str(p) for p in directory_tree]
                    if directory_tree
                    else [str(root_path)]
                )

                return {
                    "root_folder": str(root_path),
                    "directory_tree": formatted_tree,
                    "count": len(formatted_tree),
                    "warning": f"Directory {clean_folder} not found. Using {root_path} instead.",
                }
            else:
                # Retourner un message d'erreur mais avec un statut 200 pour ne pas bloquer l'interface
                return {
                    "root_folder": str(root_path),
                    "directory_tree": [
                        str(root_path)
                    ],  # Au moins le dossier racine
                    "count": 1,
                    "warning": f"Directory {clean_folder} does not exist. Please provide a valid directory.",
                }

        # Obtenir l'arborescence complète des dossiers
        directory_tree = get_tree(root_path)

        # Si l'arborescence est vide, inclure au moins le dossier racine
        if not directory_tree and root_path.exists():
            directory_tree = [root_path]

        # Formater les résultats pour une meilleure lisibilité
        formatted_tree = [str(p) for p in directory_tree]

        print(f"Directory tree: {formatted_tree}")

        return {
            "root_folder": str(root_path),
            "directory_tree": formatted_tree,
            "count": len(formatted_tree),
            "warning": (
                "No subdirectories found in the selected directory. Files will be placed in the root folder."
                if len(formatted_tree) <= 1
                else None
            ),
        }
    except Exception as e:
        print(f"Error exploring directory: {str(e)}")
        traceback.print_exc()
        # Au lieu de générer une erreur, retourner une structure minimale
        return {
            "root_folder": str(root_folder),
            "directory_tree": [str(root_folder)],  # Au moins le dossier racine
            "count": 1,
            "error": f"Error exploring directory: {str(e)}",
        }
