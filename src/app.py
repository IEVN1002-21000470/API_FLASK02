from flask import flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app = flask(__name__)

CORS(app)

conexion = MySQL(app)

