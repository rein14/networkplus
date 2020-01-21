from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from api.models  import *
from api.serializers import *

import smtplib
from email.mime.text import MIMEText
from rest_framework.response import Response
import json
from django.http import HttpResponse,HttpResponseRedirect
import base64
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.core.files.base import ContentFile
import uuid
import time
import datetime
from api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
#from geolocation.main import GoogleMaps
#from geolocation.distance_matrix.client import DistanceMatrixApiClient


class Request_Follow(APIView):
    def post(self, request, format=None):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        session = body.get('session')
        IsLoggedIn = SessionList.objects.filter(session=session).first()
        if IsLoggedIn is not None:

            following_user_id = body.get('following_user_id')

            try:
                #start: checking if already requested
                is_exist = FollowLog.objects.filter(notification_owner_id=following_user_id,
                                                    user_id=IsLoggedIn.user_id).exists()

                if is_exist is not False:
                    resdata = {"message": "Already requested.", "status": "Failed"}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")
                #end: checking if already requested

                log = FollowLog(user_id=IsLoggedIn.user_id,
                                notification_owner_id=following_user_id,
                                status=0
                                )
                log.save()

                resdata = {"message": "Follower request sent", "status": "success"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")
            except Exception as e:
                resdata = {"message": "Integrity Error", "status": "exception"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")

        else:
            resdata = {"message": "Not Logged In.", "status": "Failed"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


class AcceptFollow(APIView):
    def post(self, request, format=None):


        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        session = body.get('session')
        IsLoggedIn = SessionList.objects.filter(session=session).first()
        if IsLoggedIn is not None:

            # if body.get('is_follow')=="1":
            requested_user_id = body.get('user_id')
            status = body.get('status')

            try:

                #start: checking if following reqested
                is_exist=FollowLog.objects.filter(notification_owner_id=IsLoggedIn.user_id,
                                                  user_id=requested_user_id,status=0).exists()
                if is_exist is False:
                    resdata = {"message": "Bad request or Already request applied.", "status": "Failed"}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")

                #end: checking if following reqested

                if status=='1':
                    is_updated = FollowLog.objects.filter(notification_owner_id=IsLoggedIn.user_id,
                                                        user_id=requested_user_id).update(status=1)

                    followers = Followers(follower_id=IsLoggedIn.user_id, following_id=requested_user_id)
                    followers.save()

                    followers = Followers(follower_id=requested_user_id, following_id=IsLoggedIn.user_id)
                    followers.save()


                    notification = NotificationsFollower(user_id=IsLoggedIn.user_id,
                                                     notification_owner_id=requested_user_id,
                                                     notification_type="following request accepted"
                                                     )
                    notification.save()

                    is_update = FollowLog.objects.filter(notification_owner_id=IsLoggedIn.user_id,
                                                         user_id=requested_user_id).update(status=1)

                    resdata = {"message": "Following request accepted", "status": "success"}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")

                if status=='2':

                    is_delete=FollowLog.objects.filter(notification_owner_id=IsLoggedIn.user_id,
                                                  user_id=requested_user_id).delete()
                    resdata = {"message": "Following request rejected", "status": "success"}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")
                else:
                    resdata = {"message": "Bad request.Please set status 1 for accept or 2 for reject.", "status": "Failed"}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")

            except Exception as e:
                resdata = {"message": "Integrity Error", "status": "exception"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")



            # elif body.get('is_follow') == "0":
            #     following_user_id = body.get('following_user_id')
            #
            #     try:
            #         Followers.objects.filter(follower_id=IsLoggedIn.user_id, following_id=following_user_id).all().delete()
            #
            #         resdata = {"message": "Follower Removed", "status": "success"}
            #         return HttpResponse(json.dumps(resdata), content_type="application/json")
            #     except Exception as e:
            #         resdata = {"message": "Integrity Error", "status": "exception"}
            #         return HttpResponse(json.dumps(resdata), content_type="application/json")
            # else:
            #     resdata = {"message": "Bad Request.", "status": "Failed"}
            #     return HttpResponse(json.dumps(resdata), content_type="application/json")

        else:
            resdata = {"message": "Not Logged In.", "status": "Failed"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


class GetFollowList(APIView):
    def get(self, request, format=None):

        session = request.GET.get('session',None)
        user_id = request.GET.get('user_id',None)
        call_type = request.GET.get('call_type',None)
        page = request.GET.get('page',1)

        try:

            if call_type=="follower":
                start = (int(page) - 1) * settings.REQUEST_PER_PAGE


                following_user=User.objects.get(id=user_id)
                if following_user is None:
                    resdata = {
                        "message": "User not found",
                        "status": "failed"
                    }
                    return HttpResponse(json.dumps(resdata), content_type="application/json")


                # searched user (given user_id  ) location
                try:
                    latitude1=float(following_user.profile.latitude)
                    longitude1=float(following_user.profile.longitude)
                except:
                    latitude1=''
                    longitude1=''

                follower_ids=Followers.objects.filter(following_id=user_id).order_by("-added_date").all()\
                    .values_list('follower_id',flat=True)

                number_of_follower = len(follower_ids.distinct())

                follower_user_infos=User.objects.filter(id__in=follower_ids)[
                            start:start + settings.REQUEST_PER_PAGE]


                BASE_URL = request.build_absolute_uri('/')
                follower_data=[]
                for follower_user in follower_user_infos:

                    temp_follower={}

                    temp_follower['follower_id']=follower_user.id
                    temp_follower['follower_email']=follower_user.username
                    temp_follower['follower_username']=follower_user.profile.username

                    if latitude1!='' and longitude1!='' and follower_user.profile.latitude!='' and follower_user.profile.longitude!='':

                        temp_follower['follower_distance_in_km']=get_distance(latitude1,longitude1,float(follower_user.profile.latitude),float(follower_user.profile.longitude))

                    else:
                        temp_follower['follower_distance_in_km'] ='Information Not Found'




                    temp_follower['follower_image']= "https://s3.amazonaws.com/networkplusapp/" +follower_user.profile.profile_image

                    fol=Followers.objects.filter(follower_id=follower_user.id,following_id=user_id).first()

                    temp_follower['added_date']=fol.added_date.strftime("%Y-%m-%d %H:%M:%S")

                    follower_data.append(temp_follower)

                resdata = {
                           "message": "ok",
                           "status": "success",
                           "data": follower_data,
                           "total_count": number_of_follower,
                           "page": page,
                           }
                return HttpResponse(json.dumps(resdata), content_type="application/json")

            if call_type == "following":

                start = (int(page) - 1) * settings.REQUEST_PER_PAGE

                follower_user = User.objects.get(id=user_id)
                if follower_user is None:
                    resdata = {
                        "message": "User not found",
                        "status": "failed"
                    }
                    return HttpResponse(json.dumps(resdata), content_type="application/json")

                # searched user (given user_id  ) location

                latitude1 = float(follower_user.profile.latitude)
                longitude1 = float(follower_user.profile.longitude)

                following_ids = Followers.objects.filter(follower_id=user_id).order_by("-added_date").all() \
                    .values_list('following_id', flat=True)

                number_of_following = User.objects.filter(id__in=following_ids).count()
                following_user_infos = User.objects.filter(id__in=following_ids)[start:start + settings.REQUEST_PER_PAGE]


                BASE_URL = request.build_absolute_uri('/')
                following_data = []
                for following_user in following_user_infos:
                    temp_follower = {}

                    temp_follower['following_user_id'] = following_user.id
                    temp_follower['following_user_email'] = following_user.username
                    # temp_follower['following_user_image'] = BASE_URL + 'media/profile-picture/' + following_user.profile.profile_image
                    temp_follower['following_user_image'] = "https://s3.amazonaws.com/networkplusapp/"+ following_user.profile.profile_image
                    temp_follower['following_user_username'] = following_user.profile.username
                    try:
                        temp_follower['following_user_distance_in_km'] = get_distance(latitude1, longitude1, float(
                            following_user.profile.latitude), float(following_user.profile.longitude))

                    except:
                        temp_follower['following_user_distance_in_km'] ='Information Not Found'
                    # temp_follower['following_user_distance_in_km'] = get_distance(latitude1,longitude1,float(following_user.profile.latitude),float(following_user.profile.longitude))

                    fol = Followers.objects.filter(following_id=following_user.id, follower_id=user_id).first()

                    temp_follower['added_date'] = fol.added_date.strftime("%Y-%m-%d %H:%M:%S")

                    following_data.append(temp_follower)

                resdata = {"message": "ok",
                           "status": "success",
                           "data": following_data,
                           "total_count": number_of_following,
                           "page": page,
                           }
                return HttpResponse(json.dumps(resdata), content_type="application/json")
            else:
                resdata = {"message": "Bad Request", "status": "failed"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")


        except Exception as e:
            resdata = {"message": "Integrity Error", "status": "exception"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


from math import sin, cos, sqrt, atan2, radians
def get_distance(latitude1,longitude1,latitude2,longitude2):


    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(latitude1))
    lon1 = radians(float(longitude1))
    lat2 = radians(float(latitude2))
    lon2 = radians(float(longitude2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return float(distance)

#def get_locations(latitude,longitude):
#    google_maps = GoogleMaps(api_key=settings.GOOGLE_API_KEYS)
#   my_location = google_maps.search(lat=latitude, lng=longitude).first()

#   return my_location