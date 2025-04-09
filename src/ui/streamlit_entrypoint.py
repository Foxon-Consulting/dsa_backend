import os
import streamlit as st
from pathlib import Path
import logging

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define important paths
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
TEMP_DIR = current_dir / "temp"
TEMP_FILE_PATH = TEMP_DIR / "temp_file.pdf"
LOGS_FILE_PATH = project_root / "logs" / "analyse_file_task.md"
DEFAULT_ROOT_DIR = project_root / "tests" / "dir1"
DEFAULT_ROOT_DIR_2 = project_root / "tests" / "dir2"
# Create necessary directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)


# Prepare some default directories for demonstration
DEFAULT_DIRECTORIES = [
    str(DEFAULT_ROOT_DIR),  # Default directory at the project root
    str(DEFAULT_ROOT_DIR_2),
]


def read_logs_file():
    """Read the contents of the log file"""
    if LOGS_FILE_PATH.exists():
        return LOGS_FILE_PATH.read_text(encoding="utf-8")
    else:
        return "The log file does not exist yet."


def directory_selection_section():
    st.subheader("Select a root directory")

    # Initialize the list of selected directories
    if "selected_directories" not in st.session_state:
        st.session_state.selected_directories = []

    # Reset the directory list if the root directory changes
    if "last_root_dir" not in st.session_state:
        st.session_state.last_root_dir = None

    selected_root_directory = st.selectbox(
        "Select a root directory",
        options=DEFAULT_DIRECTORIES,
        index=0,  # Select the first default directory
    )

    # If the root directory has changed, reset the subdirectory list
    if selected_root_directory != st.session_state.last_root_dir:
        st.session_state.selected_directories = []
        st.session_state.last_root_dir = selected_root_directory

    if selected_root_directory:
        # Find all subdirectories (not files)
        subdirs = [
            d for d in Path(selected_root_directory).glob("*") if d.is_dir()
        ]

        if subdirs:
            st.write(f"Subdirectories found in {selected_root_directory}:")

            # Automatically add all subdirectories to the list
            for subdir in subdirs:
                if str(subdir) not in st.session_state.selected_directories:
                    st.session_state.selected_directories.append(str(subdir))

            # Display the list of found subdirectories
            for subdir in subdirs:
                st.write(f"- {subdir.name}")

            # Summary
            subdir_names = [
                Path(d).name for d in st.session_state.selected_directories
            ]
            st.success(
                f"Subdirectories have been added to the list: \
                     {', '.join(subdir_names)}"
            )
        else:
            st.write("No subdirectories found.")

    return st.session_state.selected_directories


def file_upload_section():
    file_variable = st.file_uploader(
        "Upload a file",
        type=[
            "pdf",
            "docx",
            "doc",
            "txt",
            "csv",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
        ],
    )
    if file_variable is not None:
        with TEMP_FILE_PATH.open("wb") as f:
            f.write(file_variable.getbuffer())
        st.session_state["messages"].append(
            {
                "role": "user",
                "content": f"User uploaded a file: {file_variable.name}",
            }
        )
    return file_variable


def process_file(temp_file_path):
    from lib import suggest_filename

    # Get the suggested name
    suggested_filename = suggest_filename(str(temp_file_path))
    # Display the result
    suggested_filename_result = (
        f"## Here is the Suggested Filename \n\n {suggested_filename}"
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": suggested_filename}
    )
    st.chat_message("assistant").write(suggested_filename_result)
    return suggested_filename


def process_directory(temp_file_path, selected_directories):

    from lib import suggest_directory

    # Get the suggested directory
    suggested_directory = suggest_directory(
        str(temp_file_path), selected_directories
    )

    # Display the result
    suggested_directory_result = (
        f"## Here is the Directory Result \n\n {suggested_directory}"
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": suggested_directory}
    )

    st.chat_message("assistant").write(suggested_directory_result)

    # Log the information
    logging.info(
        f"Directory processed: {selected_directories} -> suggested directory: \
            {suggested_directory}"
    )


def display_logs():
    logs_content = read_logs_file()
    st.markdown("## Log File Content")
    st.markdown(logs_content)


def streamlit_app():
    st.title("📝 Document Sorting Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "With the uploaded PDF file, I can help you rename \
                    it.",
            }
        ]

    file_variable = file_upload_section()
    if file_variable:
        if st.button("Process File") and TEMP_FILE_PATH.exists():
            with st.spinner("Processing file, please wait..."):
                suggested_filename = process_file(TEMP_FILE_PATH)
                display_logs()
                # Log the information
                logging.info(
                    f"File processed: {file_variable.name} -> suggested name: \
                        {suggested_filename}"
                )

    selected_dirs = directory_selection_section()
    if selected_dirs:
        if st.button("Process Directory"):
            if TEMP_FILE_PATH.exists() and file_variable is not None:
                with st.spinner("Processing directory, please wait..."):
                    process_directory(TEMP_FILE_PATH, selected_dirs)
                    display_logs()
            else:
                st.error(
                    "Please upload and process a PDF file before choosing a \
                        directory."
                )


def main():
    import streamlit.web.cli as stcli
    import sys

    sys.argv = ["streamlit", "run", str(Path(__file__).resolve())]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
