import logging

from django.core.paginator import InvalidPage
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated,\
                                       IsAuthenticatedOrReadOnly, \
                                       AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from developer.models import Stacks, Skills, Developer, Favorites
from developer.serializers import DevelopersSerializer, FavoritesSerializer
from devutils import serializers
from userauth.models import User
from utils.developer_pagination.pagination import DeveloperPagination

logger = logging.getLogger(__name__)
@api_view(['GET'])
def stacks_list(request):
    if request.method == 'GET':
        logger.debug('In get')

        favorites = Stacks.objects.all()
        serializer = serializers.StacksSerializer(favorites, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def skills_list(request):
    if request.method == 'GET':
        logger.debug('In get')

        favorites = Skills.objects.all()
        serializer = serializers.SkillsSerializer(favorites, many=True)

        return Response(serializer.data)

    # elif request.method == 'POST':
    #     logger.debug('In POST')
    #
    #     serializer = serializers.FavouritesSerializer1(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response({'error': serializer.errors},
    #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET', 'PUT', 'DELETE'])
# def favorites_detail(request, favourite_id):
#     try:
#         Stacks.objects.get(id=favourite_id)
#     except Stacks.DoesNotExist as e:
#         return Response({'error': str(e)})
#
#     if request.method == 'GET':
#         serializer = serializers.StacksSerializer(favorite)
#         return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = serializers.FavouritesSerializer1(instance=favorite, data=request.data)
    #     if serializer.is_valid():
    #         logger.info('DATA SAVED')
    #
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response({'error': serializer.errors})
    #
    # elif request.method == 'DELETE':
    #     favorite.delete()
    #
    #     return Response({'deleted': True})

class StacksView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.StacksSerializer
    queryset = Stacks.objects.all()
    permission_class = [AllowAny, ]

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class SkillsView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SkillModel
    queryset = Skills.objects.all()
    permission_class = [AllowAny, ]

    def get_queryset(self):
        if 'y' in cache:
            queryset = cache.get('x')
            serializer = serializers.SkillModel(queryset)
            re = JSONRenderer().render(serializer.data)
            return re
        else:
            queryset = self.queryset.all()
            # serializer = self.serializer_class(queryset)
            cache.set("y", queryset, timeout=CACHE_TTL)
            print(cache)
            return queryset

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
            # isFav=False
            # if int(isFav) - 1==0:
            #     isFav = True
            if Developer.objects.get(id=dev_id):
                dev = Developer.objects.get(id=dev_id)
                logger.debug(isFav)
            if isFav == "one":
                logger.debug('qqqqTrue')
                if not Favorites.objects.filter(developer=dev, user=users).exists():
                    logger.debug('if not isFavTrue')
                    Favorites.objects.create(developer=dev, favorite_bool=True, user=users)
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