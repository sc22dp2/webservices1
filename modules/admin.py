from django.contrib import admin

# Register your models here.
from .models import Module, Professor, Rating, ModuleInstance

admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(Rating)
admin.site.register(ModuleInstance)