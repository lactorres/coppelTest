from flask import Flask, request
from constants import config
from services import apiServices
from constants import general


app = Flask(__name__)
layawayApiService = apiServices.LayawayApiService()


@app.route('/addToLayaway', methods=['post'])
def addToLayaway():
    payload = {}
    auth = ""
    try:
        auth = request.headers['Authorization']
        payload = request.get_json()
    except:
        print("log")
    return layawayApiService.addToLayaway(payload, auth)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
