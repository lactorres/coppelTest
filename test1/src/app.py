from flask import Flask, request
from constants import config
from services import apiServices
from constants import general

app = Flask (__name__)
marvelApiService = apiServices.MarvelApiService()

@app.route('/searchComics', methods=['get'])
def searchAllCharacters():
    args = {}
    return marvelApiService.searchCharacters(general.EMPTY_STRING, args)

@app.route('/searchComics/<searchTerm>', methods=['get'])
def searchComicsAndCharacters(searchTerm):
    args = {}
    return marvelApiService.searchComicsAndCharacters(searchTerm, args)

@app.route('/searchComics/byComicName/<comic>', methods=['get'])
def searchComics(comic):
    args = request.args
    return marvelApiService.searchComics(comic, args)

@app.route('/searchComics/byCharacterName/<character>', methods=['get'])
def searchCharacters(character):
    args = request.args
    return marvelApiService.searchCharacters(character, args)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)