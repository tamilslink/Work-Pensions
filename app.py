import os
from flask import Flask
from flask_restful import Resource, Api

from home.controller import Home
from city_users.controller import CityUsers

app = Flask(__name__)
api = Api(app)

api.add_resource(Home, '/')
api.add_resource(CityUsers, '/cities/<string:city_name>/users')

if __name__ == '__main__':
    app.run(
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=os.getenv("APP_PORT", "8080")
    )
