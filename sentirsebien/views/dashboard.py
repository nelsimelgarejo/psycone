from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from sentirsebien.models import Perfil, FichaSociodemografica, ComponenteBienestar, ResultadoPerfil
from sentirsebien.forms import FichaSociodemograficaForm
from sentirsebien.models import topicos

# Create your views here.
def home(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    is_ficha = False
    is_sm = False
    is_asert = False
    is_das = False
    is_mspss = False
    is_pareja = False
    
    if not ComponenteBienestar.objects.filter(perfil=perfil).exists():
        """Permite crear los componentes para el nuevo usuario"""
        componentes = ComponenteBienestar.objects.filter(perfil=None)
        for componente in componentes:
            ComponenteBienestar.objects.create(
                perfil = perfil,
                topico = componente.topico,
                completado = componente.completado
            )

    if FichaSociodemografica.objects.filter(perfil = perfil).exists():
        is_ficha = True
    if ResultadoPerfil.objects.filter(perfil = perfil, topico = 'sa_mental').exists():
        is_sm = True
    if ResultadoPerfil.objects.filter(perfil = perfil, topico = 'asertividad').exists():
        is_asert = True
    if ResultadoPerfil.objects.filter(perfil = perfil, topico = 'das_ansiedad').exists():
        is_das = True
    if ResultadoPerfil.objects.filter(perfil = perfil, topico = 'ap_social').exists():
        is_mspss = True
    if ResultadoPerfil.objects.filter(perfil = perfil, topico = 'vi_pareja').exists():
        is_pareja = True

    ctx = {
        'perfil': perfil,
        'is_ficha' : is_ficha,
        'is_sm' : is_sm,
        'is_asert' : is_asert,
        'is_das' : is_das,
        'is_mspss' : is_mspss,
        'is_pareja' : is_pareja
    }
    return render(request, 'dashboard/home.html', ctx)


def ficha_sociodemografica(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    if request.method == 'POST':
        form = FichaSociodemograficaForm(request.POST)
        if form.is_valid():
            ficha =  form.save(commit=False)
            ficha.perfil = perfil
            ficha.save()
            
    return redirect('home')

def ficha_form(request):
    return render(request, 'dashboard/ficha_form.html')

def ver_perfil(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    return render(request, 'dashboard/perfil.html', {'perfil':perfil})

def ver_resultados(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    return render(request, 'dashboard/resultados.html', {'perfil':perfil})


def get_resultados_json(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)

    resultados = ResultadoPerfil.objects.filter(perfil=perfil)
    data = []

    for resultado_item in resultados:
        valor = ''
        if resultado_item.topico == 'sa_mental':
            if resultado_item.resultado == 'low':
                valor = 'Deficiente'
            elif resultado_item.resultado == 'medium':
                valor = 'Promedio'
            else:
                valor = 'Saludable'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Salud Mental Positiva',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })
        
        elif resultado_item.topico == 'asertividad':
            if resultado_item.resultado == 'low':
                valor = 'Baja'
            elif resultado_item.resultado == 'medium':
                valor = 'Media'
            else:
                valor = 'Alta'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Escala de Asertividad',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })

        elif resultado_item.topico == 'ap_social':
            if resultado_item.resultado == 'low':
                valor = 'Bajo'
            elif resultado_item.resultado == 'medium':
                valor = 'Promedio'
            else:
                valor = 'Alto'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Apoyo Social Percibido',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })
        
        elif resultado_item.topico == 'vi_pareja':
            if resultado_item.resultado == 'low':
                valor = 'Bajo'
            elif resultado_item.resultado == 'medium':
                valor = 'Moderado'
            else:
                valor = 'Alto'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Violencia de pareja',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })
        
        elif resultado_item.topico == 'das_ansiedad':
            if resultado_item.resultado == 'low':
                valor = 'Bajo'
            elif resultado_item.resultado == 'medium':
                valor = 'Promedio'
            else:
                valor = 'Alto'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Ansiedad',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })
        
        elif resultado_item.topico == 'das_estres':
            if resultado_item.resultado == 'low':
                valor = 'Bajo'
            elif resultado_item.resultado == 'medium':
                valor = 'Promedio'
            else:
                valor = 'Alto'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Estrés',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })
        
        elif resultado_item.topico == 'das_depresion':
            if resultado_item.resultado == 'low':
                valor = 'Bajo'
            elif resultado_item.resultado == 'medium':
                valor = 'Promedio'
            else:
                valor = 'Alto'
            data.append({
                'id': resultado_item.topico,
                'topico': 'Depresión',
                'resultado': valor,
                'puntaje': resultado_item.puntaje
            })
        
    return JsonResponse(data, safe=False)