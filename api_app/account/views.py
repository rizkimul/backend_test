from flask import request
from api_app import app, db
from bson.objectid import ObjectId
import uuid
from . import account

@account.route('/register', methods=['POST'])
def register():
    results = {}
    responses = 500
    if 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user_collection = db["user"]
        cursor = user_collection.find({"username": username})

        if cursor.count() == 0:
            if request.form == None:
                results['message'] = "Error: Please input field"
                responses = 400
            else:
                data = {
                'username': username,
                'password': password,
                'email' : email
                }
                user_collection.insert_one(data)
            results['message'] = 'successfully added'
            responses = 201
        else:
            results['message'] = 'Data already added'
            responses = 400    
    else:
        results['message'] = "Error: please input a field!"
        responses = 400
    return results, responses