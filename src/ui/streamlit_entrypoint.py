import os
import getpass
import streamlit as st
import shutil
import logging
from litellm import completion
from typing import List
from pathlib import Path
from crewai import LLM
from lib import suggest_filename as get_suggested_file_name
from lib import suggest_filedirectory as get_suggested_path

# Must precede any llm module imports

# from langtrace_python_sdk import langtrace

# langtrace.init(api_key = '64a6e4a48594fe5a04465a6667a5fa264baa953cf14d25538e7c502da88df0ef')


# def sanitize_filename(filename):
#     """Remove or replace invalid characters for Windows file system."""
#     invalid_chars = '<>:"/\\|?*'
#     return "".join(
#         "_" if c in invalid_chars else c for c in str(filename)
#     ).strip()


logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_API_KEY = "sk-1111"

# Créer le chemin vers le fichier temporaire dans un dossier "temp" au même niveau que le code
current_dir = Path(__file__).parent
TEMP_DIR = current_dir / "temp"
TEMP_FILE_PATH = TEMP_DIR / "temp_file.pdf"
LOGS_FILE_PATH = current_dir.parent.parent / "logs" / "analyse_file_task.md"

# Créer le répertoire temp s'il n'existe pas
TEMP_DIR.mkdir(exist_ok=True)

def read_logs_file():
    """Lire le contenu du fichier de logs"""
    if LOGS_FILE_PATH.exists():
        return LOGS_FILE_PATH.read_text(encoding="utf-8")
    else:
        return "Le fichier de logs n'existe pas encore."

def main():
    st.title("📝 PDF Naming and Sorting App")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "With the uploaded PDF file, I can help you rename it.",
            }
        ]

    # Upload file section
    pdf_variable = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_variable:
        # Écrire le fichier temporaire
        with TEMP_FILE_PATH.open("wb") as f:
            f.write(pdf_variable.getbuffer())

        st.session_state["messages"].append(
            {
                "role": "user",
                "content": f"User uploaded a PDF file: {pdf_variable.name}",
            }
        )

        if st.button("Process File"):
            # Obtenir le nom suggéré
            suggested_name = get_suggested_file_name(str(TEMP_FILE_PATH))

            # Afficher le résultat
            rename_result = f"## Here is the Rename Result \n\n {suggested_name}"

            st.session_state.messages.append(
                {"role": "assistant", "content": rename_result}
            )

            st.chat_message("assistant").write(rename_result)

            # Lire et afficher le contenu du fichier de logs
            logs_content = read_logs_file()
            st.markdown("## Log File Content")
            st.markdown(logs_content)

            # Journaliser l'information
            logging.info(f"File processed: {pdf_variable.name} -> suggested name: {suggested_name}")


if __name__ == "__main__":
    main()
