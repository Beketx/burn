import logging

from django.core.paginator import InvalidPage
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated,\
                                       IsAuthenticatedOrReadOnly, \
                                       AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from developer.models import Stacks, Skills, Developer, Favorites
from developer.serializers import DevelopersSerializer, FavoritesSerializer
from devutils import serializers
from userauth.models import User
from utils.developer_pagination.pagination import DeveloperPagination

logger = logging.getLogger(__name__)
class StacksView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.StacksSerializer
    queryset = Stacks.objects.all()
    permission_class = [AllowAny, ]

class SkillsView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SkillsSerializer
    queryset = Skills.objects.all()
    permission_class = [AllowAny, ]

class AddFavorite(APIView, DeveloperPagination):
    """
    {
    dev_id:123,
    isFavorite:True,False
    }
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            users = request.user
            favs = Favorites.objects.get_favorites(users)
            data = []
            for fav in favs:
                data.append(fav.developer)
            favs = self.paginate_queryset(data, request, view=self)
            serializer = DevelopersSerializer(favs, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        except:
            return self.paginate_queryset(data, request, view=self)

    def post(self, request):
        try:
            data = request.data
            users = self.request.user
            dev_id = data["developer_id"]
            isFav = data["is_favorite"]
            if Developer.objects.get(id=dev_id):
                dev = Developer.objects.get(id=dev_id)
                logger.debug('developer id exist')
            if isFav is True:
                logger.debug('qqqqTrue')
                if Favorites.objects.filter(developer=dev, user=users).exists() == False:
                    logger.debug('if not isFavTrue')
                    Favorites.objects.create(developer=dev, favorite_bool=isFav, user=users)
            else:
                if Favorites.objects.filter(developer=dev, user=users).exists():
                    logger.debug('if not isFavFalse')
                    Favorites.objects.get(developer=dev, user=users).delete()
            logger.debug('nowhere')
            res = {
                'status': True,
                'detail': 'Favorite action accepted'
            }
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            logger.debug('in except')
            res = {
                'status': False,
                'detail': str(e)
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)

# class MyFavorites(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated, ]
#     queryset = Favorites.objects.all()
#     def list(self, request):
#         queryset = Favorites.objects.filter(user=self.request.user)
#         serializer_class = DevelopersSerializer(queryset, many=True)
#         return Response(serializer_class.data)