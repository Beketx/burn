from django.urls import path

from userauth.views import CitiesView
from developer import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('developer-profiles', views.DeveloperProfiles, basename='devprofs')
urlpatterns = router.urls
# urlpatterns = [
#     path('developer-profiles/', views.DeveloperProfiles.as_view()),
#     # path('developer-profiles/<int:pk>/', views.DeveloperProfiles.as_view())
# ]


