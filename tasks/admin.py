from django.contrib import admin
from .models import Task


# con esto vamos a poder ver en admin, la fecha de creacion de una task ya que esta se agrega por defecto
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


# Register your models here.
# para visualizarlos en admin
admin.site.register(Task, TaskAdmin)
