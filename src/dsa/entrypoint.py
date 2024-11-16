import os
import getpass
import streamlit as st
import shutil
import logging
from typing import List
from pathlib import Path
from dsa.crews import RenameCrew, SortCrew
from dsa.task import RenameTask, SortTask
from dsa.agent import PDFAnalystAgent
from crewai import Crew, LLM
from crewai_tools import PDFSearchTool

# Choice of LLM model
llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
)

# Setting Path for sorted directory
def generate_tree(starting_directory: Path = Path("./src/dsa/dir")) -> List[Path]:
    return [p for p in starting_directory.rglob("*") if p.is_dir()]

def main():

    st.title("📝 PDF Naming and Sorting App")

    # Initialize the message log in session state if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "With the uploaded PDF file, I can help you rename it and sort it."}]

    # Display existing messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Drag and drop file uploader
    if pdf_variable := st.file_uploader("Upload a PDF file", type=["pdf"]):
        if pdf_variable:
            file_path = Path("src/dsa/temp_upload/temp_file.pdf")
            with file_path.open("wb") as f:
                f.write(pdf_variable.getbuffer())
            st.session_state["messages"].append({"role": "user", "content": f"User uploaded a PDF file: {pdf_variable.name}"})

        temp_path_file = Path("src/dsa/temp_upload/temp_file.pdf")
        rename_custom_crew = RenameCrew([PDFSearchTool(pdf=str(temp_path_file))], llm)
        final_name = rename_custom_crew.kickoff().raw + ".pdf"

        # Calling crew to execute renaming tasks
        rename_result = f"## Here is the Rename Result \n\n {final_name}"
        st.session_state.messages.append({"role": "assistant", "content": rename_result})
        st.chat_message("assistant").write(rename_result)

        # Calling crew to execute sorting tasks
        paths_list = generate_tree()

        sort_custom_crew = SortCrew([PDFSearchTool(pdf=str(temp_path_file))], llm, paths_list)
        final_path = Path(sort_custom_crew.kickoff().raw)


        sort_result = f"## Here is the Sort Result \n\n {str(final_path)}"
        st.session_state.messages.append({"role": "assistant", "content": sort_result})
        st.chat_message("assistant").write(sort_result)

    # Confirmation, file moving and renaming
    if st.button("Are you satisfied with the results?", key="satisfaction"):
        if st.radio("Please confirm:", ("Yes", "No")) == "Yes":
            temp_path_file.rename(final_path / final_name)

            st.session_state["messages"].append({"role": "assistant", "content": f"File has been moved to {final_path} and renamed to {final_name}"})
            st.chat_message("assistant").write(f"File has been moved to {final_path} and renamed to {final_name}")

if __name__ == "__main__":
    main()
