from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from userauth.models import User, City
from .models import Skills, Stacks, Developer, DeveloperService, Rating, Review, ImageTab
from .serializers import DevelopersSerializer, FullInfoDeveloperSerializer

#birth_date = birth_date.strftime("%d.%m.%Y") if birth_date else None

# class DeveloperProfiles(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):

    # def list(self, request, *args, **kwargs):
    #     queryset = Stacks.objects.all()
    #     for stacks in queryset:
    #
    #     serializer = FullInfoDeveloperSerializer
    #     q
    # def retrieve(self, request, *args, **kwargs):

    # serializer_class = FullInfoDeveloperSerializer
    # rating_count = Rating.objects.all().count()
    # serializer_action_class = {
    #     'list': FullInfoDeveloperSerializer,
    #     'retrieve': DevelopersSerializer
    # }
    # queryset = Developer.objects.filter(stacks_id=1)
    # permission_classes = (AllowAny, )
    # # pagination_class = CustomDeveloeprPagination
    #
    # def get_serializer_class(self):
    #     try:
    #         return self.serializer_action_class[self.action]
    #     except (KeyError, AttributeError):
    #         return super().get_serializer_class()

class DeveloperProfiles(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk):
        try:
            return self.get_object(pk)
        except:
            stacks = Stacks.objects.all()
            developers = []
            data = []
            sum_rate = 0
            count_rate = 0
            for stack in stacks:
                developer = Developer.objects.filter(stacks_id=stack)
                for dev in developer:
                    rating = Rating.objects.filter(developer=dev)
                    for rate in rating:
                        all_rate = (rate.communication + rate.quality + rate.truth_review)/3
                        sum_rate += all_rate
                        count_rate += 1

                    avg_rating = sum_rate/count_rate

                    json_raw = {
                            "name": dev.user.name,
                            "surname": dev.user.surname,
                            "stacks": dev.stacks_id.name,
                            "skills": dev.skills_id.name,
                            "rating": avg_rating,
                            "rating_count": count_rate,
                            "price": dev.dev_service.price
                        }

                    developers.append(json_raw)
                dev_stack = {"{}".format(stack.title): developers}
                data.append(dev_stack)
            result = {"data": data}
            return Response(result)

    def get_object(self, pk):
        try:
            developer = Developer.objects.get(id=pk)
            rating = Rating.objects.filter(developer=developer)
            sum_rate = 0
            sum_communication_rate = 0
            sum_quality_rate = 0
            sum_truth_ratecount_rate = 0
            sum_truth_rate = 0
            count_rate = 0
            for rate in rating:
                all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
                sum_rate += all_rate
                sum_communication_rate += rate.communication
                sum_quality_rate += rate.quality
                sum_truth_rate += rate.truth_review
                count_rate += 1

            avg_rating = sum_rate / count_rate
            avg_communication = sum_communication_rate / count_rate
            avg_quality = sum_quality_rate / count_rate
            avg_truth = sum_truth_rate / count_rate
            json_raw = {
                    "name": developer.user.name,
                    "surname": developer.user.surname,
                    "stacks": developer.stacks_id,
                    "skills": developer.skills_id,
                    "service_title": developer.dev_service.service_title,
                    "service_description": developer.dev_service.service_description,
                    "rating": avg_rating,
                    "communication_rating": avg_communication,
                    "quality_rating": avg_quality,
                    "truth_rating": avg_truth,
                    "rating_count": count_rate,
                    "price": developer.dev_service.price
                }
            result = {"data": json_raw}
            return Response(result)
        except:
            return Response({"1": "One"})


# for rate in rating:
#     all_rate = (rate.communication + rate.quality + rate.truth_review) / 3
#     sum_rate += all_rate
#     sum_communication_rate += rate.communication
#     sum_quality_rate += rate.quality
#     sum_truth_rate += rate.truth_review
#     count_rate += 1
#
# avg_rating = sum_rate / count_rate
# avg_communication = sum_communication_rate / count_rate
# avg_quality = sum_quality_rate / count_rate
# avg_truth = sum_truth_rate / count_rate
# json_raw = {
#     "{}".format(stack.title): {
#         "name": dev.user.name,
#         "surname": dev.user.surname,
#         "stacks": dev.stacks_id,
#         "skills": dev.skills_id,
#         "rating": avg_rating,
#         "communication_rating": avg_communication,
#         "quality_rating": avg_quality,
#         "truth_rating": avg_truth,
#         "rating_count": count_rate,
#         "price":
#     }
"""

from backend.models import Profile
from backend.serializers import ProfileSerializer
from django.http import JsonResponse

from rest_framework import mixins, permissions, generics

class ProfileViewSet(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request): # change this to use the patch mixin
        profile = Profile.objects.filter(user = request.user).first()
        profile.first_name = request.data['first_name']
        profile.last_name = request.data['last_name']
        profile.bio = request.data['bio']
        profile.location = request.data['location']
        profile.save()
        return JsonResponse({"response": "change successful"})
"""