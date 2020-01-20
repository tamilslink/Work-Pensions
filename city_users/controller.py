from flask_restful import Resource
from flask_restful import request
import geopy.distance
from geopy.geocoders import Nominatim
import logging
import requests
import math


def get_users(user_limit):
    users = requests.get("https://bpdts-test-app.herokuapp.com/users").json()
    return users[0:int(user_limit)]


def get_city_geo_coordinate(city_name):
    geolocator = Nominatim(user_agent="Geo_App")
    location = geolocator.geocode(city_name)

    return (location.latitude, location.longitude)


def get_users_by_geo_location(users, city_name):
    geolocator = Nominatim(user_agent="app")
    city_coordinate = get_city_geo_coordinate(city_name)
    results = []
    for user in users:
        latitude = user['latitude']
        longitude = user['longitude']
        coordinate = (latitude, longitude)
        try:
            distance_from_city = geopy.distance.vincenty(
                city_coordinate, coordinate).miles
        except Exception as e:
            distance_from_city = math.inf
            logging.error("Distance calculation failed for the coordinate {} of user {}. {}".format(coordinate, user, e))
        try:
            geo_location_string = str(latitude) + "," + str(longitude)
            location = geolocator.reverse(geo_location_string)
            address = location.address
            user["location_address"] = address
        except Exception as e:
            address = "ADDRESS_NOT_FOUND"
            logging.error("Get Address process is failed for the coordinate {} of user {}. {}".format(coordinate, user, e))
        city = ", " + city_name        
        if(city in address and "United Kingdom" in address):
            results.append(user)
        elif(distance_from_city <= 50):
            results.append(user)
    return results


class CityUsers(Resource):
    def get(self, city_name):
        user_limit = request.args.get('user_limit', 1000)
        return get_users_by_geo_location(get_users(user_limit), city_name)
