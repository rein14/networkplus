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
from django.db.models import Q
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
from api.views.follow import get_distance


class GetNotification(APIView):
    def get(self, request, format=None):

        try:

            data=[]
            temp_data={}

            page = request.GET.get('page', 1)
            notification_owner_id = request.GET.get('user_id')
            notification_owner_user_info=User.objects.get(id=notification_owner_id)

            start = (int(page) - 1) * settings.REQUEST_PER_PAGE

            total_follower_nof = NotificationsFollower.objects.filter(notification_owner_id=notification_owner_id).count()
            follower_notifications=NotificationsFollower.objects.filter(notification_owner_id=notification_owner_id)\
                .order_by("-added_date")[start:start + settings.REQUEST_PER_PAGE]

            follow_notification_data = []
            for fn in follower_notifications:
                temp_fn = {}
                temp_fn["user_id"] = fn.user_id
                temp_fn["notification_owner"] = fn.notification_owner_id
                temp_fn["notification_type"] = fn.notification_type
                temp_fn["is_notified"] = fn.is_notified
                temp_fn["added_date"] =str(fn.added_date )
                follow_notification_data.append(temp_fn)
                update = NotificationsFollower.objects.filter(id=fn.id).update(is_notified=True)
            temp_data["follow_notifications"] = follow_notification_data


            #start: follow request
            #deleting in_active followlog
            deleting = FollowLog.objects.filter(~Q(status=0,notification_owner_id=notification_owner_id)).delete()
            total_follow_logs=FollowLog.objects.filter(notification_owner_id=notification_owner_id).count()
            follow_logs=FollowLog.objects.filter(notification_owner_id=notification_owner_id)\
                            .order_by("-added_date")[start:start + settings.REQUEST_PER_PAGE]
            follow_request_data = []
            for fl in follow_logs:
                temp_fl = {}
                temp_fl["user_id"] = fl.user_id
                temp_fl["notification_owner"] = fl.notification_owner_id
                temp_fl["is_notified"] = fl.is_notified
                temp_fl["added_date"] = str(fl.added_date )
                follow_request_data.append(temp_fl)
                update = FollowLog.objects.filter(id=fl.id).update(is_notified=True)

            temp_data["follow_request_notifications"] = follow_request_data


            #end: follow request


            #start: geting nearby

            following_ids = Followers.objects.filter(follower_id=notification_owner_id).order_by("-added_date").all() \
                .values_list('following_id', flat=True)


            number_of_following = User.objects.filter(id__in=following_ids).count()
            following_user_infos = User.objects.filter(id__in=following_ids)[start:start + settings.REQUEST_PER_PAGE]

            BASE_URL = request.build_absolute_uri('/')
            following_data = []

            for following_user in following_user_infos:
                if notification_owner_user_info.profile.latitude != '' and notification_owner_user_info.profile.longitude != '' and following_user.profile.latitude != '' and following_user.profile.longitude != '':
                    distance=get_distance(notification_owner_user_info.profile.latitude, notification_owner_user_info.profile.longitude, following_user.profile.latitude,
                                          following_user.profile.longitude)


                    if distance<1:
                        temp_following={}
                        temp_following['follower_id'] = following_user.id
                        temp_following['distance_in_km'] = distance
                        temp_following['follower_email'] = following_user.username
                        temp_following['follower_username'] = following_user.profile.username
                        temp_following['following_user_image'] = "https://s3.amazonaws.com/networkplusapp/" + following_user.profile.profile_image
                        following_data.append(temp_following)
            temp_data["is_nearby"] = following_data

            # end: geting nearby


            # start: geting notification profile change

            total_profile_nof = NotificationsProfile.objects.filter(notification_owner_id=notification_owner_id).count()
            profile_notifications = NotificationsProfile.objects.filter(notification_owner_id=notification_owner_id) \
                                         .order_by("-added_date")[start:start + settings.REQUEST_PER_PAGE]

            profile_notification_data = []
            for pn in profile_notifications:
                temp_pn = {}
                temp_pn["user_id"] = pn.user_id
                temp_pn["notification_owner"] = pn.notification_owner_id
                temp_pn["notification_type"] = pn.notification_type
                temp_pn["is_notified"] = pn.is_notified
                temp_pn["added_date"] = str(pn.added_date )
                profile_notification_data.append(temp_pn)
                update = NotificationsProfile.objects.filter(id=pn.id).update(is_notified=True)
            temp_data["change_profile_data"] = profile_notification_data


            # end: geting notification profile change


            data.append(temp_data)

            resdata = {"message": "ok", "status": "success","total_count":total_follower_nof,"page":page,"data":data}
            return HttpResponse(json.dumps(resdata), content_type="application/json")

        except Exception as e:
            resdata = {"message": "Integrity Error", "status": "exception"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


class GetNearBy(APIView):
    def get(self, request, format=None):

        try:

            data=[]
            temp_data={}

            page = request.GET.get('page', 1)
            notification_owner_id = request.GET.get('user_id')
            notification_owner_user_info=User.objects.get(id=notification_owner_id)

            start = (int(page) - 1) * settings.REQUEST_PER_PAGE

            #start: geting nearby

            following_ids = Followers.objects.filter(follower_id=notification_owner_id).order_by("-added_date").all() \
                .values_list('following_id', flat=True)


            number_of_following = User.objects.filter(id__in=following_ids).count()
            following_user_infos = User.objects.filter(id__in=following_ids).all()

            BASE_URL = request.build_absolute_uri('/')
            following_data = []

            for following_user in following_user_infos:
                if notification_owner_user_info.profile.latitude != '' and notification_owner_user_info.profile.longitude != '' and following_user.profile.latitude != '' and following_user.profile.longitude != '':
                    distance=get_distance(notification_owner_user_info.profile.latitude, notification_owner_user_info.profile.longitude, following_user.profile.latitude,
                                          following_user.profile.longitude)


                    if distance<1:
                        temp_following={}
                        temp_following['follower_id'] = following_user.id
                        temp_following['distance_in_km'] = distance
                        temp_following['follower_email'] = following_user.username
                        temp_following['follower_username'] = following_user.profile.username
                        # temp_following['following_user_image'] = BASE_URL + 'media/profile-picture/' + following_user.profile.profile_image
                        temp_following['following_user_image'] = "https://s3.amazonaws.com/networkplusapp/" + following_user.profile.profile_image
                        following_data.append(temp_following)
            temp_data["is_nearby"] = following_data

            # end: geting nearby



            data.append(temp_data)

            resdata = {"message": "ok", "status": "success","data":data}
            return HttpResponse(json.dumps(resdata), content_type="application/json")

        except Exception as e:
            resdata = {"message": "Integrity Error", "status": "exception"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


