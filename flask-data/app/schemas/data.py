from app import ma
from app.models.data import DataEntry

class DataEntrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DataEntry
        load_instance = True
        include_fk = True

data_entry_schema = DataEntrySchema()
data_entries_schema = DataEntrySchema(many=True)
