
from django.contrib import admin

from .models import Teacher, Subjects , Level, Department

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Subjects)
admin.site.register(Department)
admin.site.register(Level)
