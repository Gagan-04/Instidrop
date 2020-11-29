from django.contrib import admin
from django.contrib.auth.models import User
from app.models import Profile,Faculty,Faculty_subjects,Students,ReqTypes,ReqDetails

admin.site.register(Profile)
admin.site.register(Faculty)
admin.site.register(Faculty_subjects)
admin.site.register(Students)
admin.site.register(ReqTypes)
admin.site.register(ReqDetails)