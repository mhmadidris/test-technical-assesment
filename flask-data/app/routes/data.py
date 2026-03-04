from flask import Blueprint, jsonify, request
from app.models.data import DataEntry
from app.schemas.data import data_entries_schema, data_entry_schema
from app import db

data_bp = Blueprint('data', __name__)

@data_bp.route('/', methods=['GET'])
def get_all_data():
    entries = DataEntry.query.all()
    return jsonify(data_entries_schema.dump(entries))

@data_bp.route('/<uuid:id>', methods=['GET'])
def get_data(id):
    entry = DataEntry.query.get_or_404(id)
    return jsonify(data_entry_schema.dump(entry))

@data_bp.route('/', methods=['POST'])
def create_data():
    data = request.get_json()
    new_entry = data_entry_schema.load(data, session=db.session)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(data_entry_schema.dump(new_entry)), 201
