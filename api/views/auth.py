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
# import boto3
from .system_email import *


class Registration(APIView):

    def post(self, request, format=None):
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        isExist=User.objects.filter(username=body.get("email")).first()
        if isExist:
            response = {
                "data": {
                    "email": ["This email already exists."]

                },
                "message": "Validation error",
                "status": "error"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if body.get("profile_image") !='':
            if not body["profile_image"].startswith('data:image/'):
                response = {
                    "data": {
                        "profile_image": ["Unsupport Image Format."]

                        },
                    "message": "Validation error",
                    "status": "error"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


        user_serializer = UserSerializer(data=body)
        if user_serializer.is_valid():
            user_serializer.save()

            # print(user_serializer.data)

            # try:

            profile = self.create_profile(body.get("profile_image"),user_serializer.data["pk"], body["username"])

            if profile:
                message = '<p>Dear Mr. ' + body["username"] + ',</p><p>You have successfully registered.</p><p>Thanks,</p><p>Team NetworkPlus</p>'


                Subject = "Network Plus: Registration"

                # send email to registered user
                parade_email = ParadeEmail()

                email_send_confirmation = parade_email.send_email(
                                                            Subject,
                                                            body["email"],
                                                             'no-reply@triumapp.com',
                                                            message
                                                        )

            else:
                current_user_instance = User.objects.get(id=user_serializer.data["pk"])
                current_user_instance.delete()

                response = {
                    "data": {
                        "message": "Somethings went wrong . User Not Created."

                    },
                    "message": "Validation error",
                    "status": "error"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


            # except:
            #     current_user_instance = User.objects.get(id=user_serializer.data["pk"])
            #     current_user_instance.delete()
            #
            #     response = {
            #         "data": {
            #             "errors": ["Bad request."]
            #
            #         },
            #         "message": "Validation error",
            #         "status": "error"
            #     }
            #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # user authentication and session generate
            user = authenticate(username=body.get("email"), password=body.get("password"))

            #new session
            session_key=str(uuid.uuid4())
            expire_date = datetime.datetime.now() + datetime.timedelta(settings.EXPIRE_DAYS)

            session = SessionList(user_id=user.id, session= session_key, expire_date=expire_date)
            session.save()

            if user is not None:
                # get user data
                BASE_URL = request.build_absolute_uri('/')

                response = {
                    "data": {
                        "email": body.get("email"),
                        "username": profile.username,
                        "id": user_serializer.data["pk"],
                        "profile_image": "https://s3.amazonaws.com/networkplusapp/"+profile.profile_image,
                        "session":session_key
                    },
                    "message": "Registration Completed.",
                    "status": "success"
                }

            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "data": user_serializer.errors,
            "message": "Validation error",
            "status": "error"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



    def create_profile(self,profile_image,user_id, username):
        if profile_image !='':
            format, imgstr = profile_image.split(';base64,')
            ext = format.split('/')[-1]

            filename = username.replace(" ", "_") + "_" + str(user_id) + "." + ext
            filepath = settings.MEDIA_ROOT + "/profile-picture/" + filename


            fw = open(filepath, "wb")
            fw.write(base64.b64decode(imgstr))
            fw.close()
        else:
            filename='Nophoto.jpg'
            filepath = settings.MEDIA_ROOT + "/profile-picture/" + filename

        s3_client = boto3.client(
            's3',
            aws_access_key_id="AKIAJLKHMQCO3A4YII6Q",
            aws_secret_access_key="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"
        )
        s3_client.upload_file(filepath, "networkplusapp", filename,ExtraArgs={'ACL':'public-read-write',})

        security_code = str(uuid.uuid4())
        profile = Profile(user_id=user_id, username=username, profile_image=filename, security_code=security_code)
        profile.save()

        # url = s3_client.generate_presigned_url('get_object',
        #                                 Params={
        #                                     'Bucket': 'networkplusapp',
        #                                     'Key': filename,
        #                                 },
        #                                 ExpiresIn=3600)
        # print(url)


        return profile


class Login(APIView):

    def post(self, request, format=None):



        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        password = body.get("password")
        email = body.get('email')


        user_request = User.objects.filter(username=email).first()


        if user_request is None:
            response = {
                "data": {
                    "error_message": ["User not found."]

                },
                "message": "Validation error",
                "status": "error"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user_request.username, password=password)

        if user is None:
            response = {
                "data": {
                    "error_message": ["Invalid username/password"]
                },
                "message": "Validation error",
                "status": "error"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


        session_key = str(uuid.uuid4())

        expire_date = datetime.datetime.now() + datetime.timedelta(days=settings.EXPIRE_DAYS)

        session = SessionList(user_id=user.id, session=session_key, expire_date=expire_date)
        session.save()

        if user is not None:
            # get user data
            BASE_URL = request.build_absolute_uri('/')

            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,

                # 'profile_image': BASE_URL + 'media/profile-picture/' + user.profile.profile_image,
                'profile_image': "https://s3.amazonaws.com/networkplusapp/" + user.profile.profile_image,
                'session': session_key
            }

            response = {
                "data": data,
                "message": "Valid Login",
                "status": "success"
            }

            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:

            response = {

                "message": "Invalid Request",
                "status": "error"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def logout_user(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    session = body.get('session')
    IsLoggedIn = SessionList.objects.filter(session=session).first()

    if IsLoggedIn is not None:
        SessionList.objects.filter(session=session).delete()
        resdata = {"message": "Logged Out", "status": "success"}
        return HttpResponse(json.dumps(resdata), content_type="application/json")
    else:
        resdata = {"message": "Access Denied", "status": "error"}
        return HttpResponse(json.dumps(resdata), content_type="application/json")


class ForgetPassword(APIView):

    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        email = body.get("email")
        user = User.objects.filter(username=email).first()
        profile = Profile.objects.filter(user_id=user.id).first()

        if user is not None:
            security_code = str(uuid.uuid4())
            profile_update = Profile.objects.filter(user_id=user.id).update(security_code=security_code)

            # target_url = "http://biz.triumapp.com/#/password-reset/?security_code=" + security_code

            target_url = settings.APP_URL + "/base/reset-password/" + security_code + "/"

            message = '<p>Dear Mr. ' + profile.username + ',</p><p>You have requested to change your Password. Please <a href="' + target_url + '">click here</a> to reset.</p><p>Thanks,</p><p>Team NetworkPlus</p>'

            Subject = "NetworkPlus: Forget Password"

            # send email to registered user
            parade_email = ParadeEmail()

            email_send_confirmation = parade_email.send_email(
                Subject,
                email,
                'no-reply@triumapp.com',
                message
            )



            response = {
                "data": {
                    'security_code': security_code,
                    'email': email,
                },
                "message": "ok.",
                "status": "sucess"
            }
            return Response(response, status=status.HTTP_200_OK)


        else:

            response = {
                "data": {},
                "message": "Email Doesn't Exists.",
                "status": "error"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):

    def post(self, request, format=None):
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)

        security_code=request.GET.get("security_code")
        new_password=request.GET.get("new_password")

        try:
            profile = Profile.objects.filter(security_code=security_code).first()
            user = User.objects.filter(id=profile.user_id).first()
            user.set_password(raw_password=new_password)

            user.save()
            profile_update = Profile.objects.filter(security_code=security_code).update(security_code='')

            response = {
                "data": {},
                "message": "Password reset Successful.",
                "status": "success"
            }
            return Response(response, status=status.HTTP_200_OK)


        except:

            response = {
                "data": {},
                "message": "Bad request.",
                "status": "error"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

