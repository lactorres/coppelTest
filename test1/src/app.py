from flask import Flask
from constants import config
from services import apiServices
from constants import general

app = Flask (__name__)
marvelApiService = apiServices.MarvelApiService()

@app.route('/searchComics', methods=['get'])
def searchAllCharacters():
    return marvelApiService.searchCharacters(general.EMPTY_STRING)

@app.route('/searchComics/<searchTerm>', methods=['get'])
def searchComicsAndCharacters(searchTerm):
    return marvelApiService.searchComicsAndCharacters(searchTerm)

@app.route('/searchComics/byComicName/<comic>', methods=['get'])
def searchComics(comic):
    return marvelApiService.searchComics(comic)

@app.route('/searchComics/byCharacterName/<character>', methods=['get'])
def searchCharacters(character):
    return marvelApiService.searchCharacters(character)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)