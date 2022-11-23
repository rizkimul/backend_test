from flask import request
from api_app import app, db
from bson.objectid import ObjectId
import uuid
from . import auth

@auth.route('/login', methods=['POST'])
def login():
    results = {}
    responses = 500
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        user_collection = db["user"]
        cursor = user_collection.find({"username": username})

        if cursor.count() == 0:
            results['message'] = "Error: data not found"
            responses = 400
        else:
            for data in cursor:
                if data['password'] == password:
                    data["_id"] = str(data["_id"])
                    access_token = create_access_token(identity=data['password'])
                    account_collection.update_one({
                        "_id": ObjectId(data("_id"))
                    },
                    {
                        "$set":{
                            'token': access_token
                        }
                    }
                    )
                    results['message'] = "Login success"
                    results['token'] = access_token
                    results['data'] = data
                    responses = 200
                    break
                else:
                    results['message'] = "Error: password doesn't match"
                    responses = 400
                    break
    else:
        results['message'] = "Error: please input a field!"
        responses = 400
    return results, responses