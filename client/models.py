from datetime import datetime

from django.db import models


class Client(models.Model):
    user = models.OneToOneField('userauth.User',
                                on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100,
                                    null=True, blank=True)
    def __str__(self):
        return self.user.email

class DevClientInContact(models.Model):
    dev_id = models.ManyToManyField("developer.Developer",
                                    null=True)
    dev_perm = models.BooleanField(null=True, default=False)
    client_id = models.ForeignKey(to="Client",
                                  on_delete=models.CASCADE)
    def __str__(self):
        return self.client_id.user.email

def burn_photos_path(instance, filename):
    user = instance.user_id
    date = datetime.today().strftime('%y-%m-%d')
    return f'project_file/users/{user.id}/{str(date)}/{filename}'

class BurnProject(models.Model):
    title = models.CharField(max_length=250,
                             null=True, blank=False)
    description = models.CharField(max_length=250,
                                   null=True, blank=True)
    deadline = models.DateField()
    file_doc = models.FileField(upload_to=burn_photos_path,
                                blank=True,
                                null=True
                                )
    user_id = models.ForeignKey("userauth.User",
                                on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.title

class ArchiveProject(models.Model):
    burn_project_id = models.ForeignKey(to="BurnProject",
                                        on_delete=models.CASCADE,
                                        null=True)
    user_id = models.ForeignKey("userauth.User",
                                on_delete=models.CASCADE,
                                null=True)
    accept_bool = models.BooleanField(null=True)
    def __str__(self):
        return self.burn_project_id.title

class BurnProjectDevelopers(models.Model):
    burn_project_id = models.ForeignKey(to="BurnProject",
                                        on_delete=models.CASCADE,
                                        null=True)
    developer_id = models.ForeignKey(to="developer.Developer",
                                     on_delete=models.CASCADE,
                                     null=True)
    price = models.IntegerField(default=10000, null=True,
                                blank=True)
    accept_bool = models.BooleanField(null=True, blank=True)
    stacks_id = models.ForeignKey(to="developer.Stacks", on_delete=models.CASCADE,
                                  null=True)
    def __str__(self):
        return self.burn_project_id.title

class BurnProjectStacks(models.Model):
    burn_project_id = models.ForeignKey(to="BurnProject",
                                        on_delete=models.CASCADE,
                                        null=True)
    stacks_id = models.ForeignKey(to="developer.Stacks", on_delete=models.CASCADE,
                                        null=True)
    def __str__(self):
        return self.burn_project_id.title

