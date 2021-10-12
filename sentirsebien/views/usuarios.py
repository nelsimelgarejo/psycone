from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import signing
from django.core.mail import send_mail
from psycone.settings import EMAIL_FROM_SENDGRID
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout

from sentirsebien.forms import SignUpForm
# Create your views here.
def send_email_task(subject, message, to_email):
    plain_message = strip_tags(message)
    send_mail(subject, plain_message, EMAIL_FROM_SENDGRID, to_email, html_message=message)


def ingreso_sistema(request):

    return render(request, 'usuarios/login.html')

def activar_cuenta(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        encoded_url = signing.dumps({"username": str(username), "email": str(email)})

        host = request.META.get('HTTP_HOST', '')
        scheme_url = request.is_secure() and "https" or "http"
        domain = f"{scheme_url}://{host}"

        subject = 'Activar cuenta en SENTIRSE BIEN'
        message = render_to_string('correos/activar_cuenta.html', {
                'username': username,
                'email': email,
                'ver_url': f"{domain}",
                'encoded_url': f"{encoded_url}"
            })
        send_email_task(subject, message, [email])
        return JsonResponse({'error': False, 'mensaje':'Se ha enviado un correo de activación a su correo'})
    else:
        return JsonResponse({'error': True, 'mensaje':'Existe un error en la petición'})


def aprobar_encode(request, encoded_url):
    json = signing.loads(encoded_url)
    username =json['username']
    email =json['email']

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        password1 = request.POST.get('password1')
        if form.is_valid():
            form.save()
            user = authenticate(username=username, password=password1)
            if user:
                login(request, user)
                return redirect('previo_ingreso')
            else:
                ctx = {
                    'username': username,
                    'email':email
                 }
                return render(request, 'usuarios/contrasenia.html', ctx)
        else:
            ctx = {
                    'username': username,
                    'email':email
                 }
            return render(request, 'usuarios/contrasenia.html', ctx)
    else:
        ctx = {
            'username': username,
            'email':email
        }
        return render(request, 'usuarios/contrasenia.html', ctx)

def previo_ingreso(request):
    usuario = get_object_or_404(User, username = request.user)
    return render(request, 'usuarios/previo_ingreso.html', {'usuario': usuario})

def post_ingreso_universidades(request):
    usuario = get_object_or_404(User, username = request.user)
    return render(request, 'usuarios/post_ingreso_universidades.html', {'usuario': usuario})




def cambiar_contrasenia(request):
    usuario = get_object_or_404(User, username = request.user)
    return render(request, 'usuarios/contrasenia.html', {'usuario': usuario})




def post_ingreso_otros(request):

    return render(request, 'usuarios/post_ingreso_otros.html')

def ingresar_dashboard(request):

    return render(request, 'dashboard/home.html')