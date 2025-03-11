from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    code = models.CharField(max_length=10, unique = True, null = False)
    name = models.CharField(max_length=50, unique = True, null = False)

class Professor(models.Model):
    prof_id = models.CharField(max_length=10, unique = True, null = False)
    first_name = models.CharField(max_length=30, null = False)
    last_name = models.CharField(max_length=30, null = False)
    # function for getting the full name as required
    def get_full_name(self):
        return "%s. %s"%(self.first_name[0], self.last_name)
    full_name = property(get_full_name)

class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField(null = False)
    semester = models.IntegerField(null = False)
    professor = models.ManyToManyField(Professor)

# makes list for rating choices
rating_choices = []
for i in range(1,6):
    rating_choices.append((i, str(i)))

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User is the build-in Django User Model
    module = models.ForeignKey(ModuleInstance,on_delete=models.CASCADE)
    rating = models.IntegerField(choices = rating_choices, null = False)