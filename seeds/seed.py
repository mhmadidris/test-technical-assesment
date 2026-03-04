# import your seeder classes here
from role import RoleSeeder
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.env import env
 
DB_URL = f"postgresql+psycopg2://{env.DB_USERNAME}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_seeder():
    session = SessionLocal()
    
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(absolute_path, 'data')
    
    # Put your class seeder here
    seeders = [
        RoleSeeder(session, os.path.join(dir_path,'role-seed.json'))
    ]
    
    for seeder in seeders:
        seeder.seed_data()
        
    session.close()
    
if __name__ == "__main__":
    run_seeder()