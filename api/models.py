from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.TextField(default="")
    username = models.CharField(max_length=150, default="")
    security_code = models.CharField(max_length=255, default="")
    company = models.CharField(max_length=150, default="")
    position = models.CharField(max_length=100, default="")
    industry = models.CharField(max_length=100, default="")
    state_or_country = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    website = models.CharField(max_length=100, default="")
    address = models.TextField(default="")
    skype_id = models.CharField(max_length=150, default="")
    twitter_id = models.CharField(max_length=150, default="")
    facebook_id = models.CharField(max_length=150, default="")
    latitude = models.CharField(max_length=100, default="")
    longitude = models.CharField(max_length=100, default="")
    isVarified=models.BooleanField(default=False)
    added_date=models.DateTimeField(editable=False, auto_now_add=True)
    modified_date=models.DateTimeField(editable=True, auto_now_add=True)


class SessionList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    session = models.TextField(default="")
    added_date = models.DateTimeField(
        default=timezone.now)
    expire_date = models.DateTimeField(default=timezone.now)


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester_user')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_user')
    added_date = models.DateTimeField(editable=False, auto_now_add=True)
    modified_date = models.DateTimeField(editable=True, auto_now_add=True)
    is_active = models.BooleanField(default=True)


class FollowLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')
    notification_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    status = models.IntegerField(default=0)  #0= requested,1= accepted,2=rejected
    added_date = models.DateTimeField(editable=False, auto_now_add=True)
    is_notified = models.BooleanField(default=False)


class NotificationsFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
    notification_owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following_owner')
    notification_type = models.CharField("follow", max_length=100)
    added_date = models.DateTimeField(editable=False, auto_now_add=True)
    is_notified = models.BooleanField(default=False)


class NotificationsProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='profile_owner')
    notification_owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notification_profile_owner')
    notification_type = models.CharField(max_length=100)
    added_date = models.DateTimeField(editable=False, auto_now_add=True)
    is_notified = models.BooleanField(default=False)