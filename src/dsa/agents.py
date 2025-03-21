from crewai import Agent, LLM
from textwrap import dedent

class PDFAnalystAgent(Agent):
    def __init__(self, tools: list, llm: LLM):

        super().__init__(
            role="Senior PDF Analyst",
            backstory=dedent("""You are an expert in extracting information from PDF files and organizing them in existing directory structures.
            You understand the importance of working only with available directories and not suggesting ones that don't exist."""),
            goal=dedent("""Analyze PDF files to determine their content and suggest the most appropriate existing folder
            for storing them, based only on available directories.
            Never invent or suggest directories that aren't in the provided list of available paths."""),
            tools=tools,
            verbose=True,
            llm=llm
        )
