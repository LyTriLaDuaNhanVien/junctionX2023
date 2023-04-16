import os
from dotenv import load_dotenv
load_dotenv()
import pymongo
mongo_conection_string=os.getenv("CONNECTION_STRING")

