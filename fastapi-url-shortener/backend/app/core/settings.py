import os
from dotenv import load_dotenv

load_dotenv()

BASE_PATH = str(os.getenv("BASE_PATH"))
DEBUG = str(os.getenv("DEBUG")).lower() == "true"
PORT = int(os.getenv("PORT"))
DATABASE_PATH = str(os.getenv("DATABASE_PATH"))