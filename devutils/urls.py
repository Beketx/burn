from rest_framework.routers import DefaultRouter

from client.views import BurnProject, DeveloperProjects, UserProjects
from userauth.views import CitiesView
from .views import SkillsView, StacksView

router = DefaultRouter()


router.register("skills", SkillsView, basename="skills")
router.register("stacks", StacksView, basename="stacks")
router.register("cities", CitiesView, basename="cities")
router.register("burn-projects", BurnProject, basename="burns")
router.register("dev-projects", DeveloperProjects, basename="burns-devs")
router.register("user-projects", UserProjects, basename="burns-users")
router.register("burn-projects", BurnProject, basename="burns")

# path('burn-projects/', views.BurnProject, name='burns')
urlpatterns = router.urls
