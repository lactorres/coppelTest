from flask import Flask, make_response, jsonify
from pymongo import MongoClient
import certifi
import requests

from constants import config, general, api

app = Flask(__name__)


class LayawayApiService():

    def addToLayaway(self, payload, auth):
        requiredParams = ["title", "issueNumber"]
        canContinue, params = self.validateParams(payload, requiredParams)
        if (canContinue):
            isLoggedIn, userData = self.isUserLoggedIn(auth)
            if (isLoggedIn):
                query = {api.ISSUE_NUMBER: params["issueNumber"]}
                canContinue, comicResponse = self.getComics(
                    params["title"], query)
                if canContinue:
                    if (len(comicResponse["comics"]) > 0):
                        if (len(comicResponse["comics"]) == 1):
                            result = self.saveUserComic(
                                userData, comicResponse["comics"][0])
                            return make_response(result)
                        else:
                            return make_response(jsonify({"error": "The where multiple comic results, please refine your searchTerm", "params": params, "comicsFound": comicResponse["comics"]}), 404)
                    else:
                        return make_response(jsonify({"error": "Comic not found", "params": params}), 404)
                return jsonify(comicResponse)
            else:
                return userData
        else:
            return params

    def saveUserComic(self, userData, comic):
        found, userComics = self.getUserComics(userData)
        alreadyExists = [existComic for existComic in userComics if existComic["id"] == comic["id"]]
        if(len(alreadyExists) != 0):
            bodyResult = {
                "status": "The comic was already registered for the user",
                "currentUserComics": userComics
            }
            return bodyResult
        userComics.append(comic)
        payload = {
            "userId": userData["id"],
            "comics": userComics
        }
        usersComicsCon = self.createDbConection()

        if found:
            setComic = {"$set": {"comics": userComics}}
            usersComicsCon.update_one({"userId": userData["id"]}, setComic)
        else:
            usersComicsCon.insert_one(payload)

        usersComicsCon.close
        bodyResult = {
            "status": "success",
            "currentUserComics": userComics
        }
        return bodyResult

    def getUserComics(self, userData):
        usersComicsCon = self.createDbConection()
        usersComicsTMP = []
        found = False
        responseUserComics = usersComicsCon.find_one({"userId": userData["id"]})
        usersComicsCon.close
        if responseUserComics:
            usersComicsTMP = responseUserComics["comics"]
            found = True
        return found, usersComicsTMP
        

    @staticmethod
    def isUserLoggedIn(auth):
        headers = {"Authorization": auth}
        response = requests.request("GET", api.USERS_ENDPOINT, headers=headers)
        if (response.status_code == 200):
            responseData = response.json()
            return True, responseData
        else:
            responseData = response.json()
            return False, make_response(responseData, response.status_code)

    @staticmethod
    def getComics(searchTerm, query):
        response = requests.request(
            "GET", api.COMICS_ENDPOINT + api.COMIC_NAME + searchTerm, params=query)
        if (response.status_code == 200):
            responseData = response.json()
            return True, responseData
        else:
            responseData = response.json()
            return False,  make_response(responseData, response.status_code)

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
        return True, parsedParams

    @staticmethod
    def createDbConection():
        client = MongoClient(config.URI, tlsCAFile=certifi.where())
        db = client.test
        users = db.usersComics
        return users
