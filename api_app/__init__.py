from flask import Flask
import pymongo
import os
from flask_jwt_extended import JWTManager

basedir = os.getcwd()

app = Flask(__name__)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = b'\x07\xd5\x8f\xd6k\x82\x1d\xd1\xde$\xe1\x98`\x91V}'
app.config["SECRET_KEY"] = b'\x07\xd5\x8f\xd6k\x82\x1d\xd1\xde$\xe1\x98`\x91V}'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_HEADER_NAME"] = 'Authorization'
app.config["JWT_HEADER_TYPE"] = 'Bearer'
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.backend_test
    mongo.server_info()

    from .auth import auth as auth_blueprint
    from .account import account as account_blueprint
    from .checklist import checklist as checklist_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(checklist_blueprint)
except pymongo.errors.ConnectionFailure:
    print("Could not connect to MongoDB: %s")
