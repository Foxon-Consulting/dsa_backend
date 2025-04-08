import fastapi
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List
from lib import suggest_filename as get_suggested_file_name
from lib import suggest_filedirectory as get_suggested_path
import shutil
import os
import tempfile
import traceback
import re

app = FastAPI(title="Document Sorting Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de réponse
class SuggestionResponse(BaseModel):
    suggestion: str

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_msg = str(exc)
    traceback_str = traceback.format_exc()
    print(f"Global exception: {error_msg}\n{traceback_str}")
    return JSONResponse(status_code=500, content={"detail": error_msg})

@app.post("/suggest-filename", response_model=SuggestionResponse)
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


@app.post("/suggest-filedirectory", response_model=SuggestionResponse)
async def suggest_filedirectory(
    file: UploadFile = File(...),
    root_folder: str = Form(...)
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
