from langchain_community import tools

class Agent:
    def __init__(self, document_loader: tools.UploadDocument):
        self.document_loader = document_loader

class GoogleDriveAgent(Agent):
    def __init__(self, document_loader: tools.UploadDocument):
        super().__init__(document_loader)

    def upload(self, document_id: str) -> str:
        try:
            return self.document_loader.load(document_id)
        except tools.UploadDocumentError:
            return "Error uploading document to Google Drive"
