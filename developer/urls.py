from django.urls import path

from userauth.views import CitiesView
from developer import views
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('developer-profiles/', views.DeveloperProfiles.as_view()),
    path('developer-profiles/<int:pk>/', views.DeveloperProfiles.as_view())
]


