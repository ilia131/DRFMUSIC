from django.contrib import admin

from .models import Profile , UserAccount , Comment

admin.site.register(Profile)
admin.site.register(UserAccount)
admin.site.register(Comment)