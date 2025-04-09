"""
API Document Sorting Assistant

This module provides a FastAPI API to suggest filenames and directories
based on file content analysis.
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
    description="API to suggest file locations and names",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "suggestions",
            "description": "Suggestion operations for document sorting",
        }
    ],
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def create_temp_file(file: UploadFile):
    """
    Creates a temporary file from an uploaded file.

    Args:
        file (UploadFile): The file uploaded by the user

    Yields:
        Path: The path to the created temporary file

    Notes:
        The temporary file is automatically deleted after use.
    """
    temp_path = None
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=f"_{file.filename}"
        )
        temp_path = temp_file.name
        temp_file.close()  # Close the file to avoid access errors

        # Write the file content
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Reset the file for future use
        await file.seek(0)

        yield Path(temp_path)
    finally:
        # Delete the temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                print(f"Temporary file deleted: {temp_path}")
            except Exception as e:
                print(
                    f"Error deleting temporary file: \
                    {str(e)}"
                )


@app.post(
    "/suggest-filename",
    response_model=SuggestFilenameResponse,
    tags=["suggestions"],
    summary="Suggest a filename",
    description="Analyzes a file and suggests a name based on its content",
    response_model_exclude_none=True,
    operation_id="suggestFilename",
)
async def suggest_filename(
    file: UploadFile,
):
    """
    Suggests a filename based on the content of the uploaded file.

    Args:
        file (UploadFile): The file to analyze

    Returns:
        SuggestFilenameResponse: The response containing the suggested name

    Raises:
        HTTPException: If an error occurs during processing
    """
    try:
        async with create_temp_file(file) as temp_path:
            result = get_suggested_file_name(str(temp_path))
            # Extract the string from the CrewOutput object
            suggested_name = (
                result.raw if hasattr(result, "raw") else str(result)
            )
            return SuggestFilenameResponse(suggestion=suggested_name)
    except Exception as e:
        print(f"Error in suggest_filename: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {str(e)}"
        )


@app.post(
    "/suggest-directory",
    response_model=SuggestDirectoryResponse,
    tags=["suggestions"],
    summary="Suggest a directory",
    description="Analyzes a file and suggests the best directory from a list \
         of candidates",
    response_model_exclude_none=True,
    operation_id="suggestDirectory",
)
async def suggest_directory(file: UploadFile, directories: List[str]):
    """
    Suggests a directory for file placement.

    Args:
        file (UploadFile): The file to analyze
        directories (List[str]): List of candidate directories

    Returns:
        SuggestDirectoryResponse: The response containing the suggested \
        directory

    Raises:
        HTTPException: If an error occurs during processing or if
        the directory list is empty
    """
    try:
        # Check that the directory list contains at least one element
        if not directories:
            raise HTTPException(
                status_code=400,
                detail="The directory list cannot be empty",
            )

        async with create_temp_file(file) as temp_path:
            try:
                result = get_suggested_path(str(temp_path), directories)
                # Extract the string from the CrewOutput object
                suggested_directory = (
                    result.raw if hasattr(result, "raw") else str(result)
                )
                return SuggestDirectoryResponse(suggestion=suggested_directory)
            except Exception as e:
                print(
                    f"Error finding suggested directory: \
                        {str(e)}"
                )
                traceback.print_exc()
                raise HTTPException(
                    status_code=500,
                    detail=f"Error finding suggested directory: \
                    {str(e)}",
                )
    except HTTPException:
        # Re-raise already formatted HTTP exceptions
        raise
    except Exception as e:
        print(f"Error in suggest_directory: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global handler for unhandled exceptions.

    Args:
        request: The request that caused the exception
        exc (Exception): The exception that occurred

    Returns:
        JSONResponse: A JSON response with the error message
    """
    error_msg = str(exc)
    traceback_str = traceback.format_exc()
    print(f"Global exception: {error_msg}\n{traceback_str}")
    return JSONResponse(status_code=500, content={"detail": error_msg})
