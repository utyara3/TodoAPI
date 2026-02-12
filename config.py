import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "")

if not DB_PATH:
    raise Exception("no db path. check .env")
