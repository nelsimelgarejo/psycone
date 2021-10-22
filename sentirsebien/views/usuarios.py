from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import signing
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from sentirsebien.forms import SignUpForm, PerfilForm
from django.shortcuts import redirect, render, get_object_or_404
from sentirsebien.tasks import send_email_task
from sentirsebien.models import Perfil, DataUNFV, FichaSociodemografica
from django.core.signing import TimestampSigner


# Create your views here.
def ingreso_sistema(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username =  request.POST.get('username')
        password =  request.POST.get('password')
    
        if User.objects.filter(username = username).exists():
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'usuarios/login.html')
        else:
            return render(request, 'usuarios/login.html')
    else:
        return render(request, 'usuarios/login.html')


def activar_cuenta(request):
    if request.method == 'POST':
        form_user = SignUpForm(request.POST)
        form_perfil = PerfilForm(request.POST)  

        if form_user.is_valid() and form_perfil.is_valid():
            usuario = form_user.save(commit = False)
            perfil = form_perfil.save(commit=False)
            codigo_universitario = request.POST.get('username')
            password1 = request.POST.get('password1')
            data_user = get_object_or_404(DataUNFV, codigo_estudiante=codigo_universitario)
            usuario.first_name = data_user.nombre_completo
            usuario.email = data_user.correo
            usuario.save()
            perfil.usuario = usuario
            perfil.save()
            data_user.activado = True
            data_user.save()

            FichaSociodemografica.objects.create(
                perfil = perfil,
                anio_ingreso = int(data_user.codigo_estudiante[:4]), #Extrae las 4 primeros números para su años de ingreso
                facultad = data_user.facultad,
                escuela = data_user.escuela
            )

            return JsonResponse({'error': False})
        else:
            return JsonResponse({'error': True})
    else:
        return JsonResponse({'error': True})


def aprobar_encode(request, encoded_url):
    json = signing.loads(encoded_url)
    username =json['username']
    email =json['email']

    if User.objects.filter(username = username).exists():
        return redirect('ingreso_sistema')

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
                return render(request, 'usuarios/activar_cuenta.html', ctx)
        else:
            ctx = {
                    'username': username,
                    'email':email
                 }
            return render(request, 'usuarios/activar_cuenta.html', ctx)
    else:
        ctx = {
            'username': username,
            'email':email
        }
        return render(request, 'usuarios/activar_cuenta.html', ctx)

def previo_ingreso(request):
    usuario = get_object_or_404(User, username = request.user)
    return render(request, 'usuarios/previo_ingreso.html', {'usuario': usuario})

def post_ingreso_universidades(request):
    usuario = get_object_or_404(User, username = request.user)
    if Perfil.objects.filter(usuario = usuario).exists():
        return redirect('home')

    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
            return redirect('home')
        else:
            return render(request, 'usuarios/post_ingreso_universidades.html', {'usuario': usuario})
    else:
        return render(request, 'usuarios/post_ingreso_universidades.html', {'usuario': usuario})

def post_ingreso_otros(request):

    return render(request, 'usuarios/post_ingreso_otros.html')

def salir_cuenta(request):
    logout(request)
    return redirect('ingreso_sistema')

def cambiar_contrasenia(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        signer = TimestampSigner()
        encoded_url = signer.sign(username)
        #encoded_url = signing.dumps({"username": str(username), "email": str(email)})
        host = request.META.get('HTTP_HOST', '')
        scheme_url = request.is_secure() and "https" or "http"
        domain = f"{scheme_url}://{host}"

        subject = 'Recuperar contraseña en SENTIRSE BIEN'
        message = render_to_string('correos/recuperar_contrasenia.html', {
                'username': username,
                'email': email,
                'ver_url': f"{domain}",
                'encoded_url': f"{encoded_url}"
            })
        send_email_task(subject, message, [email])
        return JsonResponse({'error': False, 'mensaje':'Se ha enviado un correo de activación a su correo'})
    else:
        return JsonResponse({'error': True, 'mensaje':'Existe un error en la petición'})

def cambiar_contrasenia_encode(request, encoded_url):
    try:
        signer = TimestampSigner()
        username = signer.unsign(encoded_url, max_age=600) #Vence en 10 segundos
        usuario = get_object_or_404(User, username = username)
        if request.method == 'POST':
            form = SignUpForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('ingreso_sistema')
        else:
            ctx = {
                'usuario': usuario
                 }
            return render(request, 'usuarios/cambiar_contrasenia.html', ctx)
    except:
        return render(request, 'usuarios/expirado.html')

def codigo_universitario(request):
    myDict = dict(request.GET)
    codigo_estudiante = myDict['codigo_universitario'][0]

    response = {}
    if DataUNFV.objects.filter(codigo_estudiante = codigo_estudiante, activado = False).exists():
        response['activado'] = False
        response['existe'] = True
    elif DataUNFV.objects.filter(codigo_estudiante = codigo_estudiante, activado = True).exists():
        response['activado'] = True
        response['existe'] = True
    else:
        response['activado'] = False
        response['existe'] = False

    return JsonResponse(response)
    
def dni_usuario(request):
    myDict = dict(request.GET)
    dni = myDict['dni_usuario'][0]
    codigo_universitario = myDict['codigo_universitario'][0]

    response = {}
    if DataUNFV.objects.filter(codigo_estudiante=codigo_universitario, dni = dni, activado = False).exists():
        response['activado'] = False
        response['existe'] = True
    else:
        response['activado'] = True
        response['existe'] = False

    return JsonResponse(response)