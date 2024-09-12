from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "5bcc9766461b7dcb89a5eaba3b30caa539fb33c41b641dca493e1f8b29f781e3"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from website import routes
