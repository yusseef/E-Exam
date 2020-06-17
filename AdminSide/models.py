from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length= 20)
    email= models.EmailField(max_length=30)


    def __str__(self):
        return self.name


class Subjects(models.Model):
    name = models.CharField(max_length=20)
#    level = models.ManyToManyField(Level)
    #department =models.ManyToManyField(Department, on_delete=models.CASCADE)
    teacher= models.ForeignKey(Teacher, on_delete=models.CASCADE)

    department =models.ManyToManyField('Department')
    level= models.ForeignKey('Level', on_delete=models.CASCADE, default ='')

    def __str__(self):
        return self.name


class Level(models.Model):
    name= models.CharField(max_length=20)
    #department =models.ManyToManyField('Department')


    def __str__(self):
        return self.name
class Department(models.Model):
    name=models.CharField(max_length=30)
    level= models.ForeignKey('Level', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
