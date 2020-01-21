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
# import  boto3

class SingleUser(APIView,):
    
    def get(self, request,user_id, format=None):

        user = User.objects.filter(id=user_id).first()
        session = request.GET.get('session',None)
        IsLoggedIn = SessionList.objects.filter(session=session).first()
    
        if IsLoggedIn is not None:
            try:
    
                if user is not None:
                    BASE_URL = request.build_absolute_uri('/')
                    data = []
                    profile = Profile.objects.get(user_id=user.id)

                    temp = {}
                    temp["id"] = user.id
                    temp["username"] = profile.username
                    temp["email"] = user.username
                    temp["phone"] = profile.phone
                    temp["website"] = profile.website
                    temp["address"] = profile.address
                    temp["twitter_id"] = profile.twitter_id
                    temp["company"] = profile.company
                    temp["industry"] = profile.industry
                    temp["position"] = profile.position
                    temp["state_or_country"] = profile.state_or_country
                    temp["skype_id"] = profile.skype_id
                    temp["facebook_id"] = profile.facebook_id
                    temp["latitude"] = profile.latitude
                    temp["longitude"] = profile.longitude
    
                    if profile.profile_image!='':
                        # temp["profile_image"] = BASE_URL + 'media/profile-picture/' + profile.profile_image
                        temp["profile_image"] = "https://s3.amazonaws.com/networkplusapp/" + profile.profile_image
                    else:
                        temp["profile_image"]=None

                    #finding is_follow

                    is_follow=Followers.objects.filter(follower_id=IsLoggedIn.user_id,following_id=user_id).exists()
                    temp["is_follow"] = is_follow

                    data.append(temp)
    
                    resdata = {"message": "okay", "status": "success", "data": data}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")
                else:
    
                    message = "User doesn't exist."
                    resdata = {"message": message, "status_code": "404", "status": "failed"}
                    return HttpResponse(json.dumps(resdata), content_type="application/json")
    
            except:
                message = "Bad request."
                resdata = {"message": message, "status_code": "400", "status": "failed"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")
        else:
            resdata = {"message": "You are not authorized to make this request.Please Login First.", "status": "denied", "status_code": "401"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")



class UpdateUserInfo(APIView):
    def post(self, request, format=None):

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        session = body.get('session',None)
        IsLoggedIn = SessionList.objects.filter(session=session).first()

        if IsLoggedIn is not None:
            try:
                user = User.objects.filter(id=IsLoggedIn.user_id).first()
                previous_profile = Profile.objects.filter(user_id=IsLoggedIn.user_id).first()


                username = body.get('username',previous_profile.username)
                company = body.get('company',previous_profile.company)
                industry = body.get('industry',previous_profile.industry)
                position = body.get('position',previous_profile.position)
                state_or_country = body.get('state_or_country',previous_profile.state_or_country)
                phone = body.get('phone',previous_profile.phone)
                website = body.get('website',previous_profile.website)
                address = body.get('address',previous_profile.address)
                skype_id = body.get('skype_id',previous_profile.skype_id)
                twitter_id = body.get('twitter_id',previous_profile.twitter_id)
                facebook_id = body.get('facebook_id',previous_profile.facebook_id)
                latitude = body.get('latitude',previous_profile.latitude)
                longitude = body.get('longitude',previous_profile.longitude)
                base64_image = body.get('profile_image', previous_profile.profile_image)


                #start:sending Notification
                follower_ids = Followers.objects.filter(following_id=IsLoggedIn.user_id).values_list('follower_id',flat=True)

                if username!=previous_profile.username:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="username"
                                                             )
                        notification.save()
                if company!=previous_profile.company:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="company"
                                                             )
                        notification.save()

                if industry!=previous_profile.industry:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="industry"
                                                             )
                        notification.save()

                if position!=previous_profile.position:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="position"
                                                             )
                        notification.save()
                if state_or_country!=previous_profile.state_or_country:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="state_or_country"
                                                             )
                        notification.save()
                if phone!=previous_profile.phone:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="phone number"
                                                             )
                        notification.save()
                if website!=previous_profile.website:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="website"
                                                             )
                        notification.save()
                if address!=previous_profile.address:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="address"
                                                             )
                        notification.save()
                if skype_id!=previous_profile.skype_id:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="skype_id"
                                                             )
                        notification.save()
                if twitter_id!=previous_profile.twitter_id:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="twitter_id"
                                                             )
                        notification.save()
                if facebook_id!=previous_profile.facebook_id:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="facebook_id"
                                                             )
                        notification.save()
                if base64_image!=previous_profile.profile_image:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="profile_image"
                                                             )
                        notification.save()
                if latitude!=previous_profile.latitude or longitude!=previous_profile.longitude:
                    for follower_id in follower_ids:
                        notification = NotificationsProfile(user_id=IsLoggedIn.user_id,
                                                             notification_owner_id=follower_id,
                                                             notification_type="address"
                                                             )
                        notification.save()
                #end:sending Notification






                filename = ''
                if base64_image != previous_profile.profile_image:
                    pass
                else:
                    filename = previous_profile.profile_image

                BASE_URL = request.build_absolute_uri('/')

                # User.objects.filter(id=user.id).update( username=email)
                Profile.objects.filter(user_id=user.id).update(username=username,
                                                               company=company,
                                                               industry=industry,
                                                               position=position,
                                                               state_or_country=state_or_country,
                                                               phone=phone,
                                                               website=website,
                                                               address=address,
                                                               twitter_id=twitter_id,
                                                               skype_id=skype_id,
                                                               facebook_id=facebook_id,
                                                               latitude=latitude,
                                                               longitude=longitude,
                                                               profile_image=filename)





                profile = Profile.objects.get(user_id=user.id)
                user = User.objects.filter(id=user.id).first()



                data = {
                    'id': user.id,
                    'username': profile.username,
                    'email': user.username,
                    'company': profile.company,
                    'industry': profile.industry,
                    'position': profile.position,
                    'state_or_country': profile.state_or_country,
                    'phone': profile.phone,
                    'website': profile.website,
                    'address': profile.address,
                    'twitter_id': profile.twitter_id,
                    'skype_id': profile.skype_id,
                    'facebook_id': profile.facebook_id,
                    'latitude': profile.latitude,
                    'longitude': profile.longitude,
                    # 'profile_image': BASE_URL + 'media/profile-picture/' + profile.profile_image
                    'profile_image': "https://s3.amazonaws.com/networkplusapp/" + profile.profile_image


                }


                resdata = {"status_code": "200", "message": "Succesfully Updated.", "status": "success", "data": data}
                return HttpResponse(json.dumps(resdata), content_type="application/json")
            except:
                message = "Bad Request."
                resdata = {"message": message, "status_code": "400", "status": "failed"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")
        else:
            resdata = {"message": "You are not authorized to make this request.Please Login First.", "status": "denied", "status_code": "401"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


class Get_Me(APIView):

    def get(self, request, format=None):
        session = request.GET.get('session')
        IsLoggedIn = SessionList.objects.filter(session=session).first()

        if IsLoggedIn is not None:


            try:

                user = User.objects.get(id=IsLoggedIn.user_id)
                user_data = []
                BASE_URL = request.build_absolute_uri('/')

                temporary = {}
                temporary["id"] = user.id
                temporary["username"] = user.profile.username
                temporary["email"] = user.username
                temporary["company"] = user.profile.company
                temporary["industry"] = user.profile.industry
                temporary["position"] = user.profile.position
                temporary["state_or_country"] = user.profile.state_or_country
                temporary["phone"] = user.profile.phone
                temporary["website"] = user.profile.website
                temporary["address"] = user.profile.address
                temporary["twitter_id"] = user.profile.twitter_id
                temporary["skype_id"] = user.profile.skype_id
                temporary["facebook_id"] = user.profile.facebook_id
                temporary["latitude"] = user.profile.latitude
                temporary["longitude"] = user.profile.longitude
                # temporary["my_profile_image"] = BASE_URL + 'media/profile-picture/' + user.profile.profile_image
                temporary["my_profile_image"] = "https://s3.amazonaws.com/networkplusapp/"+ user.profile.profile_image

                user_data.append(temporary)


                resdata = {"message": "", "status": "success", "data": user_data  }
                return HttpResponse(json.dumps(resdata), content_type="application/json")

            except Exception as e:
                resdata = {"message": "IntegrityError Error", "status": "exception"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")
        else:
            resdata = {"message": "Not Logged In.", "status": "Failed"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")

