from pydantic import BaseModel, Field
from typing import List

# Modèles de requête

# Modèles de réponse
class SuggestFilenameResponse(BaseModel):
    suggestion: str = Field(
        description="Suggestion générée par l'assistant",
        example="2025 01 01 - Rapport de ventes"
    )

class SuggestDirectoryResponse(BaseModel):
    suggestion: str = Field(
        description="Suggestion générée par l'assistant",
        example="Documents/Factures"
    )
