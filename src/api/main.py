"""
API Document Sorting Assistant

Ce module fournit une API FastAPI pour suggérer des noms de fichiers et des
répertoires
basés sur l'analyse du contenu des fichiers.
"""

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
from lib import suggest_filename as get_suggested_file_name
from lib import suggest_directory as get_suggested_path
import os
import tempfile
import traceback
from .models.schemas import SuggestFilenameResponse, SuggestDirectoryResponse
from contextlib import asynccontextmanager
from typing import List

app = FastAPI(
    title="Document Sorting Assistant API",
    description="API pour suggérer des emplacements et noms de fichiers",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "suggestions",
            "description": "Opérations de suggestion pour le tri de documents",
        }
    ],
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def create_temp_file(file: UploadFile):
    """
    Crée un fichier temporaire à partir d'un fichier uploadé.

    Args:
        file (UploadFile): Le fichier uploadé par l'utilisateur

    Yields:
        Path: Le chemin vers le fichier temporaire créé

    Notes:
        Le fichier temporaire est automatiquement supprimé à la fin de
        l'utilisation.
    """
    temp_path = None
    try:
        # Créer un fichier temporaire
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=f"_{file.filename}"
        )
        temp_path = temp_file.name
        temp_file.close()  # Fermer le fichier pour éviter les erreurs d'accès

        # Écrire le contenu du fichier
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Réinitialiser le fichier pour une utilisation ultérieure
        await file.seek(0)

        yield Path(temp_path)
    finally:
        # Supprimer le fichier temporaire
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                print(f"Fichier temporaire supprimé: {temp_path}")
            except Exception as e:
                print(
                    f"Erreur lors de la suppression du fichier temporaire: \
                    {str(e)}"
                )


@app.post(
    "/suggest-filename",
    response_model=SuggestFilenameResponse,
    tags=["suggestions"],
    summary="Suggérer un nom de fichier",
    description="Analyse un fichier et suggère un nom basé sur son contenu",
    response_model_exclude_none=True,
    operation_id="suggestFilename",
)
async def suggest_filename(
    file: UploadFile,
):
    """
    Suggère un nom de fichier basé sur le contenu du fichier uploadé.

    Args:
        file (UploadFile): Le fichier à analyser

    Returns:
        SuggestFilenameResponse: La réponse contenant le nom suggéré

    Raises:
        HTTPException: Si une erreur survient pendant le traitement
    """
    try:
        async with create_temp_file(file) as temp_path:
            result = get_suggested_file_name(str(temp_path))
            # Extraire la chaîne de l'objet CrewOutput
            suggested_name = (
                result.raw if hasattr(result, "raw") else str(result)
            )
            return SuggestFilenameResponse(suggestion=suggested_name)
    except Exception as e:
        print(f"Erreur dans suggest_filename: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}"
        )


@app.post(
    "/suggest-directory",
    response_model=SuggestDirectoryResponse,
    tags=["suggestions"],
    summary="Suggérer un répertoire",
    description="Analyse un fichier et suggère le meilleur répertoire parmi \
        une liste de candidats",
    response_model_exclude_none=True,
    operation_id="suggestDirectory",
)
async def suggest_directory(file: UploadFile, directories: List[str]):
    """
    Suggère un répertoire pour le placement du fichier.

    Args:
        file (UploadFile): Le fichier à analyser
        directories (List[str]): Liste des répertoires candidats

    Returns:
        SuggestDirectoryResponse: La réponse contenant le répertoire suggéré

    Raises:
        HTTPException: Si une erreur survient pendant le traitement ou si
        la liste des répertoires est vide
    """
    try:
        # Vérifier que la liste des répertoires contient au moins un élément
        if not directories:
            raise HTTPException(
                status_code=400,
                detail="La liste des répertoires ne peut pas être vide",
            )

        async with create_temp_file(file) as temp_path:
            try:
                result = get_suggested_path(str(temp_path), directories)
                # Extraire la chaîne de l'objet CrewOutput
                suggested_directory = (
                    result.raw if hasattr(result, "raw") else str(result)
                )
                return SuggestDirectoryResponse(suggestion=suggested_directory)
            except Exception as e:
                print(
                    f"Erreur lors de la recherche du répertoire suggéré: \
                        {str(e)}"
                )
                traceback.print_exc()
                raise HTTPException(
                    status_code=500,
                    detail=f"Erreur lors de la recherche du répertoire \
                    suggéré: {str(e)}",
                )
    except HTTPException:
        # Re-lever les HTTP exceptions déjà formatées
        raise
    except Exception as e:
        print(f"Erreur dans suggest_directory: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Gestionnaire global des exceptions non gérées.

    Args:
        request: La requête qui a provoqué l'exception
        exc (Exception): L'exception qui s'est produite

    Returns:
        JSONResponse: Une réponse JSON avec le message d'erreur
    """
    error_msg = str(exc)
    traceback_str = traceback.format_exc()
    print(f"Exception globale: {error_msg}\n{traceback_str}")
    return JSONResponse(status_code=500, content={"detail": error_msg})
