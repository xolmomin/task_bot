from django.contrib import admin
from django.contrib.auth.models import Group, User

from app.models import TgUser

admin.site.register(TgUser)
admin.site.unregister(Group)
admin.site.unregister(User)
