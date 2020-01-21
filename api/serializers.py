from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # username = serializers.CharField(
    #     required=True,
    #     # validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    password = serializers.CharField(required=True,
                                     # min_length=5,
                                     # max_length=20,
                                     # trim_whitespace=True,
                                     # style={'input_type': 'password'},
                                     write_only=True)
    class Meta:
        model = User
        fields = ('pk','password','email')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["email"])

        user.set_password(raw_password=validated_data["password"])

        user.is_staff = True
        user.is_superuser = False
        user.is_active = True
        user.save()

        return user