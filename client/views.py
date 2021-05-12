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


class CustomPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return True

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

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         self.permission_classes = [AllowAny, ]
    #     if self.request.method == 'PUT':
    #         self.permission_classes = [CustomPermission]

    @action(methods=['GET'], detail=False,
            permission_classes=[IsAuthenticated, ],
            url_path='my-projects',)
    def my_projects(self, request,
                    *args, **kwargs):
        projects = self.queryset.filter(user_id=self.request.user)
        serializer_class = serializers.ProjectSerializer
        serializer = serializer_class(projects, many=True)
        return Response(serializer.data)

    # def perform_update(self, serializer):
    #     user_instance = serializer.instance


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

class UserDevProjects(viewsets.ModelViewSet):
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

class ArchiveProject(viewsets.ModelViewSet):
    queryset = models.ArchiveProject.objects.all()
    serializer_class = serializers.ProjectDelSerializer
    # pagination_class = DeveloperPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        instance = self.queryset.get(user_id=self.request.user)\
        .select_related('burn_project_id')
        # .values(
        #         'burn_project_id__title',
        #         'burn_project_id__description',
        #         'burn_project_id__file_doc',
        #         'burn_project_id__deadline',
        #         'burn_project_id__user_id')
        # instance = models.BurnProject.objects.filter(id=instance.burn_project_id_id)
        # data = []
        # for i in instance:
        #     data.append(models.BurnProject.objects.get(id=i.burn_project_id))
        return instance

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProjectDelSerializer
        if self.action == 'retrieve':
            return serializers.ProjectDelSerializer
        return serializers.ProjectDelSerializer

class DeleteProject(viewsets.ModelViewSet):
    queryset = models.BurnProject.objects.all()
    serializer_class = serializers.DelProjectSerializer
    # pagination_class = DeveloperPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)