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
