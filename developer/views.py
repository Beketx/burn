from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny

from userauth.models import User
from .models import Skills, Stacks, Developer, DeveloperService, Rating, Review, ImageTab
from .serializers import DevelopersSerializer, StackSerializer, SkillSerializer, FullInfoDeveloperSerializer

#birth_date = birth_date.strftime("%d.%m.%Y") if birth_date else None

class DeveloperProfiles(RetrieveModelMixin, ListModelMixin , GenericViewSet):
    serializer_class = FullInfoDeveloperSerializer
    serializer_action_class = {
        'list': FullInfoDeveloperSerializer,
        'retrieve': DevelopersSerializer
    }
    queryset = Developer.objects.filter(stacks_id=1)
    permission_classes = (AllowAny, )
    # pagination_class = CustomDeveloeprPagination

    def get_serializer_class(self):
        try:
            return self.serializer_action_class[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()