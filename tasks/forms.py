# podemos crear nuestros propios formularios personalizados
# importamos la clase ModelForm del modulo django.forms, la cual podre extender
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        # pongo el modelo en el que estare basado
        model = Task

        # los campos que usare
        fields = ["title", "description", "important"]

        # propiedad para poder ponerle clases o cualquier atributo
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Write a title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Write a description"}
            ),
            "important": forms.CheckboxInput(
                attrs={"class": "form-check-input my-2 m-auto"}
            ),
        }
