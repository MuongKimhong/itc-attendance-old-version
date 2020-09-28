from django.contrib import admin

# Register your models here.
from .models import Department, Year, Type, Class

admin.site.register(Department)
admin.site.register(Year)
admin.site.register(Type)
admin.site.register(Class)
