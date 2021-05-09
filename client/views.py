from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from developer.models import Developer
from utils.developer_pagination.pagination import DeveloperPagination
from . import serializers, models
from .models import DevClientInContact, Client

class ClientContactDev(APIView):
    """
    {
    dev_id:123
    }
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        res = {
            'status': True,
            'detail': 'Message to developer send'
        }
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            user = request.user
            client = Client.objects.get(user=user)
            dev_id = data["developer_id"]
            if Developer.objects.get(id=dev_id):
                dev = Developer.objects.get(id=dev_id)
            if not DevClientInContact.objects.filter(client_id=client).exists():
                contact = DevClientInContact.objects.create(client_id=client)
            contact = DevClientInContact.objects.get(client_id=client)
            contact.dev_id.add(dev)
            res = {
                'status': True,
                'detail': 'Message to developer send'
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            res = {
                'status': False,
                'detail': 'Message to developer not send'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)


class BurnProject(viewsets.ModelViewSet):
    queryset = models.BurnProject.objects.all()
    serializer_class = serializers.ProjectAllSerializer
    pagination_class = DeveloperPagination
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProjectSerializer
        if self.action == 'retrieve':
            return serializers.ProjectAllSerializer
        return serializers.ProjectAllSerializer

    @action(methods=['GET', 'PUT'], detail=False,
            permission_classes=[IsAuthenticated, ],
            url_path='my-projects',)
    def my_projects(self, request,
                    *args, **kwargs):
        projects = self.queryset.filter(user_id=self.request.user)
        serializer_class = serializers.ProjectSerializer
        if self.request.method == 'PUT':
            serializer_class = serializers.ProjectAllSerializer
        serializer = serializer_class(projects)
        print(serializer.data)
        return Response(serializer.data)

class DeveloperProjects(viewsets.ModelViewSet):
    queryset = models.BurnProjectDevelopers.objects.all()
    serializer_class = serializers.ProjectDevelopers
    pagination_class = DeveloperPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
    #     try:
        user = Developer.objects.get(user=self.request.user)
        return self.queryset.filter(developer_id=user)


class UserProjects(viewsets.ModelViewSet):
    queryset = models.BurnProjectDevelopers.objects.all()
    serializer_class = serializers.ProjectUser
    pagination_class = DeveloperPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        burn_project = models.BurnProjectDevelopers.objects.filter(burn_project_id__user_id=self.request.user)
        return burn_project

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProjectUser
        if self.action == 'retrieve':
            return serializers.ProjectUser
        if self.action == 'create':
            return serializers.ProjectUserPost