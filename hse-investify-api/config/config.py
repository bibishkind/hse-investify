# config.py
import dotenv
import os
import logging

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
logging.info("config init")
logging.info(f"DATABASE_URL: {DATABASE_URL}")
