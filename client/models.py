from django.db import models


class Client(models.Model):
    user = models.OneToOneField('userauth.User', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True, blank=True)

class DevClientInContact(models.Model):
    dev_id = models.ForeignKey("developer.Developer", on_delete=models.DO_NOTHING, null=True)
    dev_perm = models.BooleanField(null=True, default=False)
    client_id = models.OneToOneField(to="Client", on_delete=models.CASCADE)
