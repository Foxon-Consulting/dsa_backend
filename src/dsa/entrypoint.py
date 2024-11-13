import os
import getpass
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from dsa.reader import DirectoryReader
# from dsa.action import RenameDocumentsBasedOnContentAndDate, SampleAction
from dsa.task import RenameTask, SortTask
from dsa.agent import PDFAnalystAgent
from crewai import Crew, LLM
from crewai_tools import PDFSearchTool

llm = LLM(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
)


def main():
    # my_loader = DirectoryReader("data")

    # my_loaded_docs = my_loader.read()

    # if not os.environ.get("OPENAI_API_KEY"):
    #     os.environ["OPENAI_API_KEY"] = getpass.getpass(
    #         "Please enter your OpenAI API key: "
    #     )

    # faiss_index = FAISS.from_documents(my_loaded_docs, OpenAIEmbeddings())
    # docs = faiss_index.similarity_search(
    #     "Who is mentioned in this document", k=2
    # )
    # for doc in docs:
    #     print(doc.page_content[:300])

    # my_action = RenameDocumentsBasedOnContentAndDate("data")
    # # my_action = SampleAction()

    # my_action.execute()

    def generate_tree(starting_directory):
        tree = ""
        for root, directories, files in os.walk(starting_directory):
            tree += f"Directory: {root}\n"

        if tree == "":
            raise ValueError("The directory is empty")

        return tree

    dir_tree = generate_tree("src/dsa/dir")

    class CustomCrew:
        def __init__(self, tools, llm, directory_tree):
            self.tools = tools
            self.llm = llm
            self.directory_tree = directory_tree

        def run(self):
            custom_agent = PDFAnalystAgent(self.tools, self.llm)

            custom_task_1 = RenameTask(custom_agent)
            custom_task_2 = SortTask(custom_agent, self.directory_tree)

            crew = Crew(
                agent=custom_agent,
                tasks=[custom_task_1, custom_task_2],
                verbose=True,
            )

            final = crew.kickoff()
            return final

    custom_crew = CustomCrew([PDFSearchTool("src/dsa/meeting_minutes_template.pdf")], llm, dir_tree)
    final = custom_crew.run()

if __name__ == "__main__":
    main()
