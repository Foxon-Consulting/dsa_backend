# from langchain_community import tools


# class Agent:
#     def __init__(self, document_loader: tools.UploadDocument):
#         self.document_loader = document_loader


# class GoogleDriveAgent(Agent):
#     def __init__(self, document_loader: tools.UploadDocument):
#         super().__init__(document_loader)

#     def upload(self, document_id: str) -> str:
#         try:
#             return self.document_loader.load(document_id)
#         except tools.UploadDocumentError:
#             return "Error uploading document to Google Drive"

#TODO: Implement CrewAI agents

from crewai import Agent, LLM
from textwrap import dedent

class PDFAnalystAgent(Agent):
    def __init__(self, tools: list, llm: LLM):
        super().__init__(
            role="Senior PDF Analyst",
            backstory=dedent(f"""You can find anything in a PDF. The people need you."""),
            goal=dedent(f"""Uncover any information from pdf files exceptionally well."""),
            tools=tools,
            verbose=True,
            llm=llm
        )
