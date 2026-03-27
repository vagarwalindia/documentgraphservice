from infrastructure.db.models import DocumentORM

class DocumentRepository:
    def __init__(self, session):
        self.session = session

    async def create_structured_document(self, document_id: str, structure: dict):
        # You can store JSON in Postgres JSONB column
        db_obj = DocumentORM(id=document_id, status="processed", structure=structure)
        self.session.add(db_obj)
        await self.session.commit()