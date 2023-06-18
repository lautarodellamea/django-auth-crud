from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# django ya permite autenticar y tener la forma de hacer login en nuestra aplicacion
# me da ya un formulario
# uno crea y el otro autentica
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# django me permite reutilizar esta clase User para poder registrar nuestros usuarios
from django.contrib.auth.models import User

#  cuando creamos el usuario debemos autenticarlo y crear una cookie
from django.contrib.auth import login, logout, authenticate

# para especificar un error de inegridad en la base de datos, cuando quiero guardar algo que ya existe
from django.db import IntegrityError

# importo un formulario personalizado que cree
from .forms import TaskForm

# lo vamos a usar para hacer una consulta
from .models import Task

# modulo de django para manejar tiempo
from django.utils import timezone

# decorador que me permite proteger rutas
from django.contrib.auth.decorators import login_required


# este archivo views sirve para que ejecutemos algo cuando una url es visitada
# el parametro request es un parametro que django ofrece para obtener informacion del cliente que a visitado la pagina
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        # print("Enviando/Mostrando Formulario")
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        # print("Obteniendo Datos del Formulario")
        # print(request.POST)

        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not password1 or not password2:
            return render(
                request,
                "signup.html",
                {
                    "error": "Please complete all fields",
                    "form": UserCreationForm,
                },
            )

        if password1 != password2:
            return render(
                request,
                "signup.html",
                {"error": "Passwords do not match", "form": UserCreationForm},
            )

        # si las contraseñas son iguyales las guardo y registro
        # if request.POST["password1"] == request.POST["password2"]:
        if request.POST["password1"] == request.POST["password2"]:
            # la base de datos puede tener sus propias validaciones, si llega a fallar manejo el error para que no tumbe la aplicacion
            try:
                # registrar usuario
                # creamos el usuario pero no lo guardamos en la base de datos
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                # guardamos en la base de datos
                user.save()

                # creamos la cookie, para ver si este usuario creo tareas, si tiene acceso a determinadas paginas y demas
                login(request, user)

                return redirect("tasks")

            # de esta forma podemos validar diferentes tipos de errores en esta vista
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "User already exists"},
                )


@login_required
def tasks(request):
    title = "Pending"
    # de esta forma solo puestro las tareas del usuario logeado, y solo las tareas que no estan completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {"tasks": tasks, "title": title})


@login_required
def tasks_completed(request):
    title = "Completed"
    # de esta forma solo puestro las tareas del usuario logeado, y solo las tareas que no estan completadas
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by(
        "-datecompleted"
    )  # las ordena de manera descendento por el "-"
    return render(request, "tasks.html", {"tasks": tasks, "title": title})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            # print(request.POST)

            # estamos recibiendo los datos, se los paso a la clase TaskForm y este genera por mi un formulario
            # lo usamos para guardar los datos de este
            form = TaskForm(request.POST)
            # print(form)

            # con el commit=False le decimos que no lo guarde
            # queremos que me devuleva los datos que hay dentro de ese formulario
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            # print(new_task)

            return redirect("tasks")

        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Please enter valid data"},
            )


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        # print(task_id)
        task = get_object_or_404(Task, pk=task_id, user=request.user)

        # crea un formulario con los datos dentro, nos servira para editar
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            # el tercer parametro es para que me muestre solo mis tareas y no la de otros usuarios
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")

        except:
            return render(
                request,
                "task_detail.html",
                {
                    "task": task,
                    "form": form,
                    "error": "Error while updating",
                },
            )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        # print(request.POST)

        # si el autenticate es valido me devuelve un usuario, sino va a estar vacio
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Incorrect user name and/or password",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")
