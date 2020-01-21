from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [

    url(r'^registration/$', views.Registration.as_view(), name="registration"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^forget-password/$', views.ForgetPassword.as_view(), name="forget_password"),
    url(r'^reset-password/$', views.ResetPassword.as_view(), name="reset_password"),
    url(r'^logout-user/$', views.logout_user, name="logout_user"),



    url(r'^user/update-profile/$', views.UpdateUserInfo.as_view(), name="update_profile"),
    url(r'^user/(?P<user_id>.*)/$', views.SingleUser.as_view(), name="single_user"),
    url(r'^get-me/$', views.Get_Me.as_view(), name="get_me"),

    url(r'^request/follow/$', views.Request_Follow.as_view(), name="request_follow"),
    url(r'^accept-follow/$', views.AcceptFollow.as_view(), name="accept_follow"),
    url(r'^get-follow-list/$', views.GetFollowList.as_view(), name="get_follow_list"),

    url(r'^get-notifications/$', views.GetNotification.as_view(), name="get_notifications"),
    url(r'^get-nearby/$', views.GetNearBy.as_view(), name="get_nearby"),
    url(r'^search-nearby/$', views.SearchInGetNearBy.as_view(), name="search_nearby"),
    url(r'^search/$', views.Search.as_view(), name="search"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()