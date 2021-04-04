from django.urls import path
from .views import DeveloperProfiles
from rest_framework.routers import DefaultRouter
# urlpatterns = [
#     path('developer-profiles/', DeveloperProfiles)
# ]

router = DefaultRouter()

router.register("developer-profiles", DeveloperProfiles, basename="DEV")

urlpatterns = router.urls

