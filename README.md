# README

## Lib alone interface (dans lib):
- suggest_filename(file: Path) -> str
- suggest_filedirectory(file: Path, directories: List[str]) -> str

## via le CLI (dans cli, fait appel a la lib)
suggest_filename = "cli.dsa:suggest_filename"
suggest_filedirectory = "cli.dsa:suggest_filedirectory"

## via streamlit (dans ui)
- lancer streamlit run streamlit_entrypoint.py

## via gradio (dans ui)
- lancer python gradio_entrypoint.py

## via fastapi
- cd .\src\app\api
- uvicorn src.api.main:app --reload
