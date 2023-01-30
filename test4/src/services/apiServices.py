from flask import Flask, make_response, jsonify
from pymongo import MongoClient
import certifi
import requests

from constants import config, api

app = Flask(__name__)


class LayawayApiService():

    def getLayawayList(self, auth, args):
        isLoggedIn, userData = self.isUserLoggedIn(auth, args)
        if (isLoggedIn):
            canContinue, comicResponse = self.getUserComics(userData, args)
            if canContinue:
                if (len(comicResponse) > 0):
                    return make_response(jsonify(comicResponse))
            return make_response(jsonify({"error": "This user doesn't have saved comics"}), 404)
        else:
            return userData
    
    def getUserComics(self, userData, args):
        usersComicsCon = self.createDbConection()
        usersComicsTMP = []
        found = False
        responseUserComics = usersComicsCon.find_one(
            {"userId": userData["id"]})
        usersComicsCon.close
        if responseUserComics:
            usersComicsTMP = responseUserComics["comics"]
            found = True
            try:
                if args["orderByIssueNumber"] == "asc":
                    usersComicsTMP = sorted(usersComicsTMP, key=lambda x: x["issueNumber"])

                if args["orderByIssueNumber"] == "desc":
                    usersComicsTMP = sorted(usersComicsTMP, key=lambda x: x["issueNumber"], reverse=True)
            except:
                print("No orderByIssueNumber arg")
            
            try:
                if args["orderByTitle"] == "asc":
                    usersComicsTMP = sorted(usersComicsTMP, key=lambda x: x["title"])

                if args["orderByTitle"] == "desc":
                    usersComicsTMP = sorted(usersComicsTMP, key=lambda x: x["title"], reverse=True)
            except:
                print("No orderByTitle arg")
                        
        return found, usersComicsTMP

    @staticmethod
    def isUserLoggedIn(auth, args):
        headers = {"Authorization": auth}
        response = requests.request("GET", api.USERS_ENDPOINT, headers=headers)
        if (response.status_code == 200):
            responseData = response.json()
            return True, responseData
        else:
            responseData = response.json()
            return False, make_response(responseData, response.status_code)


    @staticmethod
    def createDbConection():
        client = MongoClient(config.URI, tlsCAFile=certifi.where())
        db = client.test
        users = db.usersComics
        return users
