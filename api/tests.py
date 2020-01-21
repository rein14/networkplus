# from django.test import TestCase


# 
# # -- coding: utf-8 --

from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
# 
# address = "New York City Wall Street 12"
# 
google_maps = GoogleMaps(api_key='AIzaSyAWJGw-f9GjEigk2zo1giTR2swsmKbfPPE')
# 
# location = google_maps.search(location=address)  # sends search to Google Maps.
# 
# print(location.all())  # returns all locations.
# 
# my_location = location.first()  # returns only first location.
# 
# print(my_location.city)
# print(my_location.route)
# print(my_location.street_number)
# print(my_location.postal_code)
# 
# for administrative_area in my_location.administrative_area:
# 
#     print(my_location.country)
#     print(my_location.country_shortcut)
# 
#     print(my_location.formatted_address)
# 
#     print(my_location.lat)
#     print(my_location.lng)
# 
#     # reverse geocode
# 
#     lat = 40.7060008
#     lng = -74.0088189
#
#     my_location = google_maps.search(lat=lat, lng=lng).first()

# my_location = google_maps.search(lat=40.7060008, lng=-74.0088189).first()
# my_location2 = google_maps.search(lat=40.7060008, lng=-84.0088189).first()

#
# origins = ['rybnik', 'oslo']
# destinations = ['zagrzeb']
#
# google_maps = GoogleMaps(api_key='AIzaSyAWJGw-f9GjEigk2zo1giTR2swsmKbfPPE')
#
# items = google_maps.distance(origins, destinations).all() # default mode parameter is DistanceMatrixApiClient.MODE_DRIVING.
#
# for item in items:
#
#     print('origin: %s' % item.origin)
#
#     print('destination: %s' % item.destination)
#
#     print('km: %s' % item.distance.kilometers)
#
#     print('m: %s' % item.distance.meters)
#
#     print('miles: %s' % item.distance.miles)
#
#     print('duration: %s' % item.duration) # returns string.
#
#     print('duration datetime: %s' % item.duration.datetime) # returns datetime.
#
#     # you can also get items from duration, returns int() values. print('duration days: %s' % item.duration.days)
#
#     print('duration hours: %s' % item.duration.hours)
#
#     print('duration minutes: %s' % item.duration.minutes)
#
#     print('duration seconds: %s' % item.duration.seconds)

#
# import requests
# import json
#
# send_url = 'http://freegeoip.net/json'
# r = requests.get(send_url)
# j = json.loads(r.text)
# lat = j['latitude']
# lon = j['longitude']
#
# print(lat)
# print(lon)

#
# my_location = google_maps.search(lat=37.3845, lng=-122.0881).first()
#
#
# origins = ['rybnik', 'oslo']
# destinations = ['zagrzeb']
#
# print(my_location)


from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

lat1 = radians(52.2296756)
lon1 = radians(21.0122287)
lat2 = radians(52.406374)
lon2 = radians(16.9251681)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance)
print("Should be:", 278.546, "km")