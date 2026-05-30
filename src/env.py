import os
from dotenv import load_dotenv


load_dotenv()

// read from env

DB_DATABASE = str(os.getenv('DB_DATABASE'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_PORT = int(os.getenv('DB_PORT'))
DB_USER = str(os.getenv('DB_USER'))
