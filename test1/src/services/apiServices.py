from flask import make_response, jsonify
import requests
import hashlib
import json
from jsonmerge import merge
from constants import general, api


class MarvelApiService():

    def searchCharacters(self, searchTerm, args):
        searchParam = general.EMPTY_STRING
        if (searchTerm != general.EMPTY_STRING):
            searchParam = api.CHARACTERS_PARAM + searchTerm
        response = self.requestApi(api.CHARACTERS, searchParam, args)
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
            return make_response(jsonify({"error": "There was an error with Marvel Services, try again later", "description": response.json()}), 400)

        return jsonify(characters=characters)

    def searchComics(self, searchTerm, args):
        searchParam = general.EMPTY_STRING
        if (searchTerm != general.EMPTY_STRING):
            searchParam = api.COMICS_PARAM + searchTerm
        response = self.requestApi(api.COMICS, searchParam + api.DEFAULT_PARAMS, args)
        if response.status_code == 200:
            comicsResult = []
            responseData = response.json()
            responseResults = responseData['data']['results']
            
            for comics in responseResults:
                onSaleDate = [date for date in comics['dates'] if date["type"] == "onsaleDate"]
                itemComic = {
                    'id': comics['id'],
                    'title': comics['title'],
                    'image':comics['thumbnail']['path'] +"." + comics['thumbnail']['extension'],
                    'onSaleDate':onSaleDate[0]["date"],
                    "issueNumber": comics['issueNumber']
                }
                comicsResult.append(itemComic)
            
        else:
            return make_response(jsonify({"error": "There was an error with Marvel Services, try again later", "description": response.json()}), 400)

        return jsonify({"comics" : comicsResult})

    def searchComicsAndCharacters(self, searchTerm, args):
        characters = self.searchCharacters(searchTerm, args)
        comics = self.searchComics(searchTerm, args)
        charactersJson = json.loads(characters.data)
        comicsJson =  json.loads(comics.data)
        response = merge(charactersJson, comicsJson)
        return jsonify(response)

    def requestApi(self, searchType, searchParam, args):
        hash = self.calculateHash()
        url = api.API_ENDPOINT + searchType + "?apikey=" + \
            api.PUBLIC_KEY + "&hash=" + hash + "&ts=test" + searchParam
        response = requests.request("GET", url, params=args)
        return response

    @staticmethod
    def calculateHash():
        personalKey = "test"+api.PRIVATE_KEY+api.PUBLIC_KEY
        hashKey = personalKey.encode('utf-8')
        print(hashKey)
        result = hashlib.md5(hashKey)
        return result.hexdigest()
