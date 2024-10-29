import os
import getpass
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from dsa.reader import DirectoryReader
from dsa.action import RenameDocumentsBasedOnContentAndDate, SampleAction


def main():
    my_loader = DirectoryReader("data")

    my_loaded_docs = my_loader.read()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(
            "Please enter your OpenAI API key: "
        )

    faiss_index = FAISS.from_documents(my_loaded_docs, OpenAIEmbeddings())
    docs = faiss_index.similarity_search(
        "Who is mentioned in this document", k=2
    )
    for doc in docs:
        print(doc.page_content[:300])

    my_action = RenameDocumentsBasedOnContentAndDate("data")
    # my_action = SampleAction()

    my_action.execute()


if __name__ == "__main__":
    main()
