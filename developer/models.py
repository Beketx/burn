from django.db import models
from userauth.models import User

class Stacks(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

class Skills(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.title

class Developer(models.Model):
    user = models.ForeignKey('userauth.User', on_delete=models.CASCADE)
    education = models.CharField(max_length=140, null=True)
    about = models.CharField(max_length=255, null=True)
    work_experience = models.CharField(max_length=255, null=True)
    dev_service = models.OneToOneField(to="DeveloperService", on_delete=models.CASCADE, null=True)
    stacks_id = models.ManyToManyField(Stacks)
    skills_id = models.ManyToManyField(Skills)
    def __str__(self):
        return self.education

class ImageTab(models.Model):
    developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500, null=True)
    image_type = models.ForeignKey(to="ImageType", on_delete=models.CASCADE)

"""\ImageType нужно модельку доделать, продумать как будет отпарвляться при [
    '1':url,
    2: type
    ]"""


class ImageType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_code = models.CharField(unique=True, max_length=20, blank=True, null=True)
    # front_photo = models.CharField(max_length=100, null=True)
    # avatar = models.CharField(max_length=100, null=True)
    # passport = models.CharField(max_length=100, null=True)

# class StackDev(models.Model):
#     developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True)
#     stack = models.ManyToManyField(to="Stacks", on_delete=models.CASCADE, null=True)



# class SkillDev(models.Model):
#     developer = models.ForeignKey(to="Developer", on_delete=models.CASCADE, null=True)
#     skill = models.ForeignKey(to="Skills", on_delete=models.CASCADE, null=True)

class DeveloperService(models.Model):
    service_title = models.CharField(max_length=100, null=True)
    service_description = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)
    price_fix = models.BooleanField(default=True)