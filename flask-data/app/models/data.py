import uuid
from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID

class DataEntry(db.Model):
    __tablename__ = 'data_entries'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<DataEntry {self.title}>'
