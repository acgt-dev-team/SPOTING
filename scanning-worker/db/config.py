from sqlmodel import create_engine
import os
from dotenv import load_dotenv
from .model import tugasan, status

load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

url = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require'

engine = create_engine(url)