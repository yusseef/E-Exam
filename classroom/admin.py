from django.contrib import admin
from classroom.models import User, Subject, Quiz, Question, Answer


# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
