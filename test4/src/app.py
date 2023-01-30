from flask import Flask, request
from constants import config
from services import apiServices


app = Flask(__name__)
layawayApiService = apiServices.LayawayApiService()


@app.route('/getLayawayList', methods=['get'])
def getLayawayList():
    auth = ""
    args = request.args
    try:
        auth = request.headers['Authorization']
    except:
        print("log")
    return layawayApiService.getLayawayList(auth, args)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
