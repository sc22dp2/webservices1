from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Module(models.Model):
    code = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=30, default="")

class Professor(models.Model):
    prof_id = models.CharField(max_length=10, default="")
    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    def get_full_name(self):
        return "%s. %s"%(self.first_name[0], self.last_name)
    full_name = property(get_full_name)

class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    semester = models.IntegerField(default=0)
    professor = models.ManyToManyField(Professor)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(ModuleInstance,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)