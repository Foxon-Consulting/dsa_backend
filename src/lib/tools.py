from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from docling.document_converter import DocumentConverter


class DoclingToolInput(BaseModel):
    file_path: str = Field(
        ..., description="The path to the PDF file to convert"
    )


class DoclingMarkdownTool(BaseTool):
    name: str = "docling_markdown"
    description: str = (
        "Use this tool to convert: \
      - PDF files to markdown files \
      - PNG files to markdown files \
      - JPG files to markdown files \
      - JPEG files to markdown files \
      - TIFF files to markdown files \
      - GIF files to markdown files \
      - BMP files to markdown files"
    )
    args_schema: Type[BaseModel] = DoclingToolInput

    def _run(self, file_path: str) -> str:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()


class DoclingTextTool(BaseTool):
    name: str = "docling_text"
    description: str = (
        "Use this tool to convert: \
      - PDF files to text files \
      - PNG files to text files \
      - JPG files to text files \
      - JPEG files to text files \
      - TIFF files to text files \
      - GIF files to text files \
      - BMP files to text files"
    )
    args_schema: Type[BaseModel] = DoclingToolInput

    def _run(self, file_path: str) -> str:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_text()
