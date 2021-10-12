from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def activar_cuenta(request):

    return render(request, 'usuarios/login.html')

def cambiar_contrasenia(request):

    return render(request, 'usuarios/contrasenia.html')

def previo_ingreso(request):

    return render(request, 'usuarios/previo_ingreso.html')

def post_ingreso_universidades(request):

    return render(request, 'usuarios/post_ingreso_universidades.html')

def post_ingreso_otros(request):

    return render(request, 'usuarios/post_ingreso_otros.html')

def ingresar_sistema(request):

    return render(request, 'dashboard/home.html')