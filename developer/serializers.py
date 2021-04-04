from rest_framework import serializers
from .models import Skills, Stacks, Developer, DeveloperService, Rating, Review, ImageTab
from userauth.models import User

class ReviewSerializer(serializers.Serializer):
    user = serializers.CharField()
    review = serializers.CharField(max_length=500)
    rating = serializers.FloatField()

class RatingSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    communication = serializers.FloatField()
    quality = serializers.FloatField()
    truth_review = serializers.FloatField()

class DeveloperServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeveloperService
        fields = ['__all__']
    

class StackSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, read_only=True)

class SkillSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, write_only=True)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "surname"]

class DevelopersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)
    stacks = StackSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, write_only=True)
    rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(write_only=True)
    price = serializers.IntegerField()

    class Meta:
        model = Developer
        fields = ["user", "stacks", "skills", "rating", "rating_count", "price"]

class FullInfoDeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    birth_date = serializers.DateField(format="%d.%m.%Y")
    city = serializers.CharField(read_only=False,write_only=False)
    rating = RatingSerializer()
    rating_count = serializers.IntegerField(write_only=True)
    review_count = serializers.IntegerField(write_only=True)
    dev_service = DeveloperServiceSerializer

    class Meta:
        model = Developer
        fields = ["user", "birth_date", "city", "dev_service", "rating", "about", "rating_count", "review_count"]


    