from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

jwt = JWTManager()
cors = CORS()
client = MongoClient(Config.MONGO_URI)
db = client.eventpro
