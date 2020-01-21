from django.conf import settings
from api.serializers import *
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from django.db.models import Q
from api.views.follow import get_distance


class Search(APIView):
    def get(self, request, format=None):
        page = request.GET.get('page', 1)
        search_word = request.GET.get('keyword')

        try:

            # All related User Informations

            start = (int(page) - 1) * settings.REQUEST_PER_PAGE
            number_of_users = Profile.objects.filter(username__icontains=search_word).count()

            users = Profile.objects.filter(Q(username__icontains=search_word) |
                                           Q(company__icontains=search_word) |
                                           Q(industry__icontains=search_word)
                                           )[
                    start:start + settings.REQUEST_PER_PAGE]


            user_data = []
            BASE_URL = request.build_absolute_uri('/')
            for row in users:
                temporary = {}
                temporary["id"] = row.user.id
                temporary["username"] = row.username
                temporary["email"] = row.user.username
                temporary["company"] = row.company
                temporary["industry"] = row.industry
                # temporary["profile_image"] = BASE_URL + 'media/profile-picture/' + row.profile_image
                temporary["profile_image"] = "https://s3.amazonaws.com/networkplusapp/"+ row.profile_image

                user_data.append(temporary)

            resdata = {"message": "", "status": "success", "data":
                {
                    "user": {
                        "results": user_data

                    },

                    "total_count": number_of_users,
                    "page": page
                }
                       }

            return HttpResponse(json.dumps(resdata), content_type="application/json")

        except Exception as e:
            resdata = {"message": "IntegrityError Error", "status": "exception"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


class SearchInGetNearBy(APIView):
    def get(self, request, format=None):

        session = request.GET.get('session')
        IsLoggedIn = SessionList.objects.filter(session=session).first()
        req_user = User.objects.get(id=IsLoggedIn.user_id)
        if IsLoggedIn is not None:

            try:

                page = request.GET.get('page', 1)
                search_word = request.GET.get('keyword')

                start = (int(page) - 1) * settings.REQUEST_PER_PAGE


                # start: geting nearby
                total = Profile.objects.filter(Q(username__icontains=search_word) |
                                           Q(company__icontains=search_word) |
                                           Q(industry__icontains=search_word)
                                           ).exclude(user=req_user).count()
                profile_infos = Profile.objects.filter(Q(username__icontains=search_word) |
                                           Q(company__icontains=search_word) |
                                           Q(industry__icontains=search_word)
                                           ).exclude(user=req_user)[
                                start:start + settings.REQUEST_PER_PAGE]
                BASE_URL = request.build_absolute_uri('/')
                data = []

                for user_profile in profile_infos:
                    print(req_user.profile.latitude)
                    print(req_user.profile.longitude)
                    print(user_profile.latitude)
                    print(user_profile.longitude)
                    if req_user.profile.latitude != '' and req_user.profile.longitude != '' and user_profile.latitude != '' and user_profile.longitude != '':
                        distance = get_distance(req_user.profile.latitude, req_user.profile.longitude,
                                                user_profile.latitude,
                                                user_profile.longitude)



                        if distance < 1:
                            temp = {}
                            temp['user_id'] = user_profile.user.id
                            temp['distance_in_km'] = distance
                            temp['email'] = user_profile.user.username
                            temp['username'] = user_profile.username
                            # temp['image'] = BASE_URL + 'media/profile-picture/' + user_profile.profile_image
                            temp['image'] = "https://s3.amazonaws.com/networkplusapp/" + user_profile.profile_image
                            data.append(temp)

                # end: geting nearby

                resdata = {"message": "ok", "status": "success", "data": data, "page": page,"total_count":total}
                return HttpResponse(json.dumps(resdata), content_type="application/json")

            except Exception as e:
                resdata = {"message": "Integrity Error", "status": "exception"}
                return HttpResponse(json.dumps(resdata), content_type="application/json")

        else:
            resdata = {"message": "Not Logged In.", "status": "Failed"}
            return HttpResponse(json.dumps(resdata), content_type="application/json")


