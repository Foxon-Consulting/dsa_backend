import os
import shutil
import logging
from typing import List
from pathlib import Path
from crewai import LLM
from dsa import get_suggested_file_name, get_suggested_path
import gradio as gr

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


def get_llm_choice(reader_model_selection):
    if reader_model_selection == "gpt-3.5-turbo":
        llm = LLM(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
        return llm
    elif reader_model_selection == "gpt-4o-mini":
        llm = LLM(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
        return llm
    elif reader_model_selection == "llama3.2":
        llm = LLM(api_key=OLLAMA_API_KEY, model="ollama/llama3.2")
        return llm


def process_pdf(pdf_path, reader_model_selection):
    llm = get_llm_choice(reader_model_selection)

    shutil.copy(pdf_path, TEMP_FILE_PATH)

    suggested_name = get_suggested_file_name(TEMP_FILE_PATH, llm)
    suggested_path = Path(get_suggested_path(ROOT_FOLDER, TEMP_FILE_PATH, llm))

    logging.info(f"File name suggestion: {suggested_name}")
    logging.info(f"File path suggestion: {suggested_path}")

    return suggested_name, str(suggested_path)


def confirm_results(confirm, suggested_name, suggested_path):
    suggested_path = Path(suggested_path)
    if confirm == "Yes":
        new_path = suggested_path / suggested_name
        TEMP_FILE_PATH.rename(new_path)
        return f"File has been moved to {suggested_path} and renamed to {suggested_name}"
    else:
        return "Please make the necessary adjustments and try again."


def main():
    with gr.Blocks() as demo:
        gr.Markdown("# 📝 PDF Naming and Sorting App")

        reader_model_selection = gr.Dropdown(
            choices=["gpt-3.5-turbo", "gpt-4o-mini", "llama3.2"],
            label="Select a model for that will suggest a name and a path for the following file",
        )

        pdf_variable = gr.File(label="Upload a PDF file", type="filepath")

        suggested_name_output = gr.Textbox(label="Suggested Name")
        suggested_path_output = gr.Textbox(label="Suggested Path")

        process_button = gr.Button("Process PDF")
        process_button.click(
            process_pdf,
            inputs=[pdf_variable, reader_model_selection],
            outputs=[suggested_name_output, suggested_path_output],
        )

        confirm = gr.Radio(
            choices=["Yes", "No"], label="Are you satisfied with the results?"
        )
        confirm_button = gr.Button("Confirm")
        confirm_output = gr.Textbox(label="Confirmation Result")

        confirm_button.click(
            confirm_results,
            inputs=[confirm, suggested_name_output, suggested_path_output],
            outputs=confirm_output,
        )

    demo.launch()


if __name__ == "__main__":
    main()
