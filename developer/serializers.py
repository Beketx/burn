from rest_framework import serializers

from userauth.serializers import UserSerializer
from .models import Skills, Stacks, Developer, DeveloperService, Rating, Review, ImageTab
from userauth.models import User, City
from devutils.serializers import StacksSerializer, StackTitleSerializer, SkillTitleSerializer, SkillsSerializer

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
        fields = ['service_title', 'service_description', 'price', 'price_fix']


class DevelopersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)
    stacks = StackTitleSerializer(many=True, read_only=True)
    skills = SkillTitleSerializer(many=True, write_only=True)
    rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(write_only=True)
    price = serializers.IntegerField()

    class Meta:
        model = Developer
        fields = ["user", "stacks", "skills", "rating", "rating_count", "price"]

class FullInfoDeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    # birth_date = serializers.DateField(format="%d.%m.%Y")
    # city = serializers.CharField(read_only=False,write_only=False)
    rating = RatingSerializer(many=False, read_only=True)
    rating_count = serializers.IntegerField(write_only=True)
    review_count = serializers.IntegerField(write_only=True)
    dev_service = DeveloperServiceSerializer(many=False)

    class Meta:
        model = Developer
        fields = ["user", "dev_service", "rating", "about", "rating_count", "review_count"]
