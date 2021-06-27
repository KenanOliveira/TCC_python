from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ASCENDING, DESCENDING
from flask_cors import CORS, cross_origin
import string
import random
import config

app = Flask(__name__)

cors = CORS(app)

app.config['MONGO_DBNAME'] = config.DB_NAME
app.config['MONGO_URI'] = config.MONGO_URI
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = config.SECRET_KEY

mongo = PyMongo(app)