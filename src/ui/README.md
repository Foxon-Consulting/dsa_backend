# Document Sorting Assistant - Streamlit Interface

This `streamlit_entrypoint.py` file provides a web user interface for the Document Sorting Assistant application.

## Features

- Document upload (PDF, DOCX, TXT, etc.)
- Automatic file name suggestions based on content
- Target directory selection
- Suggestion of the most appropriate directory to classify the document
- Display of processing logs

## Prerequisites

- Python 3.8+
- Streamlit
- Main library dependencies

## Installation

Make sure the necessary dependencies are installed:

```bash
pip install .
pip install .[streamlit]
```

## Usage

To start the Streamlit interface:

```bash
streamlit run src/ui/streamlit_entrypoint.py
```

The application will be accessible in your browser at `http://localhost:8501`.

## User Guide

1. Upload a document using the upload field
2. Click on "Process File" to get a content-based name suggestion
3. Select a root directory to display available subdirectories
4. Click on "Process Directory" to get a suggestion for the directory to classify the document
5. Check the logs to see the processing history
