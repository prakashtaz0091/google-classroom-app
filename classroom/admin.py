from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Profile)
admin.site.register(models.Classroom)
admin.site.register(models.StudentClassroom)