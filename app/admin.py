from django.contrib import admin

# Register your models here.
from .models import Department, Year, Class

admin.site.register(Department)
admin.site.register(Year)
admin.site.register(Class)
