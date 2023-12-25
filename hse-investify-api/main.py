# main.py
import logging

logging.basicConfig(filename="main.log", level=logging.INFO)
logging.info("api run")

import uvicorn
from app.api import api

uvicorn.run(api, host="0.0.0.0")
