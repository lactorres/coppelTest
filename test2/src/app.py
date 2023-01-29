from flask import Flask, request
from flask_jwt_extended import JWTManager
import datetime
import secrets
from constants import config
from services import apiServices
from constants import general


app = Flask (__name__)
jwt = JWTManager(app) 
app.config['JWT_SECRET_KEY'] = "938tyh39rv9hcv7893hc4hc8g47"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) 
usersApiService = apiServices.UsersApiService()

@app.route('/users/register', methods=['post'])
def registerUser():
    payload = request.get_json()
    return usersApiService.registerUser(payload)

@app.route('/users/login', methods=['post'])
def loginUser():
    payload = request.get_json()
    return usersApiService.loginUser(payload)

@app.route('/users', methods=['get'])
def getUser():
    return usersApiService.getUser()

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)