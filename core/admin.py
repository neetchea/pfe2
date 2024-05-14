from django.contrib import admin
from .models import CustomUser, Classroom

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Classroom)