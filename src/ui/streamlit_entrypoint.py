import os
import getpass
import streamlit as st
import shutil
import logging
from litellm import completion
from typing import List
from pathlib import Path
from crewai import LLM
from dsa.__init__ import get_suggested_file_name, get_suggested_path

# Must precede any llm module imports

# from langtrace_python_sdk import langtrace

# langtrace.init(api_key = '64a6e4a48594fe5a04465a6667a5fa264baa953cf14d25538e7c502da88df0ef')

def sanitize_filename(filename):
    """Remove or replace invalid characters for Windows file system."""
    invalid_chars = '<>:"/\\|?*'
    return ''.join('_' if c in invalid_chars else c for c in str(filename)).strip()

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
ROOT_FOLDER = Path("tests/dir")
TEMP_FILE_PATH = Path("tests/temp_upload/temp_file.pdf")




def main():
    st.title("📝 PDF Naming and Sorting App")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "With the uploaded PDF file or folder, I can help you rename it and sort it.",
            }
        ]
    if "upload_type" not in st.session_state:
        st.session_state.upload_type = "File"

    reader_model_selection = st.selectbox("Select a model for that wil suggest a name and a path for the following file", ["claude haiku", "deepseek", "gpt-4o-mini"])

    def get_llm_choice(reader_model_selection):
        if reader_model_selection == "claude haiku":
            llm = LLM(
                api_key = CLAUDE_API_KEY,
                model = "claude-3-haiku-20240307"
                )
            return llm
        elif reader_model_selection == "gpt-4o-mini":
            llm = LLM(
                api_key = OPENAI_API_KEY,
                model = "gpt-4o-mini"
                )
            return llm
        elif reader_model_selection == "deepseek":
            llm = LLM(
                api_key = DEEPSEEK_API_KEY,
                model = "deepseek/deepseek-chat"
                )
            return llm

    llm = get_llm_choice(reader_model_selection)

    # Initialize session state for upload type
    if "upload_type" not in st.session_state:
        st.session_state["upload_type"] = "File"

    # Upload type selection
    upload_type = st.radio("Select upload type:", ("File", "Folder"))
    st.session_state["upload_type"] = upload_type

    if upload_type == "File":
        if pdf_variable := st.file_uploader("Upload a PDF file", type=["pdf"]):
            if pdf_variable:
                with TEMP_FILE_PATH.open("wb") as f:
                    f.write(pdf_variable.getbuffer())
                st.session_state["messages"].append(
                    {
                        "role": "user",
                        "content": f"User uploaded a PDF file: {pdf_variable.name}",
                    }
                )

                suggested_name = sanitize_filename(get_suggested_file_name(TEMP_FILE_PATH, llm))
                suggested_path = get_suggested_path(ROOT_FOLDER, TEMP_FILE_PATH, llm)

                rename_result = f"## Here is the Rename Result \n\n {suggested_name}"
                sort_result = f"## Here is the Path Result \n\n {suggested_path}"

                st.session_state.messages.extend([
                    {"role": "assistant", "content": rename_result},
                    {"role": "assistant", "content": sort_result}
                ])

                st.chat_message("assistant").write(rename_result)
                st.chat_message("assistant").write(sort_result)

                # Automatically move and rename the file
                target_path = Path(suggested_path) / suggested_name
                target_path.parent.mkdir(parents=True, exist_ok=True)
                TEMP_FILE_PATH.rename(target_path)

                success_message = f"File has been renamed to {suggested_name} and moved to {suggested_path}"
                st.session_state.messages.append({"role": "assistant", "content": success_message})
                st.chat_message("assistant").write(success_message)

                logging.info(f"File processed: {success_message}")

    else:  # Folder upload
        if zip_file := st.file_uploader("Upload a ZIP folder", type=["zip"]):
            if zip_file:
                # Create temporary directory for extraction
                temp_dir = Path("temp_extract")
                temp_dir.mkdir(exist_ok=True)

                # Save and extract zip file
                zip_path = temp_dir / "upload.zip"
                with zip_path.open("wb") as f:
                    f.write(zip_file.getbuffer())

                # Extract zip file
                import zipfile
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Process each PDF in the extracted folder
                for pdf_file in temp_dir.glob("**/*.pdf"):
                    # Get suggestions
                    suggested_name = sanitize_filename(get_suggested_file_name(pdf_file, llm))
                    suggested_path = get_suggested_path(ROOT_FOLDER, pdf_file, llm)

                    # Display suggestions
                    rename_result = f"## Rename suggestion for {pdf_file.name}\n\n{suggested_name}"
                    sort_result = f"## Path suggestion\n\n{suggested_path}"

                    st.session_state.messages.extend([
                        {"role": "assistant", "content": rename_result},
                        {"role": "assistant", "content": sort_result}
                    ])

                    st.chat_message("assistant").write(rename_result)
                    st.chat_message("assistant").write(sort_result)

                    # Automatically move and rename the file
                    target_path = Path(suggested_path) / suggested_name
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    pdf_file.rename(target_path)

                    logging.info(f"File processed: {pdf_file.name} -> {target_path}")

                # Clean up temporary directory
                shutil.rmtree(temp_dir)

                success_message = "All files have been processed and moved to their suggested locations."
                st.session_state.messages.append({"role": "assistant", "content": success_message})
                st.chat_message("assistant").write(success_message)

if __name__ == "__main__":
    main()
