from flask import request
from api_app import app, db
from bson.objectid import ObjectId
import uuid
from . import checklist

@checklist.route('/checklist', methods=['POST', 'GET', 'DELETE'])
def check():
    checklist_collection = db["checklist"]
    results = {}
    responses = 500
    if request.method == 'POST':
        if 'Authorization' in request.headers:
            if 'name' in request.form:
                name = request.form['name']
                data = {
                    'name': name
                    }
                checklist_collection.insert_one(data)
                results['message'] = 'successfully added'
                responses = 201
            else:
                results['message'] = "Error: please input a field!"
                responses = 400
        else:            
            results['message'] = "Your session is expired!"
            results['status'] = "error"
            responses = 403
        return results, responses
    elif request.method == 'GET':
        if 'Authorization' in request.headers:
            collection = checklist_collection.find({})
            for data in collection:
                data["_id"] = str(data["_id"])
                results['data'] = data

                responses = 200

        else:            
            results['message'] = "Your session is expired!"
            results['status'] = "error"
            responses = 403
        return results, responses
    elif request.method == 'DELETE':
        if 'Authorization' in request.headers:
            cursor = checklist_collection.delete_one(
                {"_id": ObjectId(request.form['_id'])}
            )
            if cursor.raw_result['ok']:
                results['message'] = 'Data deleted'
                responses = 200

        else:            
            results['message'] = "Your session is expired!"
            results['status'] = "error"
            responses = 403
        return results, responses


    