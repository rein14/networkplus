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


