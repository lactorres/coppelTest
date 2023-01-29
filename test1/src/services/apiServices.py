from flask import make_response, jsonify
import requests
import hashlib
from constants import general, api


class MarvelApiService():

    @staticmethod
    def searchCharacters(searchTerm):
        searchParam = general.EMPTY_STRING
        if (searchTerm != general.EMPTY_STRING):
            searchParam = api.CHARACTERS_PARAM + searchTerm
        response = MarvelApiService.requestApi(api.CHARACTERS, searchParam)
        if response.status_code == 200:
            characters = []
            responseData = response.json()
            responseResults = responseData['data']['results']
            for character in responseResults:
                itemCharacter = {
                    'id': character['id'],
                    'name': character['name'],
                    'image': character['thumbnail']['path'] + "." + character['thumbnail']['extension'],
                    'apearances': character['comics']['available']
                }
                characters.append(itemCharacter)
        else:
            return make_response(jsonify({"error": "There was an error with Marvel Services, try again later"}), 400)

        return jsonify(characters=characters)

    @staticmethod
    def searchComics(searchTerm):
        searchParam = general.EMPTY_STRING
        if (searchTerm != general.EMPTY_STRING):
            searchParam = api.COMICS_PARAM + searchTerm
        response = MarvelApiService.requestApi(api.COMICS, searchParam)
        if response.status_code == 200:
            characters = []
            responseData = response.json()
            responseResults = responseData['data']['results']
            
            for comics in responseResults:
                onSaleDate = [date for date in comics['dates'] if date["type"] == "onsaleDate"]
                itemCharacter = {
                    'id': comics['id'],
                    'title': comics['title'],
                    'image':comics['thumbnail']['path'] +"." + comics['thumbnail']['extension'],
                    'onSaleDate':onSaleDate[0]["date"],
                    "issueNumber": comics['issueNumber']
                }
                characters.append(itemCharacter)
            
        else:
            return make_response(jsonify({"error": "There was an error with Marvel Services, try again later"}), 400)

        return jsonify(characters=characters)

    def searchComicsAndCharacters(searchTerm):
        if searchTerm == general.EMPTY_STRING:
            return "nada"
        return searchTerm

    def requestApi(searchType, searchParam):
        hash = MarvelApiService.calculateHash()
        url = api.API_ENDPOINT + searchType + "?apikey=" + \
            api.PUBLIC_KEY + "&hash=" + hash + "&ts=test" + searchParam
        print(url)
        response = requests.request("GET", url)
        return response

    def calculateHash():
        personalKey = "test"+api.PRIVATE_KEY+api.PUBLIC_KEY
        hashKey = personalKey.encode('utf-8')
        print(hashKey)
        result = hashlib.md5(hashKey)
        return result.hexdigest()
