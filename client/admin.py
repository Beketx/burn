from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(DevClientInContact)
admin.site.register(BurnProject)
admin.site.register(BurnProjectDevelopers)
admin.site.register(BurnProjectStacks)
admin.site.register(ArchiveProject)
