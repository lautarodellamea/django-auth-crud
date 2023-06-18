from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(
        blank=True
    )  # si no me pasan nada por defecto el campo estara vacio
    created = models.DateTimeField(
        auto_now_add=True
    )  # cuando creemos una tarea se añadira por defecto la fecha y hora si no le pasamos el dato
    datecompleted = models.DateTimeField(
        null=True, blank=True
    )  # campo vacio inicialmente, obligatorioo para la base de datos y opcional para mi
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # el self hace referencia a la misma clase es como el this
    # hacemos este metodo para ver bien los datos en admin
    def __str__(self):
        return self.title + "- by " + self.user.username
