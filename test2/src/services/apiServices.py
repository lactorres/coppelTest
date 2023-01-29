from flask import Flask, make_response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from pymongo import MongoClient
import hashlib
import certifi

from constants import config, general

app = Flask(__name__)


class UsersApiService():

    def registerUser(self, payload):
        requiredParams = ["email", "password", "name", "age"]
        canContinue, params = self.validateParams(payload, requiredParams)
        if (canContinue):
            users = self.createDbConection()
            if users.find_one({"email": params["email"]}):
                users.close
                return make_response(jsonify({"error": "Email already exists"}), 400)
            else:
                users.insert_one(params)
                users.close
                return make_response(jsonify({"status": "created"}), 201)
        else:
            return params

    def loginUser(self, payload):
        requiredParams = ["email", "password"]
        canContinue, params = self.validateParams(payload, requiredParams)
        if (canContinue):
            users = self.createDbConection()
            currentUser = users.find_one({"email": params["email"]})
            if currentUser:
                users.close
                if (currentUser["password"] == params["password"]):
                    access_token = create_access_token(
                        identity=currentUser['email']) 
                    setToken = { "$set": { "token": access_token } }
                    users.update_one({"email": params["email"]}, setToken)
                    return make_response(jsonify({"access_token": access_token}), 200)
                else:
                    return make_response(jsonify({"error": "Email or password incorrect, please verify"}), 401)
            else:
                users.close
                return make_response(jsonify({"error": "Email doesn't exists"}), 401)
        else:
            return params

    @jwt_required()
    def getUser(self):
        current_user = get_jwt_identity()
        users = self.createDbConection()
        currentUser = users.find_one({"email": current_user})
        if currentUser:
            response = {}
            response["id"] = str(currentUser.get('_id'))
            response["name"] = currentUser["name"]
            response["age"] = currentUser["age"]
            response["token"] = currentUser["token"]

            return make_response(response, 200)
        else:
            users.close
            return make_response(jsonify({"error": "Email doesn't exists"}), 401)

    @staticmethod
    def parsePassword(password):
        hashKey = password.encode('utf-8')
        result = hashlib.md5(hashKey)
        return result.hexdigest()

    def validateParams(self, payload, requiredParams):
        parsedParams = {}
        missingParams = []
        for requiredParam in requiredParams:
            if requiredParam in payload and payload[requiredParam].strip() != general.EMPTY_STRING:
                parsedParams[requiredParam] = payload[requiredParam].strip()
            else:
                missingParams.append(requiredParam)
        if (len(missingParams) > 0):
            return False, make_response(jsonify({"error": "Missing params", "missingParams": missingParams}), 400)
        parsedParams["password"] = self.parsePassword(
            parsedParams["password"])
        return True, parsedParams

    @staticmethod
    def createDbConection():
        client = MongoClient(config.URI, tlsCAFile=certifi.where())
        db = client.test
        users = db.users
        return users
