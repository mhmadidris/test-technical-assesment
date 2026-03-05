from sqlalchemy.orm import Session
import json
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)

from app.models.role import Role

class RoleSeeder:
    def __init__(self, session: Session, json_file_path: str) -> None:
        self.session = session
        self.json_file_path = json_file_path
        
    def seed_data(self):
        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)
            
        for item in data:
            existing_role = self.session.query(Role).filter_by(id=item['id']).first()
            
            if existing_role is None:
                role = Role(**item)
                self.session.add(role)
            
        self.session.commit()