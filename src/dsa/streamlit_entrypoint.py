import os
import getpass
import streamlit as st
import shutil
import logging
from litellm import completion
from typing import List
from pathlib import Path
from crewai import LLM
from dsa import get_suggested_file_name, get_suggested_path

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_API_KEY = "sk-1111"
ROOT_FOLDER = Path("tests/dir")
TEMP_FILE_PATH = Path("tests/temp_upload/temp_file.pdf")


def main():

    st.title("📝 PDF Naming and Sorting App")

    reader_model_selection = st.selectbox("Select a model for that wil suggest a name and a path for the following file", ["gpt-3.5-turbo", "gpt-4o-mini", "llama3.2"])

    def get_llm_choice(reader_model_selection):
        if reader_model_selection == "gpt-3.5-turbo":
            llm = LLM(
                api_key = OPENAI_API_KEY,
                model = "gpt-3.5-turbo"
                )
            return llm
        elif reader_model_selection == "gpt-4o-mini":
            llm = LLM(
                api_key = OPENAI_API_KEY,
                model = "gpt-4o-mini"
                )
            return llm
        elif reader_model_selection == "llama3.2":
            llm = LLM(
                api_key = OLLAMA_API_KEY,
                model = "ollama/llama3.2"
                )
            return llm

    llm = get_llm_choice(reader_model_selection)

    # Initialize the message log in session state if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "With the uploaded PDF file, I can help you rename it and sort it.",
            }
        ]

    # Display existing messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Drag and drop file uploader
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

        suggested_name = get_suggested_file_name(TEMP_FILE_PATH, llm)

        # Calling crew to execute renaming tasks
        rename_result = f"## Here is the Rename Result \n\n {suggested_name}"
        st.session_state.messages.append(
            {"role": "assistant", "content": rename_result}
        )
        st.chat_message("assistant").write(rename_result)

        # Calling crew to execute sorting tasks
        suggested_path = Path(get_suggested_path(ROOT_FOLDER, TEMP_FILE_PATH, llm))

        sort_result = f"## Here is the Suggested Path \n\n {str(suggested_path)}"
        st.session_state.messages.append(
            {"role": "assistant", "content": sort_result}
        )
        st.chat_message("assistant").write(sort_result)


        logging.info(f"File name suggestion: {suggested_name}")
        logging.info(f"File path suggestion: {suggested_path}")


    # Confirmation, file moving and renaming
    if st.button("Are you satisfied with the results?", key="satisfaction"):
        if st.radio("Please confirm:", ("Yes", "No")) == "Yes":
            TEMP_FILE_PATH.rename(suggested_path / suggested_name)

            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": f"File has been moved to {suggested_path} and renamed to {suggested_name}",
                }
            )
            st.chat_message("assistant").write(
                f"File has been moved to {suggested_path} and renamed to {suggested_name}"
            )


if __name__ == "__main__":
    main()
