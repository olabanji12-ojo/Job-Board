from django.contrib import admin

from .models import CustomUser, Profile, Job, Job_application


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Job_application)

# Register your models here.
