from django.db import models

from developer.models import Developer
from userauth.models import User


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True, blank=True)