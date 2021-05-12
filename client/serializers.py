from rest_framework import serializers

from developer.models import Developer, Stacks
from developer.serializers import DevelopersSerializer, DeveloperFIOSerializer
from . import models
from ast import literal_eval

class ProjectStacks(serializers.ModelSerializer):

    class Meta:
        model = models.BurnProjectStacks
        fields = ('__all__')

class DelProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BurnProject
        fields = ('id',)

class ProjectSerializer(serializers.ModelSerializer):
    # stacks_id = ProjectStacks(many=True)
    stacks_id = serializers.SerializerMethodField("get_stacks")
    # stacks_id = serializers.CharField(source="BurnProjectStacks", many=True)

    class Meta:
        model = models.BurnProject
        fields = ('id',
                  'title',
                  'description',
                  'stacks_id',
                  'deadline',
                  'user_id')

    def get_stacks(self, obj):
        stacks = models.BurnProjectStacks.objects.filter(
            burn_project_id=obj
        ).values('stacks_id', 'stacks_id__title')
        return stacks
class ProjectDelSerializer(serializers.ModelSerializer):
    # stacks_id = ProjectStacks(many=True)
    stacks_id = serializers.SerializerMethodField("get_stacks")
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.BurnProject
        fields = ('id',
                  'title',
                  'description',
                  'stacks_id',
                  'deadline',
                  'user_id')

    def get_stacks(self, obj):
        stacks = models.BurnProjectStacks.objects.filter(
            burn_project_id=obj
        ).values('stacks_id', 'stacks_id__title')
        return stacks

class ProjectAllSerializer(ProjectSerializer):
    file_doc = serializers.FileField()
    stacks =  serializers.CharField(write_only=True)
    stacks_id = serializers.SerializerMethodField("get_stacks")
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('file_doc', 'stacks', 'stacks_id')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        instance = models.BurnProject.objects.create(title=validated_data['title'],
                                          description=validated_data['description'],
                                          deadline=validated_data['deadline'],
                                          file_doc=validated_data['file_doc'],
                                          user_id=user)
        stacks = validated_data['stacks']
        stacks = literal_eval(stacks)
        for stack in stacks:
            stack_proj = models.BurnProjectStacks.objects.create(burn_project_id=instance,
                                                    stacks_id_id=stack)
        return instance
    def get_stacks(self, obj):
        stacks = models.BurnProjectStacks.objects.filter(
            burn_project_id=obj
        ).values('stacks_id', 'stacks_id__title')
        return stacks




class ProjectDevelopers(serializers.ModelSerializer):
    developer_id = DeveloperFIOSerializer(many=False,
                                        read_only=True)
    user_id = serializers.SerializerMethodField('get_user')
    price = serializers.IntegerField(write_only=True)
    stacks = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.BurnProjectDevelopers
        fields = (
                  'id',
                  'accept_bool',
                  'developer_id',
                  'user_id',
                  'price',
                  'stacks_id',
                  'stacks',
                  'burn_project_id',
                  )
    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        dev = Developer.objects.get(user=user)
        stack = Stacks.objects.get(id=validated_data['stacks'])
        instance = models.BurnProjectDevelopers.objects.create(
            price=validated_data['price'],
            developer_id=dev,
            burn_project_id=validated_data['burn_project_id'],
            stacks_id=stack
        )
        return instance

    def get_user(self, obj):
        user = obj.burn_project_id.user_id
        return {"id": user.id,
                "user": {
                    "name": user.name,
                    "surname": user.surname
                }}

class ProjectUser(serializers.ModelSerializer):
    developer_id = DeveloperFIOSerializer(many=False,
                                        read_only=True)
    user_id = serializers.SerializerMethodField('get_user')
    class Meta:
        model = models.BurnProjectDevelopers
        fields = ('id',
                  'accept_bool',
                  'developer_id',
                  'stacks_id',
                  'user_id',
                  'burn_project_id')

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        dev = Developer.objects.get(user=user)
        instance = models.BurnProjectDevelopers.objects.create(
            price=validated_data['price'],
            developer_id=dev,
            burn_project_id=validated_data['burn_project_id'],
            stacks_id=validated_data['stacks_id']
        )
        return instance

    def get_user(self, obj):
        user = obj.burn_project_id.user_id
        return {"id": user.id,
                "user": {
                    "name": user.name,
                    "surname": user.surname
                }}

class ProjectUserPost(serializers.ModelSerializer):
    # developer_id = DeveloperFIOSerializer(many=False,
    #                                     read_only=True)
    id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.BurnProjectDevelopers
        fields = ('id',
                  'accept_bool',
                  'developer_id',
                  'burn_project_id')
    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        instance = models.BurnProjectDevelopers.objects.filter(
            id=validated_data['id']).update(
            accept_bool=validated_data['accept_bool']
        )

        return instance
