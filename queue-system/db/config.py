from sqlmodel import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

url = f'postgresql+psycopg2://{db_username}:{quote_plus(db_password)}@{db_host}:{db_port}/{db_name}'

engine = create_engine(url)
