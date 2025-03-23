import os
from typing import List
from pathlib import Path
from dsa.crews import RenameCrew, SortCrew
from crewai import LLM
from crewai_tools import PDFSearchTool

temp_path_file = Path("tests/temp_upload/temp_file.pdf")
search_tool = PDFSearchTool(pdf=str(temp_path_file))
n_iterations = 4
inputs = {"topic": "PDF Reading"}
renameing_trained_filename = "rename.pkl"
sorting_trained_filename = "sort.pkl"
model = "gpt-4o-mini"
log_file_name = type(search_tool).__name__ + "_" + model + "_log.md"

# Choice of LLM model
llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=model,
)


# Setting Path for sorted directory
def generate_tree(starting_directory: Path = Path("tests/dir")) -> List[Path]:
    return [p for p in starting_directory.rglob("*") if p.is_dir()]


path_list = generate_tree()


def main():
    try:
        # Create RenameCrew with only essential parameters
        crew = RenameCrew(
            tools=[search_tool],
            llm=llm,
            output_log_file="trained_rename_crew.md",
            trained_model_path=renameing_trained_filename,
        )

        # Call train method with only the required parameters
        crew.train(
            n_iterations=n_iterations,
            inputs=inputs,
            filename=renameing_trained_filename,
        )
    except Exception as e:
        raise Exception(f"Error in training RenameCrew: {e}")


if __name__ == "__main__":
    main()


# def main():
#     try:
#         # Create SortCrew with only essential parameters
#         crew = SortCrew(
#             tools=[search_tool],
#             llm=llm,
#             directory_tree=path_list,
#             output_log_file="trained_sort_crew.md",
#             trained_model_path=sorting_trained_filename
#         )

#         # Call train method with only the required parameters
#         crew.train(
#             n_iterations=n_iterations,
#             inputs=inputs,
#             filename=sorting_trained_filename
#         )
#     except Exception as e:
#         raise Exception(f"Error in training RenameCrew: {e}")

# if __name__ == "__main__":
#     main()
